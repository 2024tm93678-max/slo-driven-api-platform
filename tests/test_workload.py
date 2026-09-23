from experiments.workload import run_workload


class FakeResponse:
    def __init__(self, status_code: int):
        self.status_code = status_code


class FakeClient:
    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def get(self, path):
        return FakeResponse(200)


def test_run_workload(monkeypatch):
    monkeypatch.setattr(
        "experiments.workload.httpx.Client",
        FakeClient,
    )

    result = run_workload(
        base_url="http://testserver",
        request_count=5,
    )

    assert result["request_count"] == 5
    assert result["success_count"] == 5
    assert result["error_count"] == 0
    assert result["error_rate"] == 0.0
    assert result["p95_latency_ms"] >= 0