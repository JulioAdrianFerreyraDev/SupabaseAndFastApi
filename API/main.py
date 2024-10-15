from fastapi import FastAPI

from .data import create_models
from .routes import user_router, auth_router, admin_router, products_router, sales_router, sold_products_router

app = FastAPI()

create_models()

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(products_router)
app.include_router(sales_router)
app.include_router(sold_products_router)
