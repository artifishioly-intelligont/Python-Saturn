def download(file_name, local_dest):
	urllib.urlretrieve("http://degas.ecs.soton.ac.uk/~productizer/%s" % file_name , local_dest)
