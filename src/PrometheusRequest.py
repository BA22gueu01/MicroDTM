import requests


class PrometheusRequest:

    def __init__(self, Prometheus):
        self.PROMETHEUS = Prometheus

    def makeRequest(self, requestParam):
        if requestParam == "uptime":
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query?query=uptime[30s:1s]')
        elif requestParam == "container_spec_cpu_quota":
            cpuUsageCalculation = 'sum(rate(container_cpu_usage_seconds_total{name!~".*prometheus.*", image!="", ' \
                                  'container_name!="POD"}[5m])) by (pod_name, container_name)/' \
                                  'sum(container_spec_cpu_quota{name!~".*prometheus.*", image!="", ' \
                                  'container_name!="POD"}/container_spec_cpu_period{name!~".*prometheus.*", ' \
                                  'image!="", container_name!="POD"}) by (pod_name, container_name)'
            prometheusResponse = requests.get(self.PROMETHEUS + '/api/v1/query', params={'query': cpuUsageCalculation})
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