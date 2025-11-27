import requests
from config import WEBEX_TOKEN

url = "https://webexapis.com/v1/rooms"
headers = {"Authorization": WEBEX_TOKEN}

response = requests.get(url, headers=headers)
print("Status:", response.status_code)
print("Body:", response.text)
