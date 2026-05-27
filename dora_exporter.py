import json
import time
from prometheus_client import start_http_server, Gauge

# -----------------------------------
# DORA METRICS
# -----------------------------------

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

METRICS_FILE = "metrics.json"

# -----------------------------------
# LOAD METRICS
# -----------------------------------

def load_metrics():

    try:
        with open(METRICS_FILE) as f:
            return json.load(f)

    except FileNotFoundError:

        return {
            "deployments": [],
            "incidents": []
        }

# -----------------------------------
# CALCULATE DORA METRICS
# -----------------------------------

def calculate_metrics(data):

    deployments = data.get("deployments", [])
    incidents = data.get("incidents", [])

    # 1. Deployment Frequency
    deploy_freq = round(len(deployments) / 7, 2)

    # 2. Lead Time
    lead_times = [
        d["lead_time_hours"]
        for d in deployments
        if "lead_time_hours" in d
    ]

    avg_lead_time = (
        round(sum(lead_times) / len(lead_times), 2)
        if lead_times else 0
    )

    # 3. Change Failure Rate
    failed = [
        d for d in deployments
        if d["status"] == "failed"
    ]

    cfr = (
        round(
            (len(failed) / len(deployments)) * 100,
            2
        )
        if deployments else 0
    )

    # 4. MTTR
    mttr_values = [
        i["mttr_minutes"]
        for i in incidents
    ]

    avg_mttr = (
        round(sum(mttr_values) / len(mttr_values), 2)
        if mttr_values else 0
    )

    return (
        deploy_freq,
        avg_lead_time,
        cfr,
        avg_mttr,
        len(deployments)
    )

# -----------------------------------
# MAIN LOOP
# -----------------------------------

def run():

    print("=" * 50)
    print("Starting DORA Exporter on port 8001")
    print("Metrics endpoint: http://localhost:8001/metrics")
    print("=" * 50)

    start_http_server(8001)

    while True:

        data = load_metrics()

        (
            deploy_freq,
            lead_time,
            cfr,
            mttr,
            total_deploys
        ) = calculate_metrics(data)

        DEPLOY_FREQ.set(deploy_freq)
        LEAD_TIME.set(lead_time)
        CFR.set(cfr)
        MTTR.set(mttr)
        TOTAL_DEPLOYS.set(total_deploys)

        print(
            f"DeployFreq={deploy_freq}/day | "
            f"LeadTime={lead_time}h | "
            f"CFR={cfr}% | "
            f"MTTR={mttr}min | "
            f"TotalDeploys={total_deploys}"
        )

        time.sleep(15)

# -----------------------------------
# START EXPORTER
# -----------------------------------

if __name__ == "__main__":
    run()