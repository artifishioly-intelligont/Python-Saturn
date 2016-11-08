import requests
import json

def post_request(url):
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    url = "http://127.0.0.1:8000/post"
    list_array = [1.2, 2.2, 3.2, 4.2, 5.2]
    payload = {'key1': list_array}

    r = requests.post(url , json=payload, headers=headers)
    print(r.url)
    return r

if __name__ == '__main__':
    #get_request(4567)
    #raw_input('press something to continue to POST')
    post_request("www.something.com")