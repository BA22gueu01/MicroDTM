import requests


class APIRequest:

    def __init__(self, sockshop):
        self.sockshop = sockshop

    def makeRequest(self, requestParam):
        return requests.get(self.sockshop + requestParam)[1]
