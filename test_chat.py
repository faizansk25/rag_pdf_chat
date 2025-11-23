import requests
import json

url = "http://127.0.0.1:8001/chat"
payload = {
    "question": "What is this document about?",
    "chat_history": []
}
headers = {
    "Content-Type": "application/json"
}

try:
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response Text: {response.text}")
except Exception as e:
    print(f"Error: {e}")
