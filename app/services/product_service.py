import json
import redis
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db import repository
from app.schemas.product import ProductCreate, ProductUpdate

redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
CACHE_TTL = 60

def get_product_by_id(product_id: int, db: Session):
    cache_key = f"product:{product_id}"
    if cached := redis_client.get(cache_key):
        return json.loads(cached)

    db_product = repository.get_product(db, product_id)
    if db_product:
        redis_client.setex(cache_key, CACHE_TTL, json.dumps({
            "id": db_product.id,
            "name": db_product.name,
            "description": db_product.description,
            "price": db_product.price,
            "in_stock": db_product.in_stock
        }))
    return db_product

def create_product_service(product: ProductCreate, db: Session):
    return repository.create_product(db, product)

def update_product_service(product_id: int, product: ProductUpdate, db: Session):
    updated = repository.update_product(db, product_id, product)
    if updated:
        redis_client.delete(f"product:{product_id}")
    return updated

def delete_product_service(product_id: int, db: Session):
    deleted = repository.delete_product(db, product_id)
    if deleted:
        redis_client.delete(f"product:{product_id}")
    return deleted
