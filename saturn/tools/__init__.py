"""
This module is reserved for arbitrary helper functions
"""
import os

from downloader import download
from image_handler import ImageHandler

images = ImageHandler('%s/SaturnServer/images/' % os.path.expanduser('~'))

