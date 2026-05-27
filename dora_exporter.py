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
    'Average lead time'
)

CFR = Gauge(
    'dora_change_failure_rate_percent',
    'Change failure rate'
)

MTTR = Gauge(
    'dora_mttr_minutes',
    'Mean time to recovery'
)

TOTAL_DEPLOYS = Gauge(
    'dora_total_deployments',
    'Total deployments'
)

# -----------------------------------
# ENGINEERING METRICS
# -----------------------------------

PR_CYCLE_TIME = Gauge(
    'engineering_pr_cycle_time_hours',
    'PR cycle time'
)

BUILD_SUCCESS_RATE = Gauge(
    'engineering_build_success_rate_percent',
    'Build success rate'
)

TEST_COVERAGE = Gauge(
    'engineering_test_coverage_percent',
    'Test coverage'
)

CODE_REVIEW_TIME = Gauge(
    'engineering_code_review_time_hours',
    'Code review duration'
)

RELEASE_VELOCITY = Gauge(
    'engineering_release_velocity',
    'Deployments per week'
)

DEFECT_LEAKAGE = Gauge(
    'engineering_defect_leakage',
    'Production defects'
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
            "incidents": [],
            "pull_requests": [],
            "builds": [],
            "defects": []
        }

# -----------------------------------
# MAIN LOOP
# -----------------------------------

def run():

    print("=" * 60)
    print("Starting DORA + Engineering Metrics Exporter")
    print("Metrics endpoint: http://localhost:8001/metrics")
    print("=" * 60)

    start_http_server(8001)

    while True:

        data = load_metrics()

        deployments = data.get("deployments", [])
        incidents = data.get("incidents", [])
        prs = data.get("pull_requests", [])
        builds = data.get("builds", [])
        defects = data.get("defects", [])

        # -----------------------------------
        # DORA METRICS
        # -----------------------------------

        # Deployment Frequency

        deploy_freq = round(
            len(deployments) / 7,
            2
        )

        # Lead Time

        lead_times = [
            d["lead_time_hours"]
            for d in deployments
            if "lead_time_hours" in d
        ]

        avg_lead_time = (
            round(
                sum(lead_times) / len(lead_times),
                2
            )
            if lead_times else 0
        )

        # Change Failure Rate

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

        # MTTR

        mttr_values = [
            i["mttr_minutes"]
            for i in incidents
        ]

        avg_mttr = (
            round(
                sum(mttr_values) / len(mttr_values),
                2
            )
            if mttr_values else 0
        )

        # -----------------------------------
        # ENGINEERING METRICS
        # -----------------------------------

        # PR Cycle Time

        pr_cycle = [
            p["merged_hours"] - p["created_hours"]
            for p in prs
        ]

        avg_pr_cycle = (
            round(
                sum(pr_cycle) / len(pr_cycle),
                2
            )
            if pr_cycle else 0
        )

        # Build Success Rate

        success_builds = [
            b for b in builds
            if b["status"] == "success"
        ]

        build_rate = (
            round(
                len(success_builds) / len(builds) * 100,
                2
            )
            if builds else 0
        )

        # Code Review Time

        review_times = [
            p["review_hours"]
            for p in prs
        ]

        avg_review = (
            round(
                sum(review_times) / len(review_times),
                2
            )
            if review_times else 0
        )

        # Release Velocity

        release_velocity = len(deployments)

        # Defect Leakage

        defect_leakage = len(defects)

        # -----------------------------------
        # SET PROMETHEUS METRICS
        # -----------------------------------

        DEPLOY_FREQ.set(deploy_freq)

        LEAD_TIME.set(avg_lead_time)

        CFR.set(cfr)

        MTTR.set(avg_mttr)

        TOTAL_DEPLOYS.set(len(deployments))

        PR_CYCLE_TIME.set(avg_pr_cycle)

        BUILD_SUCCESS_RATE.set(build_rate)

        TEST_COVERAGE.set(85)

        CODE_REVIEW_TIME.set(avg_review)

        RELEASE_VELOCITY.set(release_velocity)

        DEFECT_LEAKAGE.set(defect_leakage)

        # -----------------------------------
        # LOG OUTPUT
        # -----------------------------------

        print(
            f"DeployFreq={deploy_freq}/day | "
            f"LeadTime={avg_lead_time}h | "
            f"CFR={cfr}% | "
            f"MTTR={avg_mttr}min | "
            f"PRCycle={avg_pr_cycle}h | "
            f"BuildSuccess={build_rate}% | "
            f"ReviewTime={avg_review}h | "
            f"ReleaseVelocity={release_velocity} | "
            f"DefectLeakage={defect_leakage}"
        )

        time.sleep(15)

# -----------------------------------
# START EXPORTER
# -----------------------------------

if __name__ == "__main__":
    run()