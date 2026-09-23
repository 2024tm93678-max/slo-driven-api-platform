from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json


@dataclass
class ExperimentRecord:
    experiment_id: str
    timestamp_utc: str
    arm: str
    fault_scenario: str
    request_count: int
    error_count: int
    error_rate: float
    p95_latency_ms: float
    slo_pass: bool
    rollback_triggered: bool

    @classmethod
    def create(
        cls,
        experiment_id: str,
        arm: str,
        fault_scenario: str,
        request_count: int,
        error_count: int,
        error_rate: float,
        p95_latency_ms: float,
        slo_pass: bool,
        rollback_triggered: bool,
    ):
        return cls(
            experiment_id=experiment_id,
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            arm=arm,
            fault_scenario=fault_scenario,
            request_count=request_count,
            error_count=error_count,
            error_rate=error_rate,
            p95_latency_ms=p95_latency_ms,
            slo_pass=slo_pass,
            rollback_triggered=rollback_triggered,
        )

    def to_json_line(self) -> str:
        return json.dumps(asdict(self))