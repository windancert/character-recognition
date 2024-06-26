# This Python file uses the following encoding: utf-8

from itertools import repeat
import json
import os
from pathlib import Path
from pprint import pformat
from urllib.parse import quote
from statistics import NormalDist
from typing import Dict, List, Tuple

from PIL.Image import Image
import PIL

from character_to_image import create_image_from_character_in_file

MANIFEST_FILE_NAME = "manifest.json"
ARTIFICIAL_HEIGHT = 15
ARTIFICIAL_WIDTH = 10

class ImageSet:
    def __init__(self, directory: Path):
        self.__directory = directory
        self.__manifest: Dict = {}
        if self.manifest_filepath.exists():
            with open(self.manifest_filepath, 'r') as m:
                self.__manifest = json.load(m)
                if not isinstance(self.__manifest, dict):
                    raise Exception(f"Manifest in {self.__manifest_filename} is not recognized")

    @property
    def manifest_filepath(self):
        return self.__get_path_from_filename(MANIFEST_FILE_NAME)

    @property
    def is_filled(self):
        return bool(self.__manifest)
    
    @property
    def number_of_images(self) -> int:
        if self.is_filled:
            return sum(len(filenames) for filenames in self.__manifest.values())
        raise Exception("Image set has not been filled yet, could not determine number of images")
    
    @property 
    def number_of_pixels_per_image(self) -> int:
        if self.is_filled:
            first_image: Image = self.__get_first_image()
            width, height = first_image.size
            return width * height
        raise Exception("Image set has not been filled yet, could not determine number of pixels per image")
    
    def create_artificial_set_for_characters(self, characters: str, repeats: int=50, location_noise: float=0.0,
                                             random_seed: int=1973):
        if self.is_filled:
            raise Exception("Can not create articial image set in directory which already contains data")

        include_noise = (location_noise > 0)
        if include_noise:
            noise = NormalDist(0, location_noise).samples(2*repeats*len(characters), seed=random_seed)
            noise_iter = iter(noise)
        else:
            noise_iter = repeat(0.0)

        for character in characters:
            if character not in self.__manifest:
                self.__manifest[character] = []
            for i in range(1,repeats+1):
                candidate_filename = f"{character}_{i}.png"
                final_filename = quote(candidate_filename)
                final_path = self.__get_path_from_filename(final_filename)
                create_image_from_character_in_file(final_path, character, ARTIFICIAL_WIDTH, ARTIFICIAL_HEIGHT, 
                                                    next(noise_iter), next(noise_iter))
                self.__manifest[character].append(final_filename)
        self.__write_manifest_file()

    def clear(self):
        for _, image_files in self.__manifest.items():
            for image_file in image_files:
                os.remove(self.__get_path_from_filename(image_file))
        if self.manifest_filepath.exists():
            os.remove(self.manifest_filepath)
        self.__manifest = {}

    def get_data(self) -> List[Tuple[str, Image]]:
        if not self.is_filled:
            raise Exception("Can not get images from empty image set")
        result = []
        for character, filenames in self.__manifest.items():
            for filename in filenames:
                result.append( (character, PIL.Image.open(self.__get_path_from_filename(filename))))
        return result

    def __write_manifest_file(self):
        with open(self.manifest_filepath, 'w') as f:
            f.write(pformat(self.__manifest, indent=4, compact=True).replace("'",'"'))
            # json.dump(self.__manifest, f, indent=4)

    def __get_path_from_filename(self, filename):
        return self.__directory / filename

    def __get_first_image(self):
        for _, filenames in self.__manifest:
            return Image.open(self.__get_path_from_filename(filenames[0]))
        raise Exception("Image set not filled, could not obtain an image")
