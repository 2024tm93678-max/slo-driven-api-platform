import json

from experiments.record_model import ExperimentRecord
from experiments.record_writer import save_record


def test_experiment_record_contains_required_fields():
    record = ExperimentRecord.create(
        experiment_id="EXP-001",
        arm="treatment",
        fault_scenario="elevated_latency",
        request_count=1000,
        error_count=5,
        error_rate=0.005,
        p95_latency_ms=250,
        slo_pass=True,
        rollback_triggered=False,
    )

    data = json.loads(record.to_json_line())

    assert data["experiment_id"] == "EXP-001"
    assert data["arm"] == "treatment"
    assert data["fault_scenario"] == "elevated_latency"
    assert data["request_count"] == 1000
    assert data["error_count"] == 5
    assert data["error_rate"] == 0.005
    assert data["p95_latency_ms"] == 250
    assert data["slo_pass"] is True
    assert data["rollback_triggered"] is False
    assert "timestamp_utc" in data


def test_save_record_writes_json_line(tmp_path, monkeypatch):
    record = ExperimentRecord.create(
        experiment_id="EXP-002",
        arm="control",
        fault_scenario="healthy",
        request_count=500,
        error_count=0,
        error_rate=0.0,
        p95_latency_ms=120,
        slo_pass=True,
        rollback_triggered=False,
    )

    test_file = tmp_path / "records.jsonl"

    monkeypatch.setattr(
        "experiments.record_writer.RECORDS_FILE",
        test_file,
    )

    save_record(record)

    lines = test_file.read_text(encoding="utf-8").splitlines()

    assert len(lines) == 1

    data = json.loads(lines[0])

    assert data["experiment_id"] == "EXP-002"
    assert data["arm"] == "control"
    assert data["fault_scenario"] == "healthy"