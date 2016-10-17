from flask import Flask
app = Flask('Saturn')

@app.route('/')
def index():
	return 0

@app.route('/learn')
def learn():
	return 0


@app.route('/guess')
def guess():
	return 0


@app.route('/features')
def get_all_features():
	return 0


@app.route('/features/<new_feature>')
def add_new_feature(new_feature):
	return 0

if __name__ == '__main__':
	app.debug = True
	app.run()

