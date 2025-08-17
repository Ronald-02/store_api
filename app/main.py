from fastapi import FastAPI
from app.controllers import product_controller

app = FastAPI(title="Store API")

app.include_router(product_controller.router)
