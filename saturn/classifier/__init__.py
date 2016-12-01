import SVM, table as Table


svm = SVM.SVM()
#tab = Table.FeatureTable(0, 100, {100 : 'Pond', 200 : 'Tree', 300 : 'Park', 400 : 'Pathway', 500 : 'Road'})
tab = Table.FeatureTable(0, 100, {100 : 'Building', 200 : 'House', 300 : 'Road', 400 : 'Tree'})

def guess(attr_vec):
    """
    Guesses which class the sub-images belong to.

    e.g. Given an image it could return 'tree'

    :param attr_vec: The long list of numerical representations of the attributes extracted (by olivia module) of a sub-image
    :return: The name of the class the classifier believes the sub-image belongs to
    """
    raw_preds, raw_probs = svm.predict([attr_vec])
    
    class_pred = tab.find_name(raw_preds[0])
    prob = raw_probs[0][0]

    print 'Log::Classifier:: predicts the class %s' % class_pred
    print 'Log::Classifier:: probabilities:'
    print prob
    return class_pred, prob

def learn(attr_vecs, true_classes):
    """
    Forces the classifier to learn what class the sub-image belongs to.

    :param attr_vec: The long list of numerical representations of the attributes extracted (by olivia module) of a sub-image
    :param true_class: The class that the sub-image belongs to
    :return: None
    """
    true_class_ids = []
    for name in true_classes:
        true_class_ids.append(tab.find_id(name))

    print 'Log::Classifier:: learning'

    svm.learn(attr_vecs, true_class_ids)
