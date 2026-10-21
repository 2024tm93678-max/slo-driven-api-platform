import time

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.catalog.service import get_products, create_product


router = APIRouter(prefix="/products", tags=["Catalog"])


class Product(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(gt=0)

@router.get("/slow")
def get_slow_products():
    time.sleep(0.4)
    return get_products()

@router.get("")
def get_all_products():
    return get_products()


@router.post("")
def add_product(product: Product):
    return create_product(
        name=product.name,
        price=product.price
    )