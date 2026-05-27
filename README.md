| Metric                     | Meaning                        |
| -------------------------- | ------------------------------ |
| Data Freshness SLA         | Latest successful pipeline run |
| Pipeline Reliability       | Success rate of ETL runs       |
| Data Quality Incident Rate | Validation failures            |
| Failed DAG Recovery Time   | Recovery after failure         |
| Data Contract Stability    | Schema consistency             |


{
  "etl_runs": [],
  "validation_failures": [],
  "dag_failures": [],
  "schema_changes": []
}