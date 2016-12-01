from tools import pinger

hostname = "http://localhost:5002"

"""
Sends a list of attribute vectors to the classifier microservice 
to be classified
"""
def guess(attr_vecs):
    url = hostname + "/guess"
    vectors = {'vectors' : attr_vecs}
    
    return pinger.post_request(url, vectors)
    
    
    
"""
Sends a list of attribute vectors and their true classes to the 
classifier microservice, so it can learn
"""
def learn(attr_vecs, true_classes):
    url = hostname + "/learn"
    vectors = {'vectors' : attr_vecs}
    theme = {'theme' : true_classes}
    
    return pinger.post_request(url, vectors, theme)
    

def get_all_features():
    url = hostname + "/features"
    pinger.get_request(url)
    
def add_new_feature(new_feature):
    url = hostname + "/features/" + new_feature
    pinger.get_request(url)