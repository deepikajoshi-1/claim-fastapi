from fastapi import FastAPI
from app.api.routes import auth

app = FastAPI(title="Claims Insurance Platform")

app.include_router(auth.router)
