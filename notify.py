import requests
from config import WEBEX_TOKEN, WEBEX_ROOM_ID

def notify(message):
    url = "https://webexapis.com/v1/messages"
    headers = {"Authorization": WEBEX_TOKEN}  # config.py should already have "Bearer ..." in the token
    
    data = {
        "roomId": WEBEX_ROOM_ID,
        "text": message
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        print("Webex status:", response.status_code)
        print("Webex response:", response.text)
    except Exception as e:
        print("Error sending Webex message:", e)
