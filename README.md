| Panel              | Query                                    |
| ------------------ | ---------------------------------------- |
| PR Cycle Time      | `engineering_pr_cycle_time_hours`        |
| Build Success Rate | `engineering_build_success_rate_percent` |
| Test Coverage      | `engineering_test_coverage_percent`      |
| Code Review Time   | `engineering_code_review_time_hours`     |
| Release Velocity   | `engineering_release_velocity`           |
| Defect Leakage     | `engineering_defect_leakage`             |

{
  "deployments": [],
  "incidents": [],
  "pull_requests": [],
  "builds": [],
  "defects": []
}

python generate_event.py --type pr --created-hours 1 --merged-hours 5 --review-hours 2
python generate_event.py --type build --status success
python generate_event.py --type build --status failed
python generate_event.py --type defect --status critical
python generate_event.py --type deploy --status success --lead-time 5.2
python generate_event.py --type incident --mttr 35

pip install prometheus_client

python dora_exporter.py

curl localhost:8001/metrics

wget https://github.com/prometheus/prometheus/releases/download/v2.51.0/prometheus-2.51.0.linux-amd64.tar.gz

tar xvf prometheus-2.51.0.linux-amd64.tar.gz

cd prometheus-2.51.0.linux-amd64

ls cp ../prometheus.yml .

./prometheus --config.file=prometheus.yml
