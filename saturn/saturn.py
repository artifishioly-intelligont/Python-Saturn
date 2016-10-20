from flask import Flask
from classifier import basic_classifier
import olivia
import tool

app = Flask('Saturn')


@app.route('/')
def index():
    return 'Home'


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
    # What we want to do:
    # They tell us an img_url = the sub image
    # We download it
    # We then convert it to an attr vec
    # we give the attr vec to the classifier, it guesses the class
    # we give the class back to the GUI
    local_dest = 'map.jpg'
    tool.download(degas_img_name, local_dest)
    attr_vec = olivia.get_attr_vec(local_dest)
    img_class = basic_classifier.guess(attr_vec)

    return_json = "{ \"class\":\"%s\" }" % img_class  # We need to have a method to make this nice
    return return_json


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
    app.debug = True
    app.run()
