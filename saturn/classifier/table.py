
class FeatureTable:
    feature_dictionary = {}

    def __init__(self, start, increment_number):
        self.start = start
        self.increment_number = increment_number

    def find_id(self, feature_name):
        cls = None
        for k, v in self.feature_dictionary.items():
            if feature_name == v:
                cls = k
                break

        return cls

    def find_name(self, dbl_id):

        id = min(self.feature_dictionary, key=lambda x: abs(x - dbl_id))

        if self.feature_dictionary.has_key(id):
            cls = self.feature_dictionary.get(id)
        else:
            cls = None

        return cls

    def find_all_features(self):
        store_features = []
        count = 0

        if len(self.feature_dictionary) > 0:
            for k,v in self.feature_dictionary.items():
                store_features.insert(count, v)
                count += 1

        return store_features

    def add_feature(self, feature_name):
        n = len(self.feature_dictionary)
        msg = True

        if n == 0:
            self.feature_dictionary[self.start * self.increment_number] = feature_name
            print 'Added'
            return msg
        else:
            msg = feature_name in self.feature_dictionary.values()

            if msg != True:
                self.feature_dictionary[(n + 1) * self.increment_number] = feature_name
                print 'Added'
                msg = True

            return msg

if __name__ == "__main__":
        
    t = FeatureTable(1, 100)

    t.add_feature('pond')
    t.add_feature('tree')
    t.add_feature('chair')

    print t.find_id('pond')
    print t.find_name(100)
    print t.find_name(200)
    print t.find_name(300)

    print t.find_name(230)