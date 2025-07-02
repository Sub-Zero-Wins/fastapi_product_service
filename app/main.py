from fastapi import FastAPI
from app.api.v1 import routes as product_routes
from app.db.database import engine, Base
from app.exceptions import custom_exceptions
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Product Service API",
    version="1.0.0",
    description="A FastAPI microservice for managing products",
    docs_url="/docs"
)

app.include_router(product_routes.router)

app.add_exception_handler(RequestValidationError, custom_exceptions.validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, custom_exceptions.custom_http_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
