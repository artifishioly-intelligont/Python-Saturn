import unittest
from vectorizer import Vectorizer
import os


default_prm_path = os.path.expanduser('~')+'/SaturnServer/Googlenet_791113_192patch.prm'

image_loc =  os.path.expanduser('~')+'/SaturnServer/test_resources/windmill.jpg'

class VectorizerTest(unittest.TestCase):

    def test_regression__vectorizer_layer_minus_one_behaves_same(self):
        # GIVEN a layer to test
        layer_under_test = -1

        # AND a vectorizer that uses that layer
        vec = Vectorizer(layer=layer_under_test, prm_path=default_prm_path)

        # AND an expected output
        expected_output = []

        #
        # WHEN extracting the attributes from an image
        actual_output = vec.get_attribute_vector(image_loc)

        #
        # THEN the output is as expected
        self.assertEqual(expected_output, actual_output, 'The output %s, does not match the expected output of %s' % (str(actual_output), str(expected_output)))




if __name__ == '__main__':
    unittest.main()