import numpy as np
from sklearn import svm
import csv
	
X = []
Y = []

with open('vectors.csv') as myfile:
	csvread = csv.reader(myfile)
	for row in csvread:
		x = []
		for val in row[1:]:
			x.append(float(val))
		X.append(x)
		Y.append(float(row[0]))
		
if len(X) != len(Y):
	print 'X and Y are different lengths'
	exit -1

def extract_datasets(n):
	X_test = []
	Y_test = []

	X_train = []
	Y_train = []
	for i in range(len(X)):
		if i%5 == n:
			X_test.append(X[i])
			Y_test.append(Y[i])
		else:
			X_train.append(X[i])
			Y_train.append(Y[i])
	
	return X_test, Y_test, X_train, Y_train

lin_clf = svm.SVC(kernel='linear',probability=False, decision_function_shape="ovr")

for i in range(5):
	print "*****************TEST " + str(i) + "*****************"
	X_test, Y_test, X_train, Y_train = extract_datasets(i)
	lin_clf.fit(X_train, Y_train)
	
	correct = 0
	for i in range(len(X_test)):
		prediction = lin_clf.predict(np.array([X_test[i]]))
		print "PREDICTION: " + str(prediction[0])
		print "TRUE VALUE: " + str(Y_test[i])
		
		if float(prediction[0]) == float(Y_test[i]):
			correct += 1
			
		prob = lin_clf.decision_function(np.array([X_test[i]]))
		print prob
		print
			
	print 'PERCENTAGE CORRECT: {}%\n'.format(float(correct) / float(len(X_test)) * 100)
	

