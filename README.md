# Flussonic exporter
Prometheus exporter for Flussonic media server

## requirements
apt install python3-prometheus-client python3-requests

## Config

```
{
    "flussonic_servers": [
             "flussonic1.example.net",
             "flussonic2.example.net"
    ],
    "login": "admin",
    "password": "password"
}

```
## Prometheus
```
  - job_name: 'flussonic'
    metrics_path: /metrics
    scrape_interval: 60s
    static_configs:
            - targets: [ 'localhost:9228']

```

## TODO:
