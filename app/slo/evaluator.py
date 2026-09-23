from app.slo.config import (
    ERROR_RATE_THRESHOLD,
    P95_LATENCY_THRESHOLD_MS,
)


def evaluate_slo(error_rate: float, p95_latency_ms: float) -> dict:
    error_rate_pass = error_rate <= ERROR_RATE_THRESHOLD
    latency_pass = p95_latency_ms <= P95_LATENCY_THRESHOLD_MS

    return {
        "error_rate": error_rate,
        "p95_latency_ms": p95_latency_ms,
        "error_rate_pass": error_rate_pass,
        "latency_pass": latency_pass,
        "slo_pass": error_rate_pass and latency_pass,
    }