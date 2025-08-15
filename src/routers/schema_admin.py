import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from .. import deps
from ..schemas import ApplySchemaSQL
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/schema", tags=["Schema Admin"])

ADMIN_TOKEN = os.getenv("ADMIN_SCHEMA_TOKEN")  # optional guard

@router.post("/apply")
def apply_schema_sql(payload: ApplySchemaSQL, db: Session = Depends(deps.get_db)):
    if ADMIN_TOKEN and payload.token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Forbidden: invalid token")

    try:
        db.execute(text(payload.sql))
        # transaction will commit via deps.get_db()
        return {"status": "ok", "message": "Schema updated/applied"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Schema apply failed: {e}")
