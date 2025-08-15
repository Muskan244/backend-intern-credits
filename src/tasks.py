from datetime import datetime, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import select
from .database import SessionLocal
from . import models

def add_daily_credits():
    db = SessionLocal()
    try:
        # lock all credit rows in batches
        users = db.execute(select(models.User.user_id)).all()
        now = datetime.now(timezone.utc)
        for (user_id,) in users:
            credit = db.get(models.Credit, user_id)
            if not credit:
                credit = models.Credit(user_id=user_id, credits=5, last_updated=now)
                db.add(credit)
            else:
                credit.credits += 5
                credit.last_updated = now
        db.commit()
        print(f"[scheduler] Added +5 credits to {len(users)} users @ {now.isoformat()}")
    except Exception as e:
        db.rollback()
        print(f"[scheduler] FAILED: {e}")
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler(timezone="UTC")
    scheduler.add_job(add_daily_credits, CronTrigger(hour=0, minute=0))
    scheduler.start()
    return scheduler
