docker run -d -p 8086:8086 -v influxdb_data:/var/lib/influxdb influxdb:1.8
docker run -d -p 3000:3000 -v grafana_data:/var/lib/grafana grafana/grafana
