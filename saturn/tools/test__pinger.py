import unittest
import os
import subprocess
from pinger import post_request
import time


class PingerTest(unittest.TestCase):

    def setUp(self):
        # Run the server via command line
        server_loc = os.path.expanduser('~') + '/SaturnServer/test_resources/dummy.py'
        self.p = subprocess.Popen(["python", server_loc])
        time.sleep(5)

    def test_pinger(self):

        #given a url and package
        self.url = 'http://127.0.0.1:25565/post'
        self.package = [1.2, 2.2, 3.2, 4.2, 5.2]

        #when the parameters are fed into the pinger method which will use the url to send the package to diff server
        result = post_request(self.url, self.package)

        # the result should be true
        self.assertEqual(result, "Pass")

        #close a server
        self.p.kill()

if __name__ == "__main__":
    unittest.main()