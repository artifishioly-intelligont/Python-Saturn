from flask import Flask, render_template, request, redirect, url_for, send_from_directory

import json

import classifier
import olivia
import tools

app = Flask('Saturn')

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = '~/SaturnServer/images'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['tiff', 'png', 'jpg', 'jpeg', 'gif'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
           

@app.route('/')
def index():
    print 'Log::Saturn::Message Recieved::/'
    return 'Endpoints: <br>' \
           '\t/ -- List All Endpoints<br>' \
           '\t/guess/ -- Determine which feature the image is<br>' \
           '\t/learn/ -- POST a batch of urls to images and the feature type, in order to teach the system<br>' \
           '\t/features/ -- List All    features<br>' \
           '\t/features/new -- Add a new feature<br>'


"""
The endpoint used to teach the classifier.

Access: POST
Fields: - img_names - Where the image is stored
        - class - What class the img really belongs to

Return: - ??success or fail??
"""
@app.route('/learn', methods=['POST'])
def learn():
    print 'Log::Saturn::Message Recieved::/learn'
    
    data = {}
    true_feature = request.form['feature']
    failed_imgs = []
    counter = -1

    # Loop through the uploaded files
    for key in request.files:
        counter += 1
        file = request.files[key]
        local_dest = tools.images.new_location()
    
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Save the file to the specified location
            file.save(local_dest)
            # Convert that image to an attr vec
            attr_vec = olivia.get_attr_vec(local_dest)
            # learn!
            img_class = classifier.learn(attr_vec, true_feature)

            data['success' + str(counter)] = True
            data['true_feature'] = true_feature
        else:
            print 'Error::Saturn:: Invalid file type'

            data['success' + str(counter)] = False
            failed_imgs.append(file.filename) 

    data['failed_images'] = failed_imgs

    return json.dumps(data)


"""
Endpoint to tell the user what class the image is guessed to belong to

Access: POST

Return: - class - The class that the img is believed to belong to

"""
@app.route('/guess', methods=['POST'])
def guess():
    print 'Log::Saturn::Message Recieved::/guess'
    
    data = {}
    failed_imgs = []
    counter = -1

    # Loop through the uploaded files
    for key in request.files:
        counter += 1
        file = request.files[key]
        local_dest = tools.images.new_location()
    
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Save the file to the specified location
            file.save(local_dest)
            # Convert that image to an attr vec
            attr_vec = olivia.get_attr_vec(local_dest)
            # guess!
            guessed_feature = classifier.guess(attr_vec)

            data['success' + str(counter)] = True           
            data['guessed_feature' + str(counter)] = guessed_feature
        else:
            print 'Error::Saturn:: Invalid file type'

            data['success' + str(counter)] = False
            data['guessed_feature' + str(counter)] = None
            
            failed_imgs.append(file.filename)

    data['failed_images'] = failed_imgs
    
    return json.dumps(data)


"""
An endpoint used to fill the class drop down in the GUI

Access: all

Return: - classes - An array of strings (classes)
"""
@app.route('/features')
def get_all_features():
    print 'Log::Saturn::Message Recieved::/features/'
    features_name_list = classifier.tab.find_all_features()
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

ACCESS: POST
Fields: - feature -- The new feature

Return: ??success or failure??
"""
@app.route('/features/new', methods=['POST'])
def add_new_feature():
    print 'Log::Saturn::Message Recieved::/features/new'

    new_feature = request.form['feature']
    msg = classifier.tab.add_feature(new_feature)
    data = {}

    if msg:
        data['success'] = True
        data['feature'] = new_feature + ' recorded'
    else:
        data['success'] = False
        data['feature'] = 'Feature already exists'

    return json.dumps(data)

if __name__ == '__main__':
    print 'Log::Saturn:: Starting server'
    app.run()
    print 'Log::Saturn:: Server closing'
