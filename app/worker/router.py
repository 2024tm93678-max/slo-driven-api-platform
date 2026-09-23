from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.worker.service import process_order, get_jobs


router = APIRouter(prefix="/worker", tags=["Worker"])


class Job(BaseModel):
    order_id: int = Field(gt=0)


@router.get("")
def get_all_jobs():
    return get_jobs()


@router.post("")
def process_order_job(job: Job):
    return process_order(order_id=job.order_id)