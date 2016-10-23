
class FeatureTable:
    feature_dictionary = {}

    def __init__(self, start, increment_number):
        self.start = start
        self.increment_number = increment_number

    def find_id(self, feature_name):
        for k, v in self.feature_dictionary.items():
            if feature_name == v:
                cls = k
                break
            else:
                cls = 'No match'
        return cls

    def find_name(self, id):
        if self.feature_dictionary.has_key(id):
            cls = self.feature_dictionary.get(id)
        else:
            cls = 'No match'

        return cls

    def find_all_feature(self):
        store_features = []
        count = 0

        if len(self.feature_dictionary) > 0:
            for k,v in self.feature_dictionary.items():
                store_features.insert(count, v)
                count += 1

        return store_features

    def add_feature(self, feat_name):
        n = len(self.feature_dictionary)

        if n == 0:
            self.feature_dictionary[self.start * self.increment_number] = feat_name
            print 'added'
        else:
            self.feature_dictionary[(n + 1) * self.increment_number] = feat_name
            print 'added'

if __name__ == "__main__":
        
    t = FeatureTable(1, 100)

    t.add_feature('pond')
    t.add_feature('tree')
    t.add_feature('chair')

    print t.find_id('pond')
    print t.find_name(100)
    print t.find_name(200)
    print t.find_name(300)