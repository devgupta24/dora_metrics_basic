import json
import random
from datetime import datetime, timezone

# -----------------------------------
# LOAD METRICS FILE
# -----------------------------------

try:

    with open("metrics.json") as f:
        metrics = json.load(f)

except:

    metrics = {
        "system_health": [],
        "runtime_events": [],
        "sla_events": [],
        "production_failures": []
    }

timestamp = datetime.now(timezone.utc).isoformat()

# -----------------------------------
# SYSTEM HEALTH
# -----------------------------------

health_event = {
    "timestamp": timestamp,
    "cpu_usage": random.randint(20, 80),
    "memory_usage": random.randint(30, 85),
    "status": "healthy"
}

metrics["system_health"].append(health_event)

# -----------------------------------
# RUNTIME EVENT
# -----------------------------------

runtime_event = {
    "timestamp": timestamp,
    "status": random.choice(["success", "success", "success", "failed"])
}

metrics["runtime_events"].append(runtime_event)

# -----------------------------------
# SLA EVENT
# -----------------------------------

sla_event = {
    "timestamp": timestamp,
    "sla_met": random.choice([True, True, True, False])
}

metrics["sla_events"].append(sla_event)

# -----------------------------------
# PRODUCTION FAILURE
# -----------------------------------

failure_event = {
    "timestamp": timestamp,
    "severity": random.choice(["low", "medium", "high"])
}

metrics["production_failures"].append(failure_event)

# -----------------------------------
# SAVE METRICS
# -----------------------------------

with open("metrics.json", "w") as f:

    json.dump(metrics, f, indent=2)

print("Operational metrics updated successfully")