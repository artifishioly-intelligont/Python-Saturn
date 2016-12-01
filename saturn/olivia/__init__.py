from tools import pinger

hostname = "http://localhost:5001"

"""
Sends a list of image urls to olivia, which extracts the attribute
vectors of the images and returns them in a list
"""
def get_all_attr_vecs(remote_image_locs):
    
    url = hostname + "/convert"
    data = {'urls' : remote_image_locs}
    response = pinger.post_request(url, data)
    
    return response['image_vectors'], response['failed_images'], response['success']

