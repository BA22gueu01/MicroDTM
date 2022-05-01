import requests


class APIRequest:

    def __init__(self, sockshop):
        self.sockshop = sockshop

    def makeRequest(self, requestParam):
        response = requests.get(self.sockshop + requestParam)
        responseJson = response.json()
        if requestParam == "tags":
            answer = responseJson["tags"]
        elif requestParam == "catalogue":
            answer = []
            for element in responseJson:
                jsonLine = "id:" + element["id"] + ",name:" + element["name"] + ",description:" + element[description] + ",price:" + element["price"] + ",count:" + element["count"] + ","
                print(jsonLine)
                answer.append(jsonLine)
        else:
            answer = responseJson

        return answer
