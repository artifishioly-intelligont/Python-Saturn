import unittest
import __init__ as classifier

class TableUnitTest(unittest.TestCase):

    def setUp(self):
        self.tab = classifier.tab

    def test_add_feature(self):
        self.assertEqual(self.tab.add_feature('lake'), True)

    def test_get_all_feature(self):
        self.assertEqual(len(self.tab.find_all_features()), 5)

if __name__ == "__main__":
    unittest.main()