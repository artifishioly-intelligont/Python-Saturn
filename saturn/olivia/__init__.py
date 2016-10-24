from vectorizer import Vectorizer

vec = Vectorizer()

def get_attr_vec(local_image_loc):
        # type: String -> Array<String>
        return vec.get_attribute_vector(local_image_loc)
