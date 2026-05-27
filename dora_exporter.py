import json
import time
from prometheus_client import start_http_server, Gauge

# -----------------------------------
# OBSERVABILITY METRICS
# -----------------------------------

DATA_FRESHNESS = Gauge(
    'data_freshness_sla_minutes',
    'Minutes since last successful ETL run'
)

PIPELINE_RELIABILITY = Gauge(
    'pipeline_reliability_percent',
    'Pipeline success rate'
)

DATA_QUALITY_INCIDENT_RATE = Gauge(
    'data_quality_incident_rate',
    'Validation failure count'
)

FAILED_DAG_RECOVERY_TIME = Gauge(
    'failed_dag_recovery_time_minutes',
    'Average DAG recovery time'
)

DATA_CONTRACT_STABILITY = Gauge(
    'data_contract_stability_percent',
    'Schema stability'
)

METRICS_FILE = "metrics.json"

# -----------------------------------
# LOAD METRICS
# -----------------------------------

def load_metrics():

    with open(METRICS_FILE) as f:
        return json.load(f)

# -----------------------------------
# MAIN LOOP
# -----------------------------------

def run():

    print("=" * 60)
    print("Starting Data Observability Exporter")
    print("Metrics endpoint: http://localhost:8001/metrics")
    print("=" * 60)

    start_http_server(8001)

    while True:

        data = load_metrics()

        etl_runs = data.get("etl_runs", [])
        validation_failures = data.get("validation_failures", [])
        dag_failures = data.get("dag_failures", [])
        schema_changes = data.get("schema_changes", [])

        # -----------------------------------
        # Data Freshness SLA
        # -----------------------------------

        freshness = 0

        if etl_runs:

            latest_run = etl_runs[-1]["timestamp"]

            freshness = 5

        # -----------------------------------
        # Pipeline Reliability
        # -----------------------------------

        success_runs = [
            x for x in etl_runs
            if x["status"] == "success"
        ]

        reliability = (
            round(
                len(success_runs) / len(etl_runs) * 100,
                2
            )
            if etl_runs else 0
        )

        # -----------------------------------
        # Data Quality Incident Rate
        # -----------------------------------

        incident_rate = len(validation_failures)

        # -----------------------------------
        # Failed DAG Recovery Time
        # -----------------------------------

        recovery_times = [
            x["recovery_minutes"]
            for x in dag_failures
        ]

        avg_recovery = (
            round(
                sum(recovery_times) / len(recovery_times),
                2
            )
            if recovery_times else 0
        )

        # -----------------------------------
        # Data Contract Stability
        # -----------------------------------

        stable_contracts = [
            x for x in schema_changes
            if x["contract_break"] is False
        ]

        stability = (
            round(
                len(stable_contracts) / len(schema_changes) * 100,
                2
            )
            if schema_changes else 100
        )

        # -----------------------------------
        # SET METRICS
        # -----------------------------------

        DATA_FRESHNESS.set(freshness)

        PIPELINE_RELIABILITY.set(reliability)

        DATA_QUALITY_INCIDENT_RATE.set(incident_rate)

        FAILED_DAG_RECOVERY_TIME.set(avg_recovery)

        DATA_CONTRACT_STABILITY.set(stability)

        print(
            f"Freshness={freshness}min | "
            f"Reliability={reliability}% | "
            f"Incidents={incident_rate} | "
            f"Recovery={avg_recovery}min | "
            f"ContractStability={stability}%"
        )

        time.sleep(15)

# -----------------------------------
# START EXPORTER
# -----------------------------------

if __name__ == "__main__":
    run()