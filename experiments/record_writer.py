from pathlib import Path

from experiments.record_model import ExperimentRecord


RECORDS_FILE = Path(__file__).resolve().parent / "records.jsonl"


def save_record(record: ExperimentRecord) -> None:
    with RECORDS_FILE.open("a", encoding="utf-8") as file:
        file.write(record.to_json_line() + "\n")