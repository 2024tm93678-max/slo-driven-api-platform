from app.slo.config import CONSECUTIVE_FAILURES_FOR_ROLLBACK


def should_rollback(consecutive_failures: int) -> bool:
    return consecutive_failures >= CONSECUTIVE_FAILURES_FOR_ROLLBACK