from flask import Flask, request
import json
import urllib
import classifier
import olivia
import tools
import image as find
import os

from copy import deepcopy

app = Flask('Saturn')

#creating table
tab = classifier.tab

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
    degas_urls = request.form['urls'].split(";")

    # Remove the
    degas_urls.pop()

    failed_urls = []
    fail_messages = []
    local_urls = []
    attr_vecs = []
    true_classes = []
    for image_name in degas_urls:
        local_dest = tools.images.new_location()
        try:
            urllib.urlretrieve(image_name, local_dest)
        #    tools.download_image(image_name, local_dest)
            local_urls.append(local_dest)
        except Exception as ex:
            print 'Error::Saturn:: ' + ex.message
            failed_urls.append(image_name)
            fail_messages.append(ex.message)
    # local_urls = [None, None]

    # If all downloads failed
    if len(local_urls) == len(failed_urls):
        data = {}
        data['success'] = False
        data['failed_images'] = failed_urls
        data['fail_messages'] = fail_messages
        return json.dumps(data)

    for feature in local_urls:
        attr_vec = deepcopy(olivia.get_attr_vec(local_dest))         
        attr_vecs.append(attr_vec)
        true_classes.append(true_class)
        
    classifier.learn(attr_vecs, true_classes)

    data = {}
    data['success'] = True
    data['failed_images'] = failed_urls
    data['fail_messages'] = fail_messages

    return json.dumps(data)

"""
Endpoint to tell the user what class the image is guessed to belong to

Access: POST

Return: - class - The class that the img is believed to belong to

"""
@app.route('/guess', methods=["POST"])
def guess():
    print 'Log::Saturn::Message Recieved::/guess/'

    remote_urls = request.form['urls'].split(";")
    # Remove the redundant last empty string
    remote_urls.pop()
        
    # Convert that image to an attr vec
    image_vectors, failed_images, vec_success = olivia.get_all_attr_vecs(remote_urls)

    # guess what's in the attr vec!
    guesses, guess_success = classifier.guess(image_vectors)

    data = {}
    if not guess_success:
        data['success'] = False
        data['message'] = 'There are not enough trained classes in the system. ' \
                          'POST to {domain}/learn to train the system.'
    else:
        first_url = remote_urls[0]
        if first_url in guesses.keys():
            data['success'] = True
            data['class'] = guesses[first_url]
        else:
            # if not in guesses, it must be in failed images
            data['success'] = False
            data['message'] = failed_images[first_url]

    return json.dumps(data)


"""
Endpoint to tell the user what class the image is guessed to belong to

Access: GET

Return:	- class - The class that the img is believed to belong to

"""
@app.route('/guess2/<degas_img_name>')
def guess2(degas_img_name):
    print 'Log::Saturn::Message Recieved::/guess/' + degas_img_name

    # Find somewhere to store the image
    local_dest = tools.images.new_location()

    # Store the image at local_dest
    try:
        tools.download_image(degas_img_name, local_dest)
    except Exception as ex:
        print 'Error::Saturn:: ' + ex.message

        data = {}
        data['success'] = False
        data['message'] = ex.message
        data['class'] = None

        return  json.dumps(data)

    # Convert that image to an attr vec
    attr_vec = olivia.get_attr_vec(local_dest)
    # guess what's in the attr vec!
    img_class, img_proba = classifier.guess(attr_vec)


    data = {}
    if img_class == None:
        data['success'] = False
        data['message'] = 'There are no classes in the system. Go to {domain}/features/{new_feature_name} to add some.'
    else:
        data['success'] = True
    data['class'] = img_class
    data['probs'] = list(img_proba)

    return json.dumps(data)

"""
An endpoint to ensure people use /guess correctly
"""
"""@app.route('/guess')
def wrong_path_guess():
    print 'Log::Saturn::Message Recieved::/guess/'
    data = {}
    data['success'] = False
    data['message'] = 'Incorrect guess path usage. You should use: \'{domain}/guess/{dagus_img_url}\''
    data['class'] = None

    return json.dumps(data)

"""
"""
An endpoint used to fill the class drop down in the GUI

Access: GET

Return:	- classes - An array of strings (classes)
"""
@app.route('/features')
def get_all_features():
    print 'Log::Saturn::Message Recieved::/features/'
    features_name_list = tab.find_all_features()
    data = {}

    if len(features_name_list) > 0:
        data['success'] = True
        data['features'] = features_name_list
    else:
        data['success'] = False
        data['features'] = 'No Feature Recorded.'

    return json.dumps(data)

"""
An endpoint to add a new feature to the list

ACCESS: GET

Return: ??success or failure??
"""
@app.route('/features/<new_feature>')
def add_new_feature(new_feature):
    print 'Log::Saturn::Message Recieved::/features/<new_feature>'
    msg = tab.add_feature(new_feature)
    data = {}

    if msg:
        data['success'] = True
        data['feature'] = new_feature + ' recorded'
    else:
        data['success'] = False
        data['feature'] = 'Feature already exit'

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
    if not os.system("ping -c 1 " + classifier.hostname):
        return json.dumps({'success': False, 'message': 'The classifier at {} cannot be reached'.format(classifier.hostname)})

    if not os.system("ping -c 1 " + olivia.hostname):
        return json.dumps({'success': False, 'message': 'Olivia at {} cannot be reached'.format(olivia.hostname)})

    # Get the image attribute vectors
    image_vectors, failed_images, success = find.send_to_olivia(url_list)

    output_classes = {}
    try:

        if len(image_vectors) > 0:
            # return {url_n : class_n} and remove the success criteria
            image_classes_dict = find.send_to_classifier(image_vectors)

            # Remove the success entry as it is not a URL
            del image_classes_dict['success']

            # returns a dict where all values have the value 'type'
            output_classes = find.type_class(type, image_classes_dict)

    except Exception as e:
        # Keep all the previous failed messages
        # then append the new error messages to the ones that failed during the classification process
        all_failed_images = dict(failed_images)
        all_failed_images.update({url: e.message for url in image_vectors.keys()})

        json.dumps({'success': False,
                    'failed_images': all_failed_images,
                    'image_classes': {}
                    })

    return json.dumps({'success': len(failed_images) > 0,
                       'failed_images': failed_images,
                       'image_classes': output_classes})


if __name__ == '__main__':
    print 'Log::Saturn:: Starting server'
    app.debug = True
    app.run()
    print 'Log::Saturn:: Server closing'
