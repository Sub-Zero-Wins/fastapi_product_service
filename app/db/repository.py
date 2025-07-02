from sqlalchemy.orm import Session
from app.db import models
from app.schemas.product import ProductCreate, ProductUpdate

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_all_products(db: Session, skip: int = 0, limit: int = 10, sort_by: str = "id", order: str = "asc"):
    query = db.query(models.Product)
    if order.lower() == "desc":
        query = query.order_by(getattr(models.Product, sort_by).desc())
    else:
        query = query.order_by(getattr(models.Product, sort_by).asc())
    return query.offset(skip).limit(limit).all()

def create_product(db: Session, product: ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: ProductUpdate):
    db_product = get_product(db, product_id)
    if not db_product:
        return None
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if not db_product:
        return None
    db.delete(db_product)
    db.commit()
    return db_product
