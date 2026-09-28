import requests

def send_to_django(data):

    url = "http://127.0.0.1:8000/detection/save-threat/"

    try:
        response = requests.post(url, json=data)
        print("Sent to Django:", response.json())

    except Exception as e:
        print("Error sending to Django:", e)