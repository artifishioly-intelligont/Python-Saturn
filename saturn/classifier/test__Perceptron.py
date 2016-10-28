import unittest, random
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

    def test_errorRateReducesAfterMultipleFeedbacks(self):
        """
            Test that given a simple problem that the perceptron can learn the solution.

            Methods Under Test: Perceptron.Perceptron.guess() &
                                Perceptron.Perceptron.feedback()
        """
        # GIVEN a perceptron
        per = Perceptron(input_length)

        # AND a true_function that we want the perceptron to learn
        def f_true(x):
            return 10 * x[1] + 100 * x[3] + 1000 * x[5]

        # AND some input data (X) and their true values (Y)
        x = random.sample(range(-20, 20), input_length)
        y = f_true(x)

        #
        # WHEN training the perceptron
        for m in range(number_of_training_vectors):
            p = per.predict(x)
            per.feedback(y, p, x)

        # AND grouping the error (by iteration number) and find the average of each error
        no_of_bars = number_of_training_vectors / 10
        entries_per_bar = number_of_training_vectors / no_of_bars
        bars = []
        for i in range(0,number_of_training_vectors-entries_per_bar,entries_per_bar):
            avg_error = sum(per.errors[i:i+entries_per_bar])/float(entries_per_bar)
            bars.append(avg_error)

        #
        # THEN the error within each group is less than the previous
        for i in range(1,len(bars)):
            curr_bar = bars[i]
            prev_bar = bars[i-1]

            current_less_than_prev = curr_bar < prev_bar

            self.assertTrue(current_less_than_prev, 'Current Error (bar %d: %f) should be less than previous Error (bar %d: %f)'
                            %(i, curr_bar, i-1,  prev_bar))





if __name__ == '__main__':
    unittest.main()