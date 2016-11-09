import numpy as np
from sklearn.linear_model import SGDClassifier
import csv
import operator
import random

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
	x = random.uniform(-100,100)
	y = random.uniform(-100,100)
	return x,y


def ran_pos_from_quad(acceptable_quads):
	x,y = ran_pos()

	while(quad(x,y) not in acceptable_quads):
			x,y = ran_pos()
	return x,y

X = []
Y = []
for n in range(1,4):
	values = 25
	for i in range(values):
		x,y = ran_pos_from_quad([n])
		q = quad(x,y)
		X.append([x,y])
		Y.append(q)
		
X = np.array(X)
Y = np.array(Y)

lin_clf = SGDClassifier(loss='log')

labels = [1,2,3,4]

print "*******TRAINING 1******"

lin_clf.partial_fit(X, Y, labels)

print lin_clf.predict(np.array([[10,10]]))
print lin_clf.predict(np.array([[-10,10]]))
print lin_clf.predict(np.array([[-10,-10]]))
print lin_clf.predict(np.array([[10,-10]]))

print "*******TRAINING 2******"

X = []
Y = []
values = 25
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
