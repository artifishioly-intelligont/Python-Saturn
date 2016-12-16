from tools import pinger
from requests.exceptions import ConnectionError, ConnectTimeout

hostname = "http://myrtle.ecs.soton.ac.uk"

"""
Sends a list of image urls to olivia, which extracts the attribute
vectors of the images and returns them in a list
"""
def get_all_attr_vecs(remote_image_locs):
    
    url = hostname + "/convert"
    data = {'urls' : remote_image_locs}
    try:
        response = pinger.post_request(url, data)
        image_vectors = response['image_vectors']
        failed_images = response['failed_images']
        success = response['success']

    except ConnectTimeout as ex:
        image_vectors = {}
        failed_images = {url: "Timeout to connection with Olivia at {}".format(hostname) for url in remote_image_locs}
        success = False
    except ConnectionError as ex:
        image_vectors = {}
        failed_images = {url: "Cannot establish connection with Olivia at {} ".format(hostname) for url in remote_image_locs}
        success = False

    return image_vectors, failed_images, success


"""
Sends a list of image urls to olivia, which extracts the attribute
vectors of the images and returns them in a list
"""


def get_all_attr_vecs_and_nsew(remote_image_locs):
    url = hostname + "/convert/nsew"
    data = {'urls': remote_image_locs}
    try:
        response = pinger.post_request(url, data)
        image_vectors = response['image_vectors']
        failed_images = response['failed_images']
        success = response['success']

    except ConnectTimeout as ex:
        image_vectors = {}
        failed_images = {url: "Timeout to connection with Olivia at {}".format(hostname) for url in remote_image_locs}
        success = False
    except ConnectionError as ex:
        image_vectors = {}
        failed_images = {url: "Cannot establish connection with Olivia at {} ".format(hostname) for url in
                         remote_image_locs}
        success = False

    return image_vectors, failed_images, success

def send_download_urls(payload):
    url = hostname + "/download"
    return pinger.post_request(url, payload)
