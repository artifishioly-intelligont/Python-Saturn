import requests
import json

def post_request(url, payload):
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    r = requests.post(url , json=payload, headers=headers)
    print(r.url)
    return r.text