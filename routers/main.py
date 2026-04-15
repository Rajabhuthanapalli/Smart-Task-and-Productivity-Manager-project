from fastapi import FastAPI
from routers import logs

app = FastAPI()

app.include_router(logs.router)
