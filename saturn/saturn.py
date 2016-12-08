from flask import Flask, request
import json
import classifier
import olivia
import discover
import os

app = Flask('Saturn')


@app.route('/')
def index():
    print 'Log::Saturn::Message Recieved::/'
    return 'Endpoints: <br>' \
           '\t/ -- List All Endpoints<br>' \
           '\t/guess/{degas_image_loc} -- Determine which feature the image is<br>' \
           '\t/learn/ -- POST a batch of urls to images and the feature type, in order to teach the system<br>' \
           '\t/features/ -- List All    features<br>' \
           '\t/features/{new_feature} -- Add the new feature<br>' \
           '\t/clear -- clears SVM content in classifier'


@app.route('/docs')
def reference():
    return ''

"""
The endpoint used to teach the classifier.

Access: POST
Fields: - img_names - Where the image is stored
        - class - What class the img really belongs to

Return: - success - success or fail
        - failed_images - a list of images that couldn't be vectorized or classified
        - ready - if the SVM is ready to predict classes
"""


@app.route('/learn', methods=["POST"])
def learn():
    print 'Log::Saturn::Message Recieved::/learn/'

    true_class = request.form['theme']
    remote_urls = request.form['urls'].split(";")
    # Remove the redundant last empty string
    if '' in remote_urls:
        remote_urls.remove('')

    # Convert that image to an attr vec

    image_vectors, failed_images, vec_success = olivia.get_all_attr_vecs(remote_urls)

    # Learn the attribute vectors with the given class
    true_classes = [true_class] * len(image_vectors)
    learn_success, ready_to_guess, learn_message, failed_classifications = classifier.learn(image_vectors, true_classes)
    failed_images.update(failed_classifications)

    data = {}
    data['success'] = learn_success
    data['failed_images'] = failed_images
    data['ready'] = ready_to_guess

    if not learn_success:
        data['message'] = 'There was an internal error: ' + learn_message
    else:
        data['message'] = learn_message
    return json.dumps(data)


"""
The endpoint used to correct the classifier after it guesses incorrectly

Access: POST
Fields: - img_names - Where the image is stored
        - classes - What classes the images really belong to

Return: - ??success or fail??
"""


@app.route('/correct', methods=["POST"])
def correct():
    print 'Log::Saturn::Message Recieved::/correct'

    # *** One possible implementation... ***
    # corrections = request.form['corrections']
    # remote_urls = corrections.keys()
    # true_classes = corrections.values()

    # *** A potentially easier one ***
    true_classes = request.form['themes'].split(";")
    remote_urls = request.form['urls'].split(";")
    # Remove the redundant last empty string
    if '' in true_classes:
        true_classes.remove('')
    if '' in remote_urls:
        remote_urls.remove('')

    # Learn won't work if the length of the two lists aren't the same, so return with an error message
    data = {}
    if len(true_classes) != len(remote_urls):
        data['success'] = False
        data['failed_images'] = remote_urls
        data['ready'] = False
        data['message'] = "Length miss-match between lists of URLs and True Classes provided"
        return json.dumps(data)

    # Convert that image to an attr vec
    image_vectors, failed_images, vec_success = olivia.get_all_attr_vecs(remote_urls)

    # Remove all the failed images from true_classes
    for failed_img in failed_images:
        del true_classes[remote_urls.index(failed_img)]

    # Learn the attribute vectors with the given class
    learn_success, ready_to_guess, learn_message, failed_classifications = classifier.learn(image_vectors, true_classes)
    failed_images.update(failed_classifications)

    data = {}
    data['success'] = learn_success
    data['failed_images'] = failed_images
    data['ready'] = ready_to_guess

    if not learn_success:
        data['message'] = 'There was an internal error: ' + learn_message
    else:
        data['message'] = learn_message
    return json.dumps(data)


"""
Endpoint to tell the user what class the image is guessed to belong to

Access: POST

Return: - class - The class that the img is believed to belong to

"""


@app.route('/guess', methods=["POST"])
def guess():
    print 'Log::Saturn::Message Received::/guess/'

    remote_urls = request.form['urls'].split(";")

    # Remove the redundant last empty string
    if '' in remote_urls:
        remote_urls.remove('')

    # Convert that image to an attr vec
    image_vectors, failed_images, vec_success = olivia.get_all_attr_vecs(remote_urls)

    # guess what's in the attr vec!
    guesses, guess_success, failed_classifications = classifier.guess(image_vectors)
    failed_images.update(failed_classifications)
    # Rawr
    first_url = remote_urls[0]
    data = {}
    if not guess_success:
        data['success'] = False
        if first_url in failed_images.keys():
            data['message'] = failed_images[first_url]
        else:
            data['message'] = 'There are not enough trained classes in the system. ' \
                              'POST to {}/learn to train the system.'.format(classifier.hostname)
    else:
        if first_url in guesses.keys():
            data['success'] = True
            data['class'] = guesses[first_url]
        else:
            # if not in guesses, it must be in failed images
            data['success'] = False
            data['message'] = failed_images[first_url]

    return json.dumps(data)


