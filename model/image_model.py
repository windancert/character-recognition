# This Python file uses encoding: utf-8

from pathlib import Path
from typing import Optional

import PIL
from PIL.Image import Image
from PyQt5.QtCore import QObject, pyqtSignal


class ImageModel(QObject):

    image_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.__image_path: Optional[Path] = None
        self.__image: Optional[Image] = None
        self.__convert_to_black_and_white: bool = False

    def get_image_to_show(self) -> Optional[Image]:
        return self.__image


    def load_image(self, path_to_file: Path) -> None:
        self.__image_path = path_to_file
        self.__image = PIL.Image.open(self.__image_path)
        self.image_changed.emit()

