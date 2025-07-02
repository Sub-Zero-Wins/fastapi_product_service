from pydantic import BaseModel, Field, condecimal
from typing import Optional, List

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=500)
    price: condecimal(gt=0)
    in_stock: Optional[bool] = True

class ProductUpdate(ProductCreate):
    pass

class ProductResponse(ProductCreate):
    id: int

    class Config:
        orm_mode = True

class BulkProductCreate(BaseModel):
    products: List[ProductCreate]
