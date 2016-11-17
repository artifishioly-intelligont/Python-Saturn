from tools import pinger

def send_to_olivia(url_list):
    # url to olivia's micro-service /convert success, image_vectors, failed_images]
    url = " "
    package = url_list
    
    return pinger.post_request(url , package)

def send_to_classifier(vect_list):
    #send attributes of each tiles to the classifier
    url = ''
    package = vect_list
    
    return pinger.post_request(url, package)


def type_class(type, class_list):
    class_dict = {}

    for k,v in class_list.items():
        if v == type:
            class_dict[k] = v

    return class_dict;