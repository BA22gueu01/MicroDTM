import requests


class APIRequest:

    def __init__(self, sockshop):
        self.sockshop = sockshop

    def makeRequest(self, requestParam):
        answer = requests.get(self.sockshop + requestParam)

        return answer["result"][0]
