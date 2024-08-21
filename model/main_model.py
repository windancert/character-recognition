# This Python file uses encoding: utf-8

from PyQt5.QtCore import QObject

from model.image_model import ImageModel
from model.text_model import TextModel


class MainModel(QObject):
    def __init__(self):
        super().__init__()
        self.__image_model = ImageModel()
        self.__text_model = TextModel()

    @property
    def image_model(self) -> ImageModel:
        return self.__image_model

    @property
    def text_model(self) -> TextModel:
        return self.__text_model
