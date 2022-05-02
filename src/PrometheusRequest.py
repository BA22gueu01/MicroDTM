import requests


class PrometheusRequest:

    def __init__(self, Prometheus):
        self.PROMETHEUS = Prometheus

    def makeRequest(self, requestParam):

        if requestParam == "uptime":
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query?query=uptime{kubernetes_namespace="sock-shop"}[2h:1h]')
        elif requestParam == "uptime_history":
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query?query=uptime{kubernetes_namespace="sock-shop"}[1d:1h]')

        elif requestParam == "container_spec_cpu_quota":
            # https://github.com/google/cadvisor/issues/2026
            cpuUsageCalculation = 'sum(rate(container_cpu_usage_seconds_total{namespace="sock-shop"}[2h:1h])) by (pod_name, container_name)/' \
                                  'sum(container_spec_cpu_quota{namespace="sock-shop"}/container_spec_cpu_period{namespace="sock-shop"}) by (pod_name, container_name)'
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query', params={'query': cpuUsageCalculation})
        elif requestParam == "container_spec_cpu_quota_history":
            # https://github.com/google/cadvisor/issues/2026
            cpuUsageCalculation = 'sum(rate(container_cpu_usage_seconds_total{namespace="sock-shop"}[1d:1h])) by (pod_name, container_name)/' \
                                    'sum(container_spec_cpu_quota{namespace="sock-shop"}/container_spec_cpu_period{namespace="sock-shop"}) by (pod_name, container_name)'
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query', params={'query': cpuUsageCalculation})

        # https://brian-candler.medium.com/interpreting-prometheus-metrics-for-linux-disk-i-o-utilization-4db53dfedcfc
        elif requestParam == "disk_read":
            diskReadCalculation = 'rate(node_disk_read_time_seconds_total[2h:1h]) / rate(node_disk_reads_completed_total[2h:1h])'
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query', params={'query': diskReadCalculation})
        elif requestParam == "disk_read_history":
            diskReadCalculation = 'rate(node_disk_read_time_seconds_total[1d:1h]) / rate(node_disk_reads_completed_total[1d:1h])'
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query', params={'query': diskReadCalculation})

        elif requestParam == "disk_write":
            diskWriteCalculation = 'rate(node_disk_write_time_seconds_total[2h:1h]) / rate(node_disk_writes_completed_total[2h:1h])'
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query', params={'query': diskWriteCalculation})
        elif requestParam == "disk_write_history":
            diskWriteCalculation = 'rate(node_disk_write_time_seconds_total[1d:1h]) / rate(node_disk_writes_completed_total[1d:1h])'
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query', params={'query': diskWriteCalculation})

        # https://www.tigera.io/learn/guides/prometheus-monitoring/prometheus-metrics/
        elif requestParam == "memory_usage":
            memoryCalculation = 'rate(node_memory_Active_bytes[2h:1h]) / rate(node_memory_MemTotal_bytes[2h:1h])'
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query', params={'query': memoryCalculation})
        elif requestParam == "memory_usage_history":
            memoryCalculation = 'rate(node_memory_Active_bytes[1d:1h]) / rate(node_memory_MemTotal_bytes[1d:1h])'
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query', params={'query': memoryCalculation})

        elif "_history" in requestParam:
            requestParam = requestParam.strip("_history") + '{kubernetes_namespace="sock-shop"}[1d:1h]'
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query', params={'query': requestParam})
        else:
            requestParam = requestParam + '{kubernetes_namespace="sock-shop"}[2h:1h]'
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query', params={'query': requestParam})

        prometheusResponseJson = prometheusResponse.json()
        data = prometheusResponseJson["data"]

        # Check if Prometheus result is empty
        result = []
        if len(data["result"]) == 0:
            result = [0, 0]
            return result
        elif requestParam == "container_spec_cpu_quota" or len(data["result"]) == 1:
            print(data["result"])
            return data["result"]["values"]
        else:
            for results in data["result"]:
                result.append(results["values"])
            return result
            #result = data["result"][0]
            #if requestParam == "uptime":
            #    return result["values"]
            #else:
            #    return result["value"]
