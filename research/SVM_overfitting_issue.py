import numpy as np
from sklearn.linear_model import SGDClassifier
import csv
import operator
import random
import time

from sklearn.kernel_approximation import RBFSampler

"""
This script highlights the issue of over-fitting when using SVMs. 

We originally train the SVM to identify data in quadrants [1,2,3], and
this works fine since it receives all data together and can shuffle the data. 

However, we later train it to identify quadrant 4 by giving it a new batch of
data from this quadrant. Since the data is all in this category, it can't be shuffled,
and therefore the SVM over-fits the line, skewing the results from the previously 
learnt classes [1,2,3] (Stefan can explain this)

This will be a problem when we train our SVM to learn a new feature, as it 
will over-fit the line. Therefore, we likely need to store all the data
used to train the SVM throughout its lifetime, and re-train it using
that data and the additional data whenever it learns a new feature.
"""



# 3 | 4
#---|---
# 2 | 1


def quad(x,y):
	if 0 in [x,y]:
			 return None

	posx = (x/abs(x) == 1)
	posy = (y/abs(y) == 1)

	if posx and posy:
			return 4
	elif posx and not posy:
			return 1
	elif not posx and posy:
			return 3
	elif not posx and not posy:
			return 2
	else:
			return None

def ran_pos():
	x = random.uniform(-10,10)
	y = random.uniform(-10,10)
	return x,y
	
def ran_noise(x, y):
	ranlist = [x, y]
	#for i in range (1022):
	#	ranlist.append(random.uniform(-100,100))
	return ranlist
	


def ran_pos_from_quad(acceptable_quads):
	x,y = ran_pos()

	while(quad(x,y) not in acceptable_quads):
			x,y = ran_pos()
	return x,y
	
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

X_test_1 = []
Y_test_1 = []

X_train_1 = []
Y_train_1 = []

for i in range(len(X)):
	if i%5 == 0:
		X_test_1.append(X[i])
		Y_test_1.append(Y[i])
	else:
		X_train_1.append(X[i])
		Y_train_1.append(Y[i])

lin_clf = SGDClassifier(penalty='l2', loss='hinge', shuffle=True)

labels = [100,200,300,400,500]

#lin_clf.partial_fit(X_train_1, Y_train_1, labels)
lin_clf.fit(X,Y)

print "*******TRAINING 1******"

correct = 0
for i in range(len(X)):
	prediction = lin_clf.predict(np.array([X[i]]))
	print "PREDICTION: " + str(prediction[0])
	print "TRUE: " + str(Y[i])
	
	if float(prediction[0]) == float(Y[i]):
		correct += 1

print correct
print len(X)
print 'Percentage COrrect: {}%'.format(correct/(len(X)))
"""
print "*******TRAINING 2******"

values = 10000
for i in range(values):
	x,y = ran_pos_from_quad([4])
	q = quad(x,y)
	X.append([x,y])
	Y.append(q)
	
X_features = rbf_feature.fit_transform(X)

lin_clf.partial_fit(X_features, Y, labels)

print lin_clf.predict(np.array([[10,10]]))
print lin_clf.predict(np.array([[-10,10]]))
print lin_clf.predict(np.array([[-10,-10]]))
print lin_clf.predict(np.array([[10,-10]]))


print "*******TRAINING 3******"

X = []
Y = []
values = 10000
for i in range(values):
	x,y = ran_pos_from_quad([4])
	q = quad(x,y)
	X.append([x,y])
	Y.append(q)
	
X = np.array(X)
Y = np.array(Y)

lin_clf.partial_fit(X, Y)

print lin_clf.predict(np.array([[10,10]]))
print lin_clf.predict(np.array([[-10,10]]))
print lin_clf.predict(np.array([[-10,-10]]))
print lin_clf.predict(np.array([[10,-10]]))
"""