from fastapi import FastAPI
from .database import engine
from .models import Base
from .routers import credits, schema_admin
from .tasks import start_scheduler

app = FastAPI(title="LawVriksh Credit Management API", version="1.0.0")

# Create tables if not exist (for dev)
Base.metadata.create_all(bind=engine)

# Routers
app.include_router(credits.router)
app.include_router(schema_admin.router)

# Scheduler (starts when app starts)
scheduler = start_scheduler()

@app.get("/")
def root():
    return {"status": "ok", "service": "credit-management"}
