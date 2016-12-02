import requests
import json

def post_request(url, payload):
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    r = requests.post(url , json=payload, headers=headers)
    print(r.url)
    return r.json()
    
def get_request(url):
    r = requests.get(url)
    print(r.url)
    return r.json()