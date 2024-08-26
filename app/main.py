from utils import * 
import requests
query = 'موزیک جدید'
request_search = generate_search_request(query)
request_search = requests.request(**request_search)
print(request_search)