import os
import requests
from dotenv import load_dotenv

load_dotenv()

endpoint = "https://api.assemblyai.com/v2/transcript"
json = {"audio_url": "https://bit.ly/3yxKEIY"}
headers = {
    "authorization": '160ae1579f6742519930915687ec0ec6',
    "content-type": "application/json",
}
response = requests.post(
    endpoint,
    json=json,
    headers=headers,
)
print(response.json())