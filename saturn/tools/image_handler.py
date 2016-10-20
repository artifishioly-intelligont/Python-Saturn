
import os
from datetime import datetime

def get_datetime():
    return str(datetime.now().strftime('%d.%m.%Y_%H.%M.%S'))

class ImageHandler:
    imageDir = '!Image Dir Not Set!'

    def __init__(self):
        self.imageDir = '%s/SaturnServer/images/' % os.path.expanduser('~')

    def get_image_dir(self):
        return self.imageDir

    def new_location(self):
        return '%smap__%s' % (self.get_image_dir(), get_datetime())


