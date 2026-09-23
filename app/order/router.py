from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.order.service import create_order, get_orders


router = APIRouter(prefix="/orders", tags=["Orders"])


class Order(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)


@router.get("")
def get_all_orders():
    return get_orders()


@router.post("")
def add_order(order: Order):
    return create_order(
        product_id=order.product_id,
        quantity=order.quantity
    )