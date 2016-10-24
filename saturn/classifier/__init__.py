import Perceptron, table as Table

perceptron = Perceptron.Perceptron(1000)
table = Table.FeatureTable(0, 100)

def guess(attr_vec):
    """
    Guesses which class the sub-image belongs to.

    e.g. Given an image it could return 'tree'

    :param attr_vec: The long list of numerical representations of the attributes extracted (by olivia module) of a sub-image
    :return: The name of the class the classifier believes the sub-image belongs to
    """
    raw_pred = perceptron.predict(attr_vec)
    pred_class = table.find_name(raw_pred)
    return pred_class

def learn(attr_vec, true_class):
    """
    Forces the classifier to learn what class the sub-image belongs to.

    :param attr_vec: The long list of numerical representations of the attributes extracted (by olivia module) of a sub-image
    :param true_class: The class that the sub-image belongs to
    :return: None
    """
    raw_pred = perceptron.predict(attr_vec)
    pred_class = table.find_name(raw_pred)

    perceptron.feedback(true_class, pred_class, attr_vec)
