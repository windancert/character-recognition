# This Python file uses the following encoding: utf-8

from random import sample

from chopper import chop_image
from image_set import ImageSet
from locations import LOCATION_LINES
from neural_network_classification import NeuralNetworkClassification

from PIL import Image

image_set = ImageSet(LOCATION_LINES)
classifier = NeuralNetworkClassification()
image_data = image_set.get_data()
classifier.train(image_data)

for character, image in sample(image_data, 10):
    inferred_character = classifier.classifiy(image)
    print(f"Classified as {inferred_character}, was {character}" + (" FAILED" if character != inferred_character else ""))

paard = Image.open(r"images\obama.jpg").convert('L')
images = chop_image(paard, 10, 15)

for row in images:
    for i in row:
        c = classifier.classifiy(i)
        print(c, end='')
    print(" ")
