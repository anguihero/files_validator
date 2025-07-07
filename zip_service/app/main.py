from fastapi import FastAPI
from app.routes import validate

app = FastAPI(title="Gateway Validador")

app.include_router(validate.router)
