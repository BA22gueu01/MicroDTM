import requests


class APIRequest:

    def __init__(self, sockshop):
        self.sockshop = sockshop

    def makeRequest(self, requestParam):
        response = requests.get(self.sockshop + requestParam)
        responseJson = response.json()
        tags = responseJson["tags"]

        return tags
