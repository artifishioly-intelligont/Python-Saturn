from flask import Flask
import json

import classifier
import olivia
import tools

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
Fields:	- img_url - Where the image is stored
	    - class - What class the img really belongs to

Return: - ??success or fail??
"""
@app.route('/learn')
def learn():
    return 'Hello World!'


"""
Endpoint to tell the user what class the image is guessed to belong to

Access: GET

Return:	- class - The class that the img is believed to belong to

"""
@app.route('/guess/<degas_img_name>')
def guess(degas_img_name):
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
    img_class = classifier.guess(attr_vec)


    data = {}
    if img_class == None:
        data['success'] = False
        data['message'] = 'There are no classes in the system. Go to {domain}/features/{new_feature_name} to add some.'
    else:
        data['success'] = True
    data['class'] = img_class

    return json.dumps(data)

"""
An endpoint to ensure people use /guess correctly
"""
@app.route('/guess')
def wrong_path_guess():
    data = {}
    data['success'] = False
    data['message'] = 'Incorrect guess path usage. You should use: \'{domain}/guess/{dagus_img_url}\''
    data['class'] = None
    return json.dumps(data)


"""
An endpoint used to fill the class drop down in the GUI

Access: GET

Return:	- classes - An array of strings (classes)
"""
@app.route('/features')
def get_all_features():
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
    msg = tab.add_feature(new_feature)
    data = {}

    if msg:
        data['success'] = True
        data['feature'] = new_feature + ' recorded'
    else:
        data['success'] = False
        data['feature'] = 'Feature already exit'

    return json.dumps(data)

if __name__ == '__main__':
    print 'Log::Saturn:: Starting server'
    app.debug = True
    app.run()
    print 'Log::Saturn:: Server closing'
