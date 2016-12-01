from tools import pinger

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
            'feature': true_classes
        }

    response = pinger.post_request(url, data)
    success = response['success']

    return success


def get_all_features():
    url = hostname + "/features"
    response = pinger.get_request(url)

    all_features = response['features']
    success = response['success']

    return all_features, success

    
def add_new_feature(new_feature):
    url = hostname + "/features/" + new_feature
    response = pinger.get_request(url)

    success = response['success']
    message = response['message']

    return success, message
