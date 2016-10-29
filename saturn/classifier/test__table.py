import unittest
import table

class TableUnitTest(unittest.TestCase):

    def setUp(self):
        self.tab = table.FeatureTable(0, 100, {100: 'Pond', 200: 'Tree', 300: 'Park', 400: 'Pathway'})

    def test_find_name(self):
        dict = self.tab.feature_dictionary
        new_feature_value = 'CAR'
        new_feature_key = (len(dict) + 1) * self.tab.increment_number
        self.tab.feature_dictionary[new_feature_key] = new_feature_value

        self.assertEqual(self.tab.find_name(new_feature_key), new_feature_value)
        del self.tab.feature_dictionary[new_feature_key]

    def test_find_id(self):
        dict = self.tab.feature_dictionary
        new_feature_value = 'CAR'
        new_feature_key = (len(dict) + 1) * self.tab.increment_number
        self.tab.feature_dictionary[new_feature_key] = new_feature_value

        self.assertEqual(self.tab.find_id(new_feature_value), new_feature_key)
        del self.tab.feature_dictionary[new_feature_key]

    def test_add_feature(self):
        dict = self.tab.feature_dictionary
        new_feature_value = 'car'
        new_feature_key = len(dict) * self.tab.increment_number
        self.tab.feature_dictionary[new_feature_key] = new_feature_value

        self.assertEqual(self.tab.add_feature(new_feature_value), True)
        self.assertEqual(self.tab.feature_dictionary[new_feature_key], new_feature_value)
        self.assertEqual(self.tab.add_feature(new_feature_value), False)
        del self.tab.feature_dictionary[new_feature_key]

    def test_get_all_feature(self):
        dict = self.tab.feature_dictionary
        new_feature_value = 'car'
        new_feature_key = (len(dict) + 1) * self.tab.increment_number
        self.tab.feature_dictionary[new_feature_key] = new_feature_value

        self.assertEqual(len(self.tab.find_all_features()), 5)
        del self.tab.feature_dictionary[new_feature_key]

if __name__ == "__main__":
    unittest.main()