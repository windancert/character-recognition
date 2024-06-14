# This Python file uses the following encoding: utf-8

from abc import ABC, abstractmethod
from typing import List, Tuple

from numpy import ndarray
import numpy
from PIL.Image import Image

class Classification(ABC):
    def __init__(self):
        self.__classification_to_index = {}
        self.__index_to_classification = {}

    def train(self, data: List[Tuple[str, Image]]):
        classifications, images = zip(*data)
        self.__create_character_index_mappings(classifications)
        images_as_matrix = self.__create_matrix_of_images(images)
        classifications_as_matrix = self.__create_vector_of_classifications(classifications)
        self.train_on_matrix(images_as_matrix, classifications_as_matrix)            

    def classifiy(self, image: Image) -> str:
        index = self.classifiy_from_vector(self.__convert_image_to_1d_array(image))
        if index not in self.__index_to_classification:
            raise Exception(f"Classification failed, returned index = {index}, possible indices {self.__index_to_classification.keys()}")
        return self.__index_to_classification[index]
        
    @abstractmethod
    def train_on_matrix(self, images_as_matrix: ndarray, classifications_as_vector: ndarray):
        pass

    @abstractmethod
    def classifiy_from_vector(self, image_as_vector: ndarray) -> int:
        pass

    def __create_character_index_mappings(self, classifications: Tuple[str, ...]) -> None:
        unique_classifications = set(classifications)
        self.__classification_to_index = {c:i for i, c in enumerate(unique_classifications)}
        self.__index_to_classification = {i:c for c, i in self.__classification_to_index.items()}

    def __create_vector_of_classifications(self, classifications: Tuple[str, ...]) -> ndarray:
        if self.__classification_to_index is None:
            raise Exception("Classification has not been trained yet")
        return numpy.asarray([self.__classification_to_index[c] for c in classifications])

    def __create_matrix_of_images(self, images:Tuple[Image, ...]) -> ndarray:
        nbr_images = len(images)
        image_sizes = set([i.size for i in images])
        if len(image_sizes) != 1:
            raise Exception(f"Found the following image sizes: {image_sizes}, expected only 1")
        image_size = image_sizes.pop()
        nbr_pixels = image_size[0] * image_size[1]
        images_as_matrix = numpy.ndarray((nbr_images, nbr_pixels))
        for i, image in enumerate(images):
            images_as_matrix[i,:] = self.__convert_image_to_1d_array(image)
        return images_as_matrix
        

    def __convert_image_to_1d_array(self, image: Image):
        return numpy.asarray(image).reshape(-1)
    