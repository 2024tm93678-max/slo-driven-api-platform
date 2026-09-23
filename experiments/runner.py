from experiments.record_model import ExperimentRecord
from experiments.record_writer import save_record


def run_experiment():
    record = ExperimentRecord.create(
        experiment_id="EXP-001",
        arm="control",
        fault_scenario="healthy",
        request_count=100,
        error_count=0,
        error_rate=0.0,
        p95_latency_ms=120,
        slo_pass=True,
        rollback_triggered=False,
    )

    save_record(record)

    print("Experiment completed.")
    print(record.to_json_line())


if __name__ == "__main__":
    run_experiment()