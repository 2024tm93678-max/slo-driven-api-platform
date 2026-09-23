jobs = []


def process_order(order_id: int):
    job = {
        "id": len(jobs) + 1,
        "order_id": order_id,
        "status": "processed"
    }

    jobs.append(job)

    return job


def get_jobs():
    return jobs