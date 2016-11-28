from tools import pinger

def send_to_olivia(url_list):
    """
    :param url_list: A list of URLs of images on a remote location
    :returns:
        image_vectors dict<string,array<int> > -- Remote URL to vectorized image
        failed_images dict<string,string> -- Remote URL to reason for failure
        success boolean -- if all the images were vectorized
    """
    # url to olivia's micro-service /convert success, image_vectors, failed_images]
    url = "http://localhost:5001/convert"
    data = {'urls' : url_list}
    response = send_to_service(url, data)

    return response['image_vectors'], response['failed_images'], response['success']


def send_to_classifier(url_to_vector_dict):
    """
    :param url_to_vector_dict:
    :returns:
    """
    #send attributes of each tiles to the classifier
    url = "http://localhost:5002/guess"
    return send_to_service(url, url_to_vector_dict)

def send_to_service(service_url, data):
    result = pinger.post_request(service_url, data)
    return result


def type_class(type, image_classes_dict):
    """
    Filter the dictionary to only keep entries with the value of type

    :param type: String -- The type of feature we are looking for
    :param image_classes_dict: dict<String,String> -- Remote URL to type (e.g. 'http://path/to/image.jpg': 'Trees')
    :return:
        filtered_class_dict: dict<String,String> -- Remote URL to type where type = 'type'
    """
    filtered_class_dict = dict(image_classes_dict)

    for k, v in image_classes_dict.items():
        if v != type:
            del filtered_class_dict[k]

    return filtered_class_dict
