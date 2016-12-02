from tools import pinger
from requests.exceptions import ConnectionError, ConnectTimeout

hostname = "http://localhost:5002"

"""
Sends a list of attribute vectors to the classifier microservice 
to be classified

:param: attr_vecs: A dictionary of string remote_url to a double array, the attribute vector for that image
"""
def guess(attr_vecs):
    url = hostname + "/guess"
    vectors = {'vectors' : attr_vecs}
    
    response = pinger.post_request(url, vectors)

    success = response['success']
    del response['success']
    guesses = response

    return guesses, success
    
    
    
"""
Sends a list of attribute vectors and their true classes to the 
classifier microservice, so it can learn
"""
def learn(attr_vecs, true_classes):
    url = hostname + "/learn"
    data = \
        {
            'vectors': attr_vecs,
            'theme': true_classes
        }

    response = pinger.post_request(url, data)
    success = response['success']
    ready_to_guess = response['ready']
    message = response['message']

    return success, ready_to_guess, message


def get_all_features():
    url = hostname + "/features"
    try:
        response = pinger.get_request(url)
        all_features = response['features']
        success = response['success']

    except (ConnectTimeout, ConnectionError) as ex:
        all_features = {}
        success = False

    return all_features, success

    
def add_new_feature(new_feature):
    url = hostname + "/features/" + new_feature
    try:
        response = pinger.get_request(url)
        success = response['success']
        message = response['message']

    except ConnectTimeout as ex:
        message = "Connection with classifier timed out at {}".format(hostname)
        success = False

    return success, message
