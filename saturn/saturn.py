from flask import Flask, request
import json
import classifier
import olivia
import image as find
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
           '\t/features/{new_feature} -- Add the new feature<br>'

"""
The endpoint used to teach the classifier.

Access: POST
Fields: - img_names - Where the image is stored
        - class - What class the img really belongs to

Return: - ??success or fail??
"""
@app.route('/learn', methods=["POST"])
def learn():
    print 'Log::Saturn::Message Recieved::/learn/'

    true_class = request.form['theme']
    remote_urls = request.form['urls'].split(";")
    # Remove the redundant last empty string
    remote_urls.pop()

    # Convert that image to an attr vec

    image_vectors, failed_images, vec_success = olivia.get_all_attr_vecs(remote_urls)

    # Learn the attribute vectors with the given class
    true_classes = true_class*len(image_vectors)
    learn_success, ready_to_guess, learn_message, failed_classifications = classifier.learn(image_vectors, true_classes)
    failed_images.update(failed_classifications)

    data = {}
    data['success'] = learn_success
    data['failed_images'] = failed_images
    data['ready'] = ready_to_guess

    if not learn_success:
        data['message'] = 'There was an internal error: '+learn_message
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
    remote_urls.pop()
        
    # Convert that image to an attr vec
    image_vectors, failed_images, vec_success = olivia.get_all_attr_vecs(remote_urls)

    # guess what's in the attr vec!
    guesses, guess_success, failed_classifications = classifier.guess(image_vectors)
    failed_images.update(failed_classifications)

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
    success, msg = classifier.add_new_feature(new_feature)
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
    """
    :return:
    example (successful) return:
    {
        success : True,
        image_classes :
        {
            'url1' : [0.1, 0.0, 0.5, ...],
            'url2' : [0.9, 1.2, 0.6, ...]
        },
        failed_images : {}
    }
    example (failed) return:
    {
    success : False,
    image_classes :
    {
        'url1' : [0.1, 0.0, 0.5, ...]
    },
    failed_images :
    {
        'url2' : 'DownloadException: The path 'url2' does not exist'
    }
    """
    
    """
    # Ensure we are sent json
    json_data = request.get_json()
    if not json_data:
        return json.dumps({'success': False, 'message': 'No JSON data was sent to the endpoint'})

    # Ensure the parameters exist
    url_list = json_data['urls']
    type = json_data['theme']  # e.g. pong, tree, etc
    if not url_list:
        return json.dumps({'success': False, 'message': 'No URLs specified, add an array value with key \'urls\''})
    if not type:
        return json.dumps({'success': False, 'message': 'No search type specified, add a string value with key \'type\''})

    # Ensure that the micro-services are running
    classifier_reached = os.system("ping -c 1 " + classifier.hostname) == 0
    if not classifier_reached:
        return json.dumps({'success': False, 'message': 'The classifier at {} cannot be reached'.format(classifier.hostname)})

    olivia_reached = os.system("ping -c 1 " + olivia.hostname) == 0
    if not olivia_reached:
        return json.dumps({'success': False, 'message': 'Olivia at {} cannot be reached'.format(olivia.hostname)})
    """
    
    url_list = request.form['urls'].split(';')
    type = request.form['theme']

    # Get the image attribute vectors
    image_vectors, failed_images, success = olivia.get_all_attr_vecs(url_list)
    
    all_failed_images = dict(failed_images)
    output_classes = {}
    try:
        if len(image_vectors) > 0:
            # return {url_n : class_n} and remove the success criteria
            image_classes_dict, success, failed_classifications = classifier.guess(image_vectors)
            all_failed_images.update(failed_classifications)

            # returns a dict where all values have the value 'type'
            output_classes = {url: type for url in image_classes_dict.keys() if image_classes_dict[url] == type}

    except Exception as e:
        # Keep all the previous failed messages
        # then append the new error messages to the ones that failed during the classification process        
        all_failed_images.update({url: e.message for url in image_vectors.keys()})
        
        return json.dumps({'success': False,
                    'failed_images': all_failed_images,
                    'image_classes': {}
                    })

    return json.dumps({'success': len(all_failed_images) > 0,
                       'failed_images': all_failed_images,
                       'image_classes': output_classes})


if __name__ == '__main__':
    print 'Log::Saturn:: Starting server'
    app.debug = True
    app.run()
    print 'Log::Saturn:: Server closing'