"""
An endpoint used to fill the class drop down in the GUI

Access: GET

Return:	- classes - An array of strings (classes)
"""


@app.route('/features')
def get_all_features():
    print 'Log::Saturn::Message Recieved::/features/'
    features_name_list, success, message = classifier.get_all_features()
    data = {'message': ""}

    if len(features_name_list) > 0:
        data['success'] = True
        data['features'] = features_name_list

    else:
        if not success:
            data['message'] = message
        else:
            data['message'] = "No Features recorded"
        data['success'] = False
        data['features'] = []

    return json.dumps(data)


"""
An endpoint to add a new feature to the list

ACCESS: GET

Return: ??success or failure??
"""


@app.route('/features/<new_feature>')
def add_new_feature(new_feature):
    print 'Log::Saturn::Message Recieved::/features/<new_feature>'
    success, msg = classifier.add_new_feature(new_feature.lower())
    data = {}

    data['success'] = success
    data['message'] = msg

    return json.dumps(data)


'''
gets url list as input
send the url list to oliva's microservice and gets attribute vector in return
sends the attribute vector to classifier and get the class
use that class to send the respective url to the frontend

classifier
learn(array(array(attribute vectors)), array(class_ids))

guess(array(array(attribute vectors))
--> returns array(class_names)
'''


@app.route('/find', methods=['POST'])
def get_class():
    if 'urls' in request.form.keys():
        url_list = request.form['urls'].split(';')
        if '' in url_list:
            url_list.remove('')

    else:
        return json.dumps(
            {'success': False, 'message': 'No URLs specified, add a string separated by colons with key \'urls\''})

    # Get the image attribute vectors
    image_vectors, failed_images, success = olivia.get_all_attr_vecs_and_nsew(url_list)

    all_failed_images = dict(failed_images)
    matching_urls = {}
    unmatching_urls = {}
    try:
        if len(image_vectors) > 0:
            # return {url_n : class_n} and remove the success criteria
            image_direction_classes_dict, success, failed_classifications_directions = classifier.guess(image_vectors)
            all_failed_images.update(discover.condense_error_paths(failed_classifications_directions))

            image_class_probs = discover.condense_and_determine_probs(image_direction_classes_dict)

            if 'theme' in request.form.keys():
                type = request.form['theme'].lower()
                # returns a dict where all values have the value 'type'
                matching_urls = {url: image_class_probs[url] for url in image_class_probs.keys() if
                                 discover.isMostLikelyFeature(type)}
                unmatching_urls = {url: image_class_probs[url] for url in image_class_probs.keys() if
                                   not discover.isMostLikelyFeature(type)}

            else:
                # matching_urls = image_class_probs
                matching_urls = {url: discover.highestChanceFeature(theme_probs) for url, theme_probs
                                 in image_class_probs.items()}

    except Exception as e:
        # Keep all the previous failed messages
        # then append the new error messages to the ones that failed during the classification process        
        all_failed_images.update({url: e.message for url in image_vectors.keys()})

        return json.dumps({'success': False,
                           'failed_images': all_failed_images,
                           'matching_urls': {},
                           'unmatching_urls': {}
                           })

    return json.dumps({'success': not (len(all_failed_images) > 0),
                       'failed_images': all_failed_images,
                       'matching_urls': matching_urls,
                       'unmatching_urls': unmatching_urls
                       })


@app.route('/clear', methods=['DELETE', 'GET'])
def clear():
    if request.method == 'GET':
        return 'Please use HTTP-DELETE to use this endpoint, your request to <b>clear</b> was ignored.'

    data = {}
    success, message, ready = classifier.clearSVM()
    data['success'] = success
    data['message'] = 'SVM Database\'s content {} cleared, Message:{}'.format(''if success else 'not', message)
    data['ready'] = ready


    return json.dumps(data)


@app.route('/reset', methods=['DELETE', 'GET'])
def reset():
    if request.method == 'GET':
        return 'Please use HTTP-DELETE to use this endpoint, your request to <b>reset</b> was ignored.'

    data = {}
    success, message, ready = classifier.resetSVM()
    data['success'] = success
    data['message'] = 'SVM Database\'s content {} reset, Message:{}'.format(''if success else 'not', message)
    data['ready'] = ready

    return json.dumps(data)

@app.route('/meteor', methods=['GET'])
def long_reset():
    return reset()

if __name__ == '__main__':
    print 'Log::Saturn:: Starting server'
    app.debug = True
    app.run()
    print 'Log::Saturn:: Server closing'
