from flask import Flask
from classifier import basic_classifier
from olivia import vectorizer
app = Flask('Saturn')


@app.route('/')
def index():
	return 'Home'
#POST
"""
The endpoint used to teach the classifier.

Access: POST
Fields:	- img_url - Where the image is stored
	- class - What class the img really belongs to
	-

Return: - ??success or fail??
"""
@app.route('/learn')
def learn():
	return 'Hello World!'

#POST
"""
Endpoint to tell the user what class the image is guessed to belong to

Access: POST
Fields:	- img_url
	- ?

Return:	- class - The class that the img is believed to belong to

"""
@app.route('/guess')
def guess():
	return 'guess'

#GET
"""
An endpoint used to fill the class drop down in the GUI

Access: GET

Return:	- classes - An array of strings (classes)
"""
@app.route('/features')
def get_all_features():
	return 'null'

#GET
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

