import requests

base_url = "http://localhost:8000"

response = requests.get(url=base_url)
print(response)
