# This Python file uses the following encoding: utf-8

from numpy import ndarray
import numpy
from sklearn.neural_network import MLPClassifier

from classification import Classification

class NeuralNetworkClassification(Classification):
    def __init__(self):
        super().__init__()
        self.__classifier = MLPClassifier((100, 50))

    def train_on_matrix(self, images_as_matrix: ndarray, classifications_as_vector: ndarray):
        self.__classifier.fit(images_as_matrix, classifications_as_vector)

    def classifiy_from_vector(self, image_as_vector: ndarray) -> int:
        result = self.__classifier.predict(image_as_vector.reshape(1, -1))
        return int(result)
