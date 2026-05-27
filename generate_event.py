import json
import argparse
from datetime import datetime, timezone
from pathlib import Path

METRICS_FILE = Path("metrics.json")

if METRICS_FILE.exists():
    with open(METRICS_FILE) as f:
        data = json.load(f)
else:
    data = {
        "deployments": [],
        "incidents": [],
        "etl_runs": []
    }

parser = argparse.ArgumentParser()

parser.add_argument("--type", required=True)
parser.add_argument("--status")
parser.add_argument("--lead-time", type=float)
parser.add_argument("--mttr", type=float)
parser.add_argument("--rows", type=int)

args = parser.parse_args()

timestamp = datetime.now(timezone.utc).isoformat()

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

elif args.type == "etl":
    data["etl_runs"].append({
        "timestamp": timestamp,
        "rows_processed": args.rows,
        "status": args.status
    })

with open(METRICS_FILE, "w") as f:
    json.dump(data, f, indent=2)

print("Event added successfully.")
