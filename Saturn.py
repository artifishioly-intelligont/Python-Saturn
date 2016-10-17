from flask import Flask
app = Flask('Saturn')

@app.route('/')
def index():
	return 'null'

@app.route('/learn')
def learn():
	return 'null'


@app.route('/guess')
def guess():
	return 'null'


@app.route('/features')
def get_all_features():
	return 'null'


@app.route('/features/<new_feature>')
def add_new_feature(new_feature):
	return 'null'

if __name__ == '__main__':
	app.debug = True
	app.run()

