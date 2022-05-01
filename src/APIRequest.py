import requests


class APIRequest:

    def __init__(self, sockshop):
        self.sockshop = sockshop

    def makeRequest(self, requestParam):
        response = requests.get(self.sockshop + requestParam)
        responseJson = response.json()
        if requestParam == "tags":
            answer = responseJson["tags"]
        else:
            for element in responseJson:
                print(element)
            answer = responseJson

        return answer
