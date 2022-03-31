import requests  

PROMETHEUS = 'http://10.161.2.161:31090/'

response =requests.get(PROMETHEUS + '/api/v1/query', params={'query': 'counter_status_200_carts_customerId_items'})

print(response)