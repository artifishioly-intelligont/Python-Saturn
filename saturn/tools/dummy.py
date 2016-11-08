from flask import Flask, request
import json
import re

app = Flask('tester')

@app.route('/')
def start():
	return 'server started'

@app.route('/post', methods=['POST', 'GET'])
def something():
	print 'recieved post'

	if request.method == 'POST':
		jsonData = request.get_json()
		data = jsonData['key1']
		print type(data)
		print data

	else:
		error = 'Not a Post'
	return 'Got it'

if __name__ == '__main__':
	app.run(port=8000)