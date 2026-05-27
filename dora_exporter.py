import json
import time
from prometheus_client import start_http_server, Gauge

ETL_ROWS = Gauge(
    'dora_etl_pipeline_rows_processed',
    'Rows processed'
)

PIPELINE_RELIABILITY = Gauge(
    'pipeline_reliability_percent',
    'Pipeline reliability'
)

PIPELINE_FAILURES = Gauge(
    'pipeline_failed_runs',
    'Failed pipeline runs'
)

METRICS_FILE = "metrics.json"

def load_metrics():

    with open(METRICS_FILE) as f:
        return json.load(f)

def calculate_metrics(data):

    etl_runs = data.get("etl_runs", [])

    latest_rows = (
        etl_runs[-1]["rows_processed"]
        if etl_runs else 0
    )

    success_runs = [
        x for x in etl_runs
        if x["status"] == "success"
    ]

    failed_runs = [
        x for x in etl_runs
        if x["status"] == "failed"
    ]

    reliability = (
        round(len(success_runs) / len(etl_runs) * 100, 2)
        if etl_runs else 0
    )

    return (
        latest_rows,
        reliability,
        len(failed_runs)
    )

def run():

    print("Starting exporter on port 8001")

    start_http_server(8001)

    while True:

        data = load_metrics()

        rows, reliability, failed = calculate_metrics(data)

        ETL_ROWS.set(rows)
        PIPELINE_RELIABILITY.set(reliability)
        PIPELINE_FAILURES.set(failed)

        print(
            f"Rows={rows} | "
            f"Reliability={reliability}% | "
            f"FailedRuns={failed}"
        )

        time.sleep(15)

if __name__ == "__main__":
    run()