#!/usr/bin/python


class FeatureTable:
    feature_dictionary = {}

    def __init__(self, start, increment_number):
        self.start = start
        self.increment_number = increment_number

    def find_id(self, feature_name):
        for k, v in self.feature_dict.items():
            if feature_name == v:
                cls = k
            else:
                cls = 'No match'
        return cls

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