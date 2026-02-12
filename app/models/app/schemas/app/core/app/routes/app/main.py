from fastapi import FastAPI
from app.routes import tasks, auth

app = FastAPI(title="Smart Task & Productivity Manager")

app.include_router(tasks.router)
app.include_router(auth.router)
