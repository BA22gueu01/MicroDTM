import requests
import logging
import time

PROMETHEUS = 'http://10.161.2.161:31090/'

print("Start Loop")

while True:
    response =requests.get(PROMETHEUS + '/api/v1/query', params={'query': 'counter_status_200_carts_customerId_items'})
    responseJson = response.json()
    data = responseJson["data"]
    result = data["result"][0]
    values = result["value"]
    print("At time", values[0], "there were", values[1], "successful requests!")
    time.sleep(30)