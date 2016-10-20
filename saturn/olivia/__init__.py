from vectorizer import Vectorizer

vec = Vectorizer(layer=-1)

def get_attr_vec(local_image_loc):
        # type: (String) -> String
        return vec.get_attribute_vector(local_image_loc)
