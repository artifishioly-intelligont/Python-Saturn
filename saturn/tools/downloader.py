import urllib

def download(file_name, local_dest):
	"""
	Downloads a file from any location on http://degas.ecs.soton.ac.uk/~productizer/

    :param file_name: where in the productizer space it is stored e.g. 'images/map1.jpg'
    :param local_dest: Where the file should be saved to e.g. ~/SaturnServer/images/map__20.10.2016_20.32.45.jpg
    """
	urllib.urlretrieve("http://degas.ecs.soton.ac.uk/~productizer/%s" % file_name, local_dest)
