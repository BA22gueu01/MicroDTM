import requests


class PrometheusRequest:

    def __init__(self, Prometheus):
        self.PROMETHEUS = Prometheus

    def makeRequest(self, requestParam):
        instance = "10.161.2.161:9100"
        job = "node-exporter"

        if requestParam == "uptime":
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query?query=uptime[30s:1s]')
        elif requestParam == "container_spec_cpu_quota":
            # https://github.com/google/cadvisor/issues/2026
            cpuUsageCalculation = 'sum(rate(container_cpu_usage_seconds_total{name!~".*prometheus.*", image!="", ' \
                                  'container_name!="POD"}[5m])) by (pod_name, container_name)/' \
                                  'sum(container_spec_cpu_quota{name!~".*prometheus.*", image!="", ' \
                                  'container_name!="POD"}/container_spec_cpu_period{name!~".*prometheus.*", ' \
                                  'image!="", container_name!="POD"}) by (pod_name, container_name)'
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query', params={'query': cpuUsageCalculation})
        # https://brian-candler.medium.com/interpreting-prometheus-metrics-for-linux-disk-i-o-utilization-4db53dfedcfc
        elif requestParam == "disk_read":
            diskReadCalculation = 'rate(node_disk_read_time_seconds_total{instance="' + instance \
                                  + '",job="' + job + '"}[5m]) / rate(node_disk_reads_completed_total{instance="' + \
                                  instance + '",job="' + job + '"}[5m]) '
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query', params={'query': diskReadCalculation})
        elif requestParam == "disk_write":
            diskWriteCalculation = 'rate(node_disk_write_time_seconds_total{instance="' + instance \
                                   + '",job="' + job + '"}[5m]) / rate(node_disk_writes_completed_total{instance="' + \
                                   instance + '",job="' + job + '"}[5m])'
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query', params={'query': diskWriteCalculation})
        # https://www.tigera.io/learn/guides/prometheus-monitoring/prometheus-metrics/
        elif requestParam == "memory_usage":
            memoryCalculation = 'node_memory_Active_bytes{instance="' + instance + '", job="' \
                                + job + '"}/node_memory_MemTotal_bytes{instance="' + instance + '", job="' + job + '"}'
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query', params={'query': memoryCalculation})
        else:
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query', params={'query': requestParam})
        prometheusResponseJson = prometheusResponse.json()
        data = prometheusResponseJson["data"]

        # Check if Prometheus result is empty
        if len(data["result"]) == 0:
            result = [0, 0]
            return result
        else:
            result = data["result"][0]
            if requestParam == "uptime":
                return result["values"]
            else:
                return result["value"]
