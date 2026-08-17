import requests

# 1. Define target URL and payload
url = "http://localhost:5000/push-notifications"
payload = {"password":"asjkdhiwuasdiwuahisdbjiwg8u1872y3iqujwe72yqwjbd278etwdb","title": "test", "body": "test"}

# 2. Make the POST request using the json parameter
response = requests.post(url, json=payload)

# 3. Handle the response
print(f"Status Code: {response.status_code}")
print(response.json())  # Parse response body as JSON
