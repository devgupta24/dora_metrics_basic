import pandas as pd
import json
from datetime import datetime, timezone

# -----------------------------------
# SAMPLE ETL DATA
# -----------------------------------

data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Amount": [100, 200, 300]
}

# -----------------------------------
# CREATE DATAFRAME
# -----------------------------------

df = pd.DataFrame(data)

print(df)

# -----------------------------------
# LOAD METRICS FILE
# -----------------------------------

try:

    with open("metrics.json") as f:
        metrics = json.load(f)

except:

    metrics = {
        "etl_runs": [],
        "validation_failures": [],
        "dag_failures": [],
        "schema_changes": []
    }

# -----------------------------------
# ETL EVENT
# -----------------------------------

etl_event = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "rows_processed": len(df),
    "status": "success"
}

metrics["etl_runs"].append(etl_event)

# -----------------------------------
# SAMPLE VALIDATION FAILURE
# -----------------------------------

validation_event = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "failed_records": 2
}

metrics["validation_failures"].append(validation_event)

# -----------------------------------
# SAMPLE DAG FAILURE
# -----------------------------------

dag_failure = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "recovery_minutes": 15
}

metrics["dag_failures"].append(dag_failure)

# -----------------------------------
# SAMPLE SCHEMA CHANGE
# -----------------------------------

schema_change = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "contract_break": False
}

metrics["schema_changes"].append(schema_change)

# -----------------------------------
# SAVE METRICS
# -----------------------------------

with open("metrics.json", "w") as f:

    json.dump(metrics, f, indent=2)

print("ETL observability metrics updated successfully")