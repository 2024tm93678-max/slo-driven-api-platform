import time

import httpx


def run_workload(
    base_url: str,
    request_count: int = 20,
) -> dict:
    success_count = 0
    error_count = 0
    latencies_ms = []

    with httpx.Client(base_url=base_url, timeout=10.0) as client:
        for _ in range(request_count):
            start_time = time.perf_counter()

            response = client.get("/health")

            elapsed_ms = (time.perf_counter() - start_time) * 1000
            latencies_ms.append(elapsed_ms)

            if response.status_code < 400:
                success_count += 1
            else:
                error_count += 1

    latencies_ms.sort()

    p95_index = max(
        0,
        int(len(latencies_ms) * 0.95) - 1,
    )

    p95_latency_ms = latencies_ms[p95_index]

    error_rate = error_count / request_count

    return {
        "request_count": request_count,
        "success_count": success_count,
        "error_count": error_count,
        "error_rate": error_rate,
        "p95_latency_ms": p95_latency_ms,
    }