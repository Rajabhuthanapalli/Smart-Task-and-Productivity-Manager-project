from fastapi import FastAPI
from .database import Base, engine
from . import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Task & Productivity Manager")

@app.get("/")
def root():
    return {"message": "Smart Task Manager API is running"}
