import json
import time
from prometheus_client import start_http_server, Gauge

# -----------------------------------
# OPERATIONAL METRICS
# -----------------------------------

SYSTEM_HEALTH = Gauge(
    'runtime_system_health_percent',
    'Runtime system health'
)

RELIABILITY = Gauge(
    'runtime_reliability_percent',
    'Runtime reliability'
)

AVAILABILITY = Gauge(
    'runtime_availability_percent',
    'Availability'
)

SLA_ADHERENCE = Gauge(
    'runtime_sla_adherence_percent',
    'SLA adherence'
)

PRODUCTION_STABILITY = Gauge(
    'production_stability_percent',
    'Production stability'
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
    print("Starting Operational Metrics Exporter")
    print("Metrics endpoint: http://localhost:8001/metrics")
    print("=" * 60)

    start_http_server(8001)

    while True:

        data = load_metrics()

        system_health = data.get("system_health", [])
        runtime_events = data.get("runtime_events", [])
        sla_events = data.get("sla_events", [])
        production_failures = data.get("production_failures", [])

        # -----------------------------------
        # Runtime System Health
        # -----------------------------------

        avg_cpu = (
            sum(x["cpu_usage"] for x in system_health)
            / len(system_health)
            if system_health else 0
        )

        health_score = round(100 - avg_cpu, 2)

        # -----------------------------------
        # Reliability
        # -----------------------------------

        success_runs = [
            x for x in runtime_events
            if x["status"] == "success"
        ]

        reliability = (
            round(
                len(success_runs) / len(runtime_events) * 100,
                2
            )
            if runtime_events else 0
        )

        # -----------------------------------
        # Availability
        # -----------------------------------

        availability = reliability

        # -----------------------------------
        # SLA Adherence
        # -----------------------------------

        sla_success = [
            x for x in sla_events
            if x["sla_met"] is True
        ]

        sla_score = (
            round(
                len(sla_success) / len(sla_events) * 100,
                2
            )
            if sla_events else 0
        )

        # -----------------------------------
        # Production Stability
        # -----------------------------------

        high_failures = [
            x for x in production_failures
            if x["severity"] == "high"
        ]

        stability = (
            round(
                100 - (
                    len(high_failures)
                    / len(production_failures)
                    * 100
                ),
                2
            )
            if production_failures else 100
        )

        # -----------------------------------
        # SET METRICS
        # -----------------------------------

        SYSTEM_HEALTH.set(health_score)

        RELIABILITY.set(reliability)

        AVAILABILITY.set(availability)

        SLA_ADHERENCE.set(sla_score)

        PRODUCTION_STABILITY.set(stability)

        print(
            f"Health={health_score}% | "
            f"Reliability={reliability}% | "
            f"Availability={availability}% | "
            f"SLA={sla_score}% | "
            f"Stability={stability}%"
        )

        time.sleep(15)

# -----------------------------------
# START EXPORTER
# -----------------------------------

if __name__ == "__main__":
    run()