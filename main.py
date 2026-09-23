# from fastapi import FastAPI

# from app.catalog.router import router as catalog_router
# from app.order.router import router as order_router
# from app.worker.router import router as worker_router

# #from app.catalog.service import get_products, create_product


# app = FastAPI(title="Catalog Service")
# app.include_router(catalog_router)
# app.include_router(order_router)
# app.include_router(worker_router)


# # class Product(BaseModel):
# #     name: str = Field(min_length=1)
# #     price: float = Field(gt=0)


# @app.get("/health")
# def health_check():
#     return {"status": "healthy"}


# # @app.get("/products")
# # def get_all_products():
# #     return get_products()


# # @app.post("/products")
# # def add_product(product: Product):
# #     return create_product(
# #         name=product.name,
# #         price=product.price
# #     )

import time

from fastapi import FastAPI, Request
from prometheus_client import generate_latest
from starlette.responses import Response

from app.catalog.router import router as catalog_router
from app.order.router import router as order_router
from app.worker.router import router as worker_router
from app.metrics.collector import (
    REQUEST_COUNT,
    REQUEST_ERROR_COUNT,
    REQUEST_LATENCY,
)


app = FastAPI(title="SLO-Driven API Platform")


app.include_router(catalog_router)
app.include_router(order_router)
app.include_router(worker_router)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    elapsed_time = time.perf_counter() - start_time

    path = request.url.path
    method = request.method
    status = str(response.status_code)

    REQUEST_COUNT.labels(
        method=method,
        path=path,
        status=status,
    ).inc()

    REQUEST_LATENCY.labels(
        method=method,
        path=path,
    ).observe(elapsed_time)

    if response.status_code >= 400:
        REQUEST_ERROR_COUNT.labels(
            method=method,
            path=path,
            status=status,
        ).inc()

    return response


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type="text/plain",
    )