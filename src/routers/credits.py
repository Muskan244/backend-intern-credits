from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from datetime import datetime, timezone

from .. import models, deps
from ..schemas import CreditBalance, AmountIn

router = APIRouter(prefix="/api/credits", tags=["Credits"])

def _ensure_credit_row(db: Session, user_id: int) -> models.Credit:
    # lock the credit row if exists, create if missing
    credit = db.execute(
        select(models.Credit).where(models.Credit.user_id == user_id).with_for_update(nowait=False)
    ).scalar_one_or_none()
    if credit:
        return credit

    # verify user exists
    user = db.execute(select(models.User).where(models.User.user_id == user_id)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    credit = models.Credit(user_id=user_id, credits=0, last_updated=datetime.now(timezone.utc))
    db.add(credit)
    db.flush()  # get it persisted in the transaction
    return credit

@router.get("/{user_id}", response_model=CreditBalance)
def get_balance(user_id: int, db: Session = Depends(deps.get_db)):
    credit = db.execute(select(models.Credit).where(models.Credit.user_id == user_id)).scalar_one_or_none()
    if not credit:
        # return zero with ensured row for consistency
        credit = _ensure_credit_row(db, user_id)
    return CreditBalance.model_validate(credit)

@router.post("/{user_id}/add", response_model=CreditBalance)
def add_credits(user_id: int, payload: AmountIn, db: Session = Depends(deps.get_db)):
    credit = _ensure_credit_row(db, user_id)
    credit.credits += payload.amount
    credit.last_updated = datetime.now(timezone.utc)
    db.flush()
    return CreditBalance.model_validate(credit)

@router.post("/{user_id}/deduct", response_model=CreditBalance)
def deduct_credits(user_id: int, payload: AmountIn, db: Session = Depends(deps.get_db)):
    credit = _ensure_credit_row(db, user_id)
    if credit.credits - payload.amount < 0:
        raise HTTPException(status_code=400, detail="Insufficient credits (cannot go negative)")
    credit.credits -= payload.amount
    credit.last_updated = datetime.now(timezone.utc)
    db.flush()
    return CreditBalance.model_validate(credit)

@router.patch("/{user_id}/reset", response_model=CreditBalance)
def reset_credits(user_id: int, db: Session = Depends(deps.get_db)):
    credit = _ensure_credit_row(db, user_id)
    credit.credits = 0
    credit.last_updated = datetime.now(timezone.utc)
    db.flush()
    return CreditBalance.model_validate(credit)
