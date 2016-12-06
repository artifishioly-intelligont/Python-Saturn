
class Perceptron:

    learning_rate = 0.001
    weights = []
    errors = []

    def __init__(self, length_of_input):
        self.weights = [1.0]*length_of_input

    def predict(self,input_vector):
        """
        Guess the true value from the input vector

        i.e. What class the input_vector belongs to

        :param input_vector: The numerical representation of the attributes
        :return:
        """
        if len(self.weights) != len(input_vector):
            raise Exception('Input vector (length: %d)is not of the same length as the weights (length: %d)' % (len(input_vector),len(self.weights)))

        total = 0
        for index in range(0,len(input_vector)):
            total += self.weights[index] + input_vector[index]

        return total

    def feedback(self, true_value, predicted_value, input_vector):
        error = true_value - predicted_value
        if(abs(error) != 0):
            self.errors.append(float(abs(true_value)) / abs(error))
        
        else:
            self.errors.append(float(0))
        
        lambdaDeltaE = list(input_vector)
        for i in range(0, len(input_vector)):
            lambdaDeltaE[i] *= self.learning_rate*2*error

        for i in range(0,len(input_vector)):
            self.weights[i] += lambdaDeltaE[i]


if __name__ == '__main__':
    import random
    # Lets train a perceptron to learn the function: f_true(x1,x2,x3,x4,x5,x6) = 10*x1 + 100*x3 + 1000*x5
    #   therefore we have an input vector of 6 elements
    input_length = 6
    number_of_training_vectors = 50

    def f_true(x):
        return 10 * x[1] + 100 * x[3] + 1000 * x[5]

    # Generate input data
    X = []
    for i in range(number_of_training_vectors):
        x = random.sample(range(-20, 20), input_length)
        X.append(x)

    # Generate true/actual value for each input vector
    Y = []
    for n in range(number_of_training_vectors):
        Y.append(f_true(X[n]))

    # Make classifier
    learner = Perceptron(input_length)

    # Train classifier
    for m in range(number_of_training_vectors):
        x = X[m]
        y = Y[m]
        p = learner.predict(x)
        print 'x = %s' % str(x)
        print 'y = %s' % str(y)
        print 'p = %s' % str(p)
        print '----------------\n\n'

        learner.feedback(y, p, x)

    print '--------------'
    print 'errors:'+str(learner.errors)

    try:
        import plotly
        import plotly.graph_objs as go
    except ImportError as ie:
        print 'You have not installed \'plotly\', a graphing tool. Hence a visualisation of the error (as %) cannot be shown'
        print 'Run:'
        print '     pip install plotly'
        print 'Then re-run this script'

    xs = range(0,len(learner.errors))
    ys = learner.errors

    trace = go.Scatter(x = xs, y=ys)
    plotly.offline.plot([trace])
