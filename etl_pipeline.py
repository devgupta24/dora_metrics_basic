import pandas as pd
import json
from datetime import datetime, timezone

# Sample ETL data
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Amount": [100, 200, 300]
}

df = pd.DataFrame(data)

print(df)

rows_processed = len(df)

etl_event = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "rows_processed": rows_processed,
    "status": "success"
}

# Load metrics file
try:
    with open("metrics.json") as f:
        metrics = json.load(f)

except:
    metrics = {
        "deployments": [],
        "incidents": [],
        "etl_runs": []
    }

# Append ETL run
metrics["etl_runs"].append(etl_event)

# Save metrics
with open("metrics.json", "w") as f:
    json.dump(metrics, f, indent=2)

print("ETL metrics updated successfully")