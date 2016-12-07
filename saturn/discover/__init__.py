def condense_and_determine_probs(image_direction_classes_dict):
    """

    :param image_direction_classes_dict: A dictionary of <url>#<direction> to class
    :return: dictionary(url->dictionary(feature_type->probabillity)
    e.g.
    {
        'http://url/to/imageA.jpg' : { 'tree' : 0.555, 'pond' : 0.333, 'fire' : 0.111 },
        'http://url/to/imageB.jpg' : { 'tree' : 0.777, 'fire' : 0.222 }
    }

    """
    probabilities = {}
    single_chance = 0.111
    for url_and_direction, feature_type in image_direction_classes_dict.items():
        url = url_and_direction.split('#')[0]
        direction = url_and_direction.split('#')[1]
        # If this is not the first time we have seen the url
        if url in probabilities:
            # If this url has been classed as this feature?
            if feature_type in probabilities[url]:
                probabilities[url][feature_type] += single_chance
            else:
                probabilities[url][feature_type] = single_chance
        else:
            probabilities[url] = {feature_type: single_chance}
    return probabilities


def condense_error_paths(image_direction_dict):
    failed_urls = {}
    for url_and_direction, error in image_direction_dict.items():
        url = url_and_direction.split('#')[0]
        direction = url_and_direction.split('#')[1]
        if url in failed_urls:
            failed_urls[url] += "{}:{};".format(direction, error)
        else:
            failed_urls[url] = "{}:{};".format(direction,error)
    return failed_urls


def isMostLikelyFeature(feature_probs, feature_type):
    return highestChanceFeature(feature_probs) == feature_type


def highestChanceFeature(feature_probs):
    winning_feature_type = feature_probs.keys()[0]
    winning_prob = feature_probs[winning_feature_type]
    for current_feature, current_prob in feature_probs.items()[1:]:
        if current_prob > winning_prob:
            winning_feature_type = current_feature
            winning_prob = current_prob
    return winning_feature_type

