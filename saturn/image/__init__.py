from tools import pinger

def send_to_olivia(url_list):
    # url to olivia's micro-service /convert success, image_vectors, failed_images]
    url = " "
    package = url_list
    result = pinger.post_request(url , package)

    if result['success']:
        return result['image_vectors']
    else:
        return False

def send_to_classifier(vect_list):
    #send attributes of each tiles to the classifier
    url = ''
    package = vect_list
    result = pinger.post_request(url, package)
    return result


def type_class(type, class_list):
    type_class_list = []

    for k,v in class_list.items():
        if v == type:
            type_class_list.append(k)

    return type_class_list;