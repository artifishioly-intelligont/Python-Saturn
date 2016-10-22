from flask import Flask
import json

import classifier
import olivia
import tools

app = Flask('Saturn')


@app.route('/')
def index():
    return 'Endpoints:\n' \
           '\t'


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
    return 'null'


"""
An endpoint to add a new feature to the list

ACCESS: GET

Return: ??success or failure??
"""
@app.route('/features/<new_feature>')
def add_new_feature(new_feature):
    return new_feature


if __name__ == '__main__':
    print 'Log::Saturn:: Starting server'
    app.debug = True
    app.run()
    print 'Log::Saturn:: Server closing'
