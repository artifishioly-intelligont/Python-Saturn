#!/usr/bin/python

import urllib

def download(file_name, local_dest):
	urllib.urlretrieve("http://degas.ecs.soton.ac.uk/~productizer/%s" % file_name , local_dest)


if __name__ == '__main__':
        download('images/windmill.jpg','download.jpg')