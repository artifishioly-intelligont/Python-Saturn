import Perceptron, table as Table

perceptron = Perceptron.Perceptron(1024)
tab = Table.FeatureTable(0, 100, {100 : 'Pond', 200 : 'Tree', 300 : 'Park', 400 : 'Pathway'})

def guess(attr_vec):
    """
    Guesses which class the sub-image belongs to.

    e.g. Given an image it could return 'tree'

    :param attr_vec: The long list of numerical representations of the attributes extracted (by olivia module) of a sub-image
    :return: The name of the class the classifier believes the sub-image belongs to
    """
    print 'Debug::Classifier:: %s' % str(attr_vec)
    raw_pred = perceptron.predict(attr_vec)
    pred_class = tab.find_name(raw_pred)

    print 'Log::Classifier:: predicts the class %s' % pred_class
    return pred_class

def learn(attr_vec, true_class):
    """
    Forces the classifier to learn what class the sub-image belongs to.

    :param attr_vec: The long list of numerical representations of the attributes extracted (by olivia module) of a sub-image
    :param true_class: The class that the sub-image belongs to
    :return: None
    """
    raw_pred_id = perceptron.predict(attr_vec)
    true_class_id = tab.find_id(true_class)
    print 'Log::Classifier:: predicts the class %s' % tab.find_name(raw_pred_id)
    print 'Log::Classifier:: learning'

    perceptron.feedback(true_class_id, raw_pred_id, attr_vec)
