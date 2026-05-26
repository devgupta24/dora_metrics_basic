import json
import time
from datetime import datetime, timezone
from prometheus_client import start_http_server, Gauge

# -------------------------------
# Prometheus Metrics
# -------------------------------

DEPLOY_FREQ = Gauge(
    'dora_deploy_frequency_per_day',
    'Deployments per day'
)

LEAD_TIME = Gauge(
    'dora_lead_time_hours',
    'Average lead time in hours'
)

CFR = Gauge(
    'dora_change_failure_rate_percent',
    'Change failure rate percentage'
)

MTTR = Gauge(
    'dora_mttr_minutes',
    'Mean time to recovery'
)

TOTAL_DEPLOYS = Gauge(
    'dora_total_deployments',
    'Total deployments'
)

ETL_ROWS = Gauge(
    'dora_etl_pipeline_rows_processed',
    'ETL rows processed'
)

METRICS_FILE = "metrics.json"

# -------------------------------
# Load metrics.json
# -------------------------------

def load_metrics():

    try:
        with open(METRICS_FILE) as f:
            return json.load(f)

    except FileNotFoundError:

        return {
            "deployments": [],
            "incidents": [],
            "etl_runs": []
        }

# -------------------------------
# Calculate Metrics
# -------------------------------

def calculate_metrics(data):

    deployments = data.get("deployments", [])
    incidents = data.get("incidents", [])
    etl_runs = data.get("etl_runs", [])

    # Deployment Frequency
    deploy_freq = round(len(deployments) / 7, 2)

    # Lead Time
    lead_times = [
        d["lead_time_hours"]
        for d in deployments
        if "lead_time_hours" in d
    ]

    avg_lead_time = (
        round(sum(lead_times) / len(lead_times), 2)
        if lead_times else 0
    )

    # CFR
    failed = [
        d for d in deployments
        if d["status"] == "failed"
    ]

    cfr = (
        round((len(failed) / len(deployments)) * 100, 2)
        if deployments else 0
    )

    # MTTR
    mttr_values = [
        i["mttr_minutes"]
        for i in incidents
    ]

    avg_mttr = (
        round(sum(mttr_values) / len(mttr_values), 2)
        if mttr_values else 0
    )

    # ETL Rows
    latest_rows = (
        etl_runs[-1]["rows_processed"]
        if etl_runs else 0
    )

    return (
        deploy_freq,
        avg_lead_time,
        cfr,
        avg_mttr,
        len(deployments),
        latest_rows
    )

# -------------------------------
# Main Loop
# -------------------------------

def run():

    print("Starting DORA Exporter on port 8001")

    start_http_server(8001)

    while True:

        data = load_metrics()

        (
            deploy_freq,
            lead_time,
            cfr,
            mttr,
            total_deploys,
            etl_rows
        ) = calculate_metrics(data)

        DEPLOY_FREQ.set(deploy_freq)
        LEAD_TIME.set(lead_time)
        CFR.set(cfr)
        MTTR.set(mttr)
        TOTAL_DEPLOYS.set(total_deploys)
        ETL_ROWS.set(etl_rows)

        print(
            f"DeployFreq={deploy_freq} | "
            f"LeadTime={lead_time}h | "
            f"CFR={cfr}% | "
            f"MTTR={mttr}min"
        )

        time.sleep(15)

# -------------------------------
# Start Exporter
# -------------------------------

if __name__ == "__main__":
    run()