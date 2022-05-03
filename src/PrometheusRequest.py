import requests


class PrometheusRequest:

    def __init__(self, Prometheus):
        self.PROMETHEUS = Prometheus

    def makeRequest(self, requestParam):

        if requestParam == "uptime":
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query?query=uptime{kubernetes_namespace="sock-shop"}[2h:1h]')
        elif requestParam == "uptime_history":
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query?query=uptime{kubernetes_namespace="sock-shop"}[25h:1h]')

        elif requestParam == "container_spec_cpu_quota":
            # https://github.com/google/cadvisor/issues/2026
            cpuUsageCalculation = 'sum(rate(container_cpu_usage_seconds_total{namespace="sock-shop"}[1d:1h])) by (pod_name, container_name)/sum(container_spec_cpu_quota{namespace="sock-shop"})/sum(container_spec_cpu_period{namespace="sock-shop"}) by (pod_name, container_name)'
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query', params={'query': cpuUsageCalculation})
        elif requestParam == "container_spec_cpu_quota_history":
            # https://github.com/google/cadvisor/issues/2026
            cpuUsageCalculation = 'sum(rate(container_cpu_usage_seconds_total{namespace="sock-shop"}[1d:1h])) by (pod_name, container_name)/sum(container_spec_cpu_quota{namespace="sock-shop"})/sum(container_spec_cpu_period{namespace="sock-shop"}) by (pod_name, container_name)'
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query', params={'query': cpuUsageCalculation})

        # https://brian-candler.medium.com/interpreting-prometheus-metrics-for-linux-disk-i-o-utilization-4db53dfedcfc
        elif requestParam == "disk_read":
            diskReadCalculation = '(node_disk_read_time_seconds_total / node_disk_reads_completed_total)[2h:1h]'
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query', params={'query': diskReadCalculation})
        elif requestParam == "disk_read_history":
            diskReadCalculation = '(node_disk_read_time_seconds_total / node_disk_reads_completed_total)[25h:1h]'
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query', params={'query': diskReadCalculation})

        elif requestParam == "disk_write":
            diskWriteCalculation = '(node_disk_write_time_seconds_total / node_disk_writes_completed_total)[2h:1h]'
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query', params={'query': diskWriteCalculation})
        elif requestParam == "disk_write_history":
            diskWriteCalculation = '(node_disk_write_time_seconds_total / node_disk_writes_completed_total)[25h:1h]'
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query', params={'query': diskWriteCalculation})

        # https://www.tigera.io/learn/guides/prometheus-monitoring/prometheus-metrics/
        elif requestParam == "memory_usage":
            memoryCalculation = '(node_memory_Active_bytes/ node_memory_MemTotal_bytes)[2h:1h]'
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query', params={'query': memoryCalculation})
        elif requestParam == "memory_usage_history":
            memoryCalculation = '(node_memory_Active_bytes/ node_memory_MemTotal_bytes)[1d:1h]'
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query', params={'query': memoryCalculation})

        elif requestParam == "response_time":
            responseCalculation = '(http_request_duration_seconds_sum{kubernetes_namespace="sock-shop"} / ' \
                    'http_request_duration_seconds_count{kubernetes_namespace="sock-shop"})[2h:1h]'
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query', params={'query': responseCalculation})
        elif requestParam == "response_time_history":
            responseCalculation = '(http_request_duration_seconds_sum{kubernetes_namespace="sock-shop"} / ' \
                    'http_request_duration_seconds_count{kubernetes_namespace="sock-shop"})[1d:1h]'
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query', params={'query': responseCalculation})

        elif "_history" in requestParam:
            requestParam = requestParam.replace("_history", "") + '{kubernetes_namespace="sock-shop"}[25h:1h]'
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
        elif len(data["result"]) == 1:
            for results in data["result"]:
                if "values" in results:
                    return results["values"]
                else:
                    return results["value"]
        else:
            for results in data["result"]:
                if "values" in results:
                    result.append(results["values"])
                else:
                    result.append(results["value"])
                return result

