from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, BulkProductCreate
from app.db.database import SessionLocal
from app.services import product_service
from app.db import repository
from app.core.security import authenticate_user

router = APIRouter(prefix="/api/v1/products", tags=["Products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[ProductResponse])
def get_products(skip: int = 0, limit: int = 10, sort_by: str = "id", order: str = "asc", db: Session = Depends(get_db)):
    return repository.get_all_products(db, skip, limit, sort_by, order)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = product_service.get_product_by_id(product_id, db)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(authenticate_user)])
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return product_service.create_product_service(product, db)

@router.put("/{product_id}", response_model=ProductResponse, dependencies=[Depends(authenticate_user)])
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    updated = product_service.update_product_service(product_id, product, db)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(authenticate_user)])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    deleted = product_service.delete_product_service(product_id, db)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")

@router.post("/bulk-upload", response_model=List[ProductResponse], status_code=201, dependencies=[Depends(authenticate_user)])
def bulk_upload_products(payload: BulkProductCreate, db: Session = Depends(get_db)):
    return [product_service.create_product_service(p, db) for p in payload.products]
