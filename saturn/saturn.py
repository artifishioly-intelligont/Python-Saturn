from flask import Flask, request
import json
import urllib
import classifier
import olivia
import tools
import image as find
import types

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
    # Stub values
    if request.method == 'POST':
        true_class = request.form['theme']
        degas_urls = request.form['urls'].split(";")
        degas_urls.pop()

    # return json.dumps(degas_urls)
    # De-comment for manual testing
    # degas_urls = ['windmill.jpg','windmill.jpg']
    # true_class = classifier.tab.find_all_features()[0]

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
    # Stub values
    if request.method == 'POST':
        degas_urls = request.form['urls'].split(";")
        degas_urls.pop()
        
    # degas_urls = ['windmill.jpg','windmill.jpg']

    failed_urls = []
    fail_messages = []
    local_urls = []
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

    # Convert that image to an attr vec
    attr_vec = olivia.get_attr_vec(local_urls[0])
    # guess what's in the attr vec!
    # img_class, img_proba = classifier.guess(attr_vec)
    img_class = classifier.guess(attr_vec)


    data = {}
    if img_class == None:
        data['success'] = False
        data['message'] = 'There are no classes in the system. Go to {domain}/features/{new_feature_name} to add some.'
    else:
        data['success'] = True
        data['class'] = img_class
        #data['proba'] = list(img_proba)

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
@app.route('/find', methods=['POST', 'GET'])
def get_class():
    '''

    :return:
    '''
    #holds the url that belongs to the specific type
    output_class = []

    if request.method == 'POST':
        jsonData = request.get_json()
        url_list = jsonData['url']
        type = jsonData['type']

        if url_list:
            image_attributes_dict = find.send_to_olivia(url_list)

            if type(image_attributes_dict) != types.BooleanType:
                image_attributes_array = image_attributes_dict.values()
                # return {url : class}
                image_classes_dict = find.send_to_classifier(image_attributes_array)

                #returns array of url with are of specific type
                output_class = find.type_class(type, image_classes_dict)

    return json.dump(output_class)

if __name__ == '__main__':
    print 'Log::Saturn:: Starting server'
    app.debug = True
    app.run()
    print 'Log::Saturn:: Server closing'
