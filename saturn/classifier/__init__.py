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
    

    try:
        response = pinger.post_request(url, vectors)

        success = response['success']
        del response['success']
        guesses = response
        failed_images = {}
    
    except ConnectionError as ex:
        success = False
        guesses = {}
        failed_images = {img_url: "Cannot establish a connection with Classifier at {} endpoint".format(url) for img_url in attr_vecs.keys()}

    return guesses, success, failed_images



    
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

    try:
        response = pinger.post_request(url, data)
        success = response['success']
        ready_to_guess = response['ready']
        message = response['message']
        failed_images = {}
        
    except ConnectionError as ex:
        success = False
        ready_to_guess = False
        message = "Cannot establish a connection with Classifier at {} endpoint".format(url)
        failed_images = {img_url: "Cannot establish a connection with Classifier at {} endpoint".format(url) for img_url in attr_vecs.keys()}

    return success, ready_to_guess, message, failed_images


def get_all_features():
    url = hostname + "/features"
    try:
        response = pinger.get_request(url)
        all_features = response['features']
        success = response['success']
        message = ""

    except (ConnectTimeout, ConnectionError) as ex:
        all_features = {}
        success = False
        message = "Failed to establish connection to {}".format(hostname)

    return all_features, success, message

    
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
