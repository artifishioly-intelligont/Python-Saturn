from flask import Flask
from classifier import poo
app = Flask('Saturn')

@app.route('/')
def index():
	return poo.eat()

@app.route('/learn')
def learn():
	return 'Hello World!'


@app.route('/guess')
def guess():
	return 'guess'


@app.route('/features')
def get_all_features():
	return 'null'


@app.route('/features/<new_feature>')
def add_new_feature(new_feature):
	return new_feature

if __name__ == '__main__':
	app.debug = True
	app.run()

