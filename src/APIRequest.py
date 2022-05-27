import requests


class APIRequest:

    def __init__(self, sockshop):
        self.sockshop = sockshop

    def makeRequest(self, requestParam):
        try:
            response = requests.get(self.sockshop + requestParam)
            responseJson = response.json()
            if requestParam == "tags":
                answer = responseJson["tags"]
            elif requestParam == "catalogue":
                answer = []
                for element in responseJson:
                    jsonLine = "id:" + element["id"] + ",name:" + element["name"] + ",description:" + element["description"] \
                           + ",price:" + str(element["price"]) + ",count:" + str(element["count"]) + ","
                    answer.append(jsonLine)
            else:
                answer = responseJson
        except Exception as e:
            print(e)
            answer = [0]

        return answer
