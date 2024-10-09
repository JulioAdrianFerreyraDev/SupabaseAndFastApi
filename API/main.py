from fastapi import FastAPI
from .data import create_models
from .routes import user_router
app = FastAPI()

create_models()

app.include_router(user_router)