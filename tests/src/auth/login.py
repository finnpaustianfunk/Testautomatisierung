import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://apiv2.emil.de/authservice/v1/login"

# change payload if needed
payload = {
    "username": os.getenv("EMIL_USERNAME"),
    "password": os.getenv("EMIL_PASSWORD")
}
headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers, verify=False)

print(response.text)