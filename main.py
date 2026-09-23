from fastapi import FastAPI

from app.catalog.router import router as catalog_router
from app.order.router import router as order_router
from app.worker.router import router as worker_router

#from app.catalog.service import get_products, create_product


app = FastAPI(title="Catalog Service")
app.include_router(catalog_router)
app.include_router(order_router)
app.include_router(worker_router)


# class Product(BaseModel):
#     name: str = Field(min_length=1)
#     price: float = Field(gt=0)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# @app.get("/products")
# def get_all_products():
#     return get_products()


# @app.post("/products")
# def add_product(product: Product):
#     return create_product(
#         name=product.name,
#         price=product.price
#     )

