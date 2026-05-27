# dora_metrics_basic

python generate_event.py --type deploy --status success --lead-time 5.2

python generate_event.py --type deploy --status success --lead-time 6.1

python generate_event.py --type deploy --status failed --lead-time 3.2

python generate_event.py --type deploy --status success --lead-time 7.5


python generate_event.py --type incident --mttr 35

pip install prometheus_client

python dora_exporter.py

curl localhost:8001/metrics

wget https://github.com/prometheus/prometheus/releases/download/v2.51.0/prometheus-2.51.0.linux-amd64.tar.gz

tar xvf prometheus-2.51.0.linux-amd64.tar.gz

cd prometheus-2.51.0.linux-amd64

ls
cp ../prometheus.yml .

./prometheus --config.file=prometheus.yml

