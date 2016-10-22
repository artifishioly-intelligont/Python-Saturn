#!/usr/bin/python

import numpy as np
from sklearn.svm import SVC

class Table:

    feature_dict = {3 : [1, 5.6], 7 : [5.6, 7.6], 8 : [7.6, 10]}
    feature_range = [[1, 5.6], [5.6, 7.6], [7.6, 10]]

    feature_key = [3, 7, 8]
    feature_table = {3 : 'pond', 7 : 'car' , 8 : 'tree'}

    range_start_value = 1
    range_end_value = 20

    #defining class range for each type i.e. when id = 10 range will start from 5.6 to 10.5
    x = np.array(feature_range)
    y = np.array(feature_key)


    def find_feature(self, dbl):
        list = [dbl, dbl]
        clf = SVC()
        clf.fit(Table.x, Table.y)
        ftr_key = clf.predict([list])
        feature = self.get_class(ftr_key)
        print feature
        return

    # returns the feature as string using the key
    def get_class(self, key):
        if self.feature_table.has_key(key):
            cls = self.feature_table.get(key)
        else:
            cls = 'No match'

        return cls

    # adding new feature to the list with its double value
    def add_feature(self, name_str, value_dbl):
        value = round(value_dbl)

        if isinstance(name_str, str) and isinstance(value, float):
            self.update(name_str, value)
        else:
            print 'Unable to update'
        return

    # updates the list and dictionary
    def update(self, name):
        store_list = []
        count = 0

        div = self.feature_table.i

        if len(store_list) == 2:
            for ran in store_list:

        else:
            self.

        return

    def update_feature_list(self):



    def test(self, dict):
        count = 0

        dvi = dict.itervalues()
        while(count < len(dict)):
            dvi.next()




