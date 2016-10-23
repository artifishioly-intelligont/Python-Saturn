#!/usr/bin/python

import numpy as np
from sklearn.svm import SVC

class Table:

    feature_dict = {3 : [1, 5.6], 7 : [5.6, 7.6], 8 : [7.6, 10]}
    feature_range = [[1, 5.6], [5.6, 7.6], [7.6, 10]]

    f = {}
    f[1] = 'Formaula 1'
    f[200] = 'pond'
    print f[1]
    print f[1000000]


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
            self.update_range(name_str, value)
            self.update_all()
        else:
            print 'Unable to update'
        return

    # updates the list and dictionary
    # value as a key
    def update_range(self, name, value):
        store_key = []
        count = 0

        key1 = 0
        key2 = 0

        for k, v in self.feature_dict.items():
            store_key.insert(count, k)
            count += 1

        store_key.sort()

        for key in store_key:
            if(value > key):
                key1 = key
            else:
                key2 = key
                break

        if(len(store_key) <= 1):
            range_first_value = (self.range_start_value + value) / 2
            range_second_value = (self.range_end_value + value) / 2
            new_range = [range_first_value, range_second_value]

            self.feature_dict.setdefault(value, new_range)
            self.feature_range.insert(0, new_range)
            self.feature_key.insert(0, value)
        else:
            if(key1 == 0 or key2 == 0):
                if(key1 == 0):
                    range_first_value = (self.range_start_value + value) / 2
                    range_second_value = (key2 + value) / 2
                    new_range = [range_first_value, range_second_value]
                    higher_range_value = [range_second_value, self.feature_dict.get(key2)[1]]


                    self.feature_dict[key2] = higher_range_value
                    self.feature_dict.setdefault(value, new_range)

                    self.update_all_list(-1, value, new_range)
                else:
                    range_first_value = (key1 + value) / 2
                    range_second_value = (self.range_end_value + value) / 2
                    new_range = [range_first_value, range_second_value]
                    lower_range_value = [self.feature_dict.get(key1)[0], range_second_value]


                    self.feature_dict[key1] = lower_range_value
                    self.feature_dict.setdefault(value, new_range)

                    self.update_all_list((store_key.index(key1) + 1), value, new_range)
            else:
                range_first_value = (key1 + value) / 2
                range_second_value = (key2 + value) / 2
                new_range = [range_first_value, range_second_value]

                lower_range_value = [self.feature_dict.get(key1)[0], range_first_value]
                higher_range_value = [range_second_value, self.feature_dict.get(key2)[1]]

                self.feature_dict[key1] = lower_range_value
                self.feature_dict[key2] = higher_range_value
                self.feature_dict.setdefault(value, new_range)

                # updating all the remaining list
                self.update_all_list_((store_key.index(key1) + 1), value, new_range)

        #updating feature table
        self.feature_table.setdefault(value, name)

        return

    def update_all_list(self, index1, value, new_range):
        if(index1 == -1):
            self.feature_range.insert(0, new_range)
            self.feature_key(0, value)
        else:
            self.feature_range.insert(index1, new_range)
            self.feature_key.insert(index1, value)






