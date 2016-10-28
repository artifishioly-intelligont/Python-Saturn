import unittest
from Perceptron import Perceptron

input_length = 6
number_of_training_vectors = 50


class PerceptronTest(unittest.TestCase):

    def setUp(self):
        per = Perceptron(input_length)


    def test_weightsDontChangeWithPredict(self):
        """
            Test to see that the perceptron does not change the weights when predicting

            Method Under Test: Perceptron.Perceptron.predict()
        """
        # GIVEN a perceptron
        per = Perceptron(input_length)

        # AND the it's weights
        before_weights = per.weights[:]

        # AND a list of attributes
        list = [0.5]*input_length

        #
        # WHEN predicting the class for the list of attributes
        per.predict(list)

        #
        # THEN the weights do not change
        after_weights = per.weights[:]
        self.assertEqual(before_weights, after_weights, 'The weights should not change after predicting a class')

    def test_weightsDoChangeWithFeedback(self):
        """
            Test to see that the perceptron changes the weights after feedback

            Method Under Test: Perceptron.Perceptron.feedback()
        """
        # GIVEN a perceptron
        per = Perceptron(input_length)

        # AND the it's weights
        before_weights = per.weights[:]

        # AND a list of attributes
        list = [0.5]*input_length

        # AND some 'true result' for the prediction
        true_value = 999999

        #
        # WHEN predicting the class for the list of attributes
        pred_value = per.predict(list)

        # AND giving feedback
        per.feedback(true_value, pred_value, list)

        #
        # THEN the weights do not change
        after_weights = per.weights[:]
        self.assertNotEqual(before_weights, after_weights, 'The weights should change after recieving feedback (before: %s, after: %s)' % (str(before_weights), str(after_weights)))


if __name__ == '__main__':
    unittest.main()