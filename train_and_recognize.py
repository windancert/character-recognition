# This Python file uses the following encoding: utf-8

from random import sample

from image_set import ImageSet
from locations import LOCATION_LINES
from neural_network_classification import NeuralNetworkClassification

image_set = ImageSet(LOCATION_LINES)
classifier = NeuralNetworkClassification()
image_data = image_set.get_data()
classifier.train(image_data)

for character, image in sample(image_data, 10):
    inferred_character = classifier.classifiy(image)
    print(f"Classified as {inferred_character}, was {character}")
