#!/usr/bin/python


class FeatureTable:
    feature_dictionary = {}

    def __init__(self, start, increment_number):
        self.start = start
        self.increment_number = increment_number

<<<<<<< HEAD
    def find_id(self, feature_name):
        for k, v in self.feature_dict.items():
            if feature_name == v:
                cls = k
            else:
                cls = 'No match'
        return cls
=======
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
>>>>>>> ec032c7f7526d24bc5e217cfdbd1b7aa3450154a

    def find_name(self, id):
        if self.feature_dictionary.has_key(id):
            cls = self.feature_dictionary.get(id)
        else:
            cls = 'No match'

        return cls

    def add_feature(self, feat_name):
        n = len(self.feature_dictionary)

        if n == 0:
            self.feature_dictionary[self.start + n * self.increment_number] = feat_name
        else:
            self.feature_dictionary[n * self.increment_number] = feat_name
        return

    if __name__ == "__main__":
        from classifier import *
        
        t = FeatureTable(1, 100)

        t.add_feature('pond')

        print t.find_id('pond')