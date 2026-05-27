import json
import argparse
from datetime import datetime, timezone
from pathlib import Path

METRICS_FILE = Path("metrics.json")

# -----------------------------------
# LOAD EXISTING METRICS
# -----------------------------------

if METRICS_FILE.exists():

    with open(METRICS_FILE) as f:
        data = json.load(f)

else:

    data = {
        "deployments": [],
        "incidents": [],
        "pull_requests": [],
        "builds": [],
        "defects": []
    }

# -----------------------------------
# ARGUMENT PARSER
# -----------------------------------

parser = argparse.ArgumentParser()

parser.add_argument("--type", required=True)

parser.add_argument("--status")

parser.add_argument("--lead-time", type=float)

parser.add_argument("--mttr", type=float)

# Engineering Metrics

parser.add_argument("--created-hours", type=float)

parser.add_argument("--merged-hours", type=float)

parser.add_argument("--review-hours", type=float)

args = parser.parse_args()

timestamp = datetime.now(timezone.utc).isoformat()

# -----------------------------------
# EVENT TYPES
# -----------------------------------

if args.type == "deploy":

    data["deployments"].append({
        "timestamp": timestamp,
        "status": args.status,
        "lead_time_hours": args.lead_time
    })

elif args.type == "incident":

    data["incidents"].append({
        "timestamp": timestamp,
        "mttr_minutes": args.mttr
    })

elif args.type == "pr":

    data["pull_requests"].append({
        "timestamp": timestamp,
        "created_hours": args.created_hours,
        "merged_hours": args.merged_hours,
        "review_hours": args.review_hours
    })

elif args.type == "build":

    data["builds"].append({
        "timestamp": timestamp,
        "status": args.status
    })

elif args.type == "defect":

    data["defects"].append({
        "timestamp": timestamp,
        "severity": args.status
    })

else:

    print("Invalid event type")

# -----------------------------------
# SAVE METRICS
# -----------------------------------

with open(METRICS_FILE, "w") as f:

    json.dump(data, f, indent=2)

print("Event added successfully")