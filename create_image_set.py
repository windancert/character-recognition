# This Python file uses the following encoding: utf-8

import locations
from image_set import ImageSet

lines_image_set = ImageSet(locations.LOCATION_LINES)
lines_image_set.clear()
lines_image_set.create_artificial_set_for_characters(r"-|+\/", 25, 5)
