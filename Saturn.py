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
	#What we want to do:
	# They tell us an img_url = the sub image
	# We download it
	# We then convert it to an attr vec
	# we give the attr vec to the classifier, it guesses the class
	# we give the class back to the GUI
	
	img_loc = 'Get this from the request' # We need to extract the img_loc from the post
	attr_vec = vectorizer.extract_attributes(img_loc)
	img_class = basic_classifier.guess(attr_vec)
	
	return_json = "{ \"class\":\"%s\" }"  % img_class # We need to have a method to make this nice
	return return_json

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

