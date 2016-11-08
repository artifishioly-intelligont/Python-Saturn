import requests
import json

def post_request(url, package):
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    payload = {'key1': package}

    r = requests.post(url , json=payload, headers=headers)
    print(r.url)
    return r.text
