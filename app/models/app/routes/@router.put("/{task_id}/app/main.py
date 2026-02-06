from fastapi import FastAPI
from app.routes import tasks

app = FastAPI(title="Smart Task & Productivity Manager")

app.include_router(tasks.router)
