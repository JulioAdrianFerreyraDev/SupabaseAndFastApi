from fastapi import FastAPI
from .data import create_models
from .routes import user_router, auth_router

app = FastAPI()

create_models()

app.include_router(user_router)
app.include_router(auth_router)