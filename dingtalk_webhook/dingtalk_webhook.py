import requests
import json
import hmac
import hashlib
import base64
import time
from urllib.parse import quote_plus

def initWebhook(cmdWebhook, cmdSecret, cmdAtUserPhone):
    global webhook, secret, atUserPhone
    webhook = cmdWebhook
    secret = cmdSecret
    atUserPhone = cmdAtUserPhone

def generate_signature(secret):
    timestamp = str(round(time.time() * 1000))
    string_to_sign = f'{timestamp}\n{secret}'
    hmac_code = hmac.new(secret.encode('utf-8'), string_to_sign.encode('utf-8'), digestmod=hashlib.sha256).digest()
    signature = quote_plus(base64.b64encode(hmac_code))
    return timestamp, signature

def send_message(message):
    global webhook, secret, atUserPhone
    timestamp, signature = generate_signature(secret)
    webhook += f'&timestamp={timestamp}&sign={signature}'
    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "text",
        "text": {
            "content": message + "\n@{atUserPhone}".format(atUserPhone=atUserPhone)
        },
        "at": {"atMobiles": [atUserPhone],"isAtAll": False}
    }
    response = requests.post(webhook, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        raise ValueError(f"Request to DingTalk bot failed: {response.status_code}, {response.text}")