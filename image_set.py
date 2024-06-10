# This Python file uses the following encoding: utf-8

from itertools import repeat
import json
import os
from pathlib import Path
from urllib.parse import quote_plus
from statistics import NormalDist
from typing import Dict, Tuple

from PIL import Image, ImageFont, ImageDraw

MANIFEST_FILE_NAME = "manifest.json"
ARTIFICIAL_HEIGHT = 75
ARTIFICIAL_WIDTH = 50

class ImageSet:
    def __init__(self, directory: Path):
        self.__directory = directory
        self.__manifest: Dict = {}
        if self.manifest_filename.exists():
            with open(self.manifest_filename, 'r') as m:
                self.__manifest = json.load(m)
                if not isinstance(self.__manifest, dict):
                    raise Exception(f"Manifest in {self.__manifest_filename} is not recognized")

    @property
    def manifest_filename(self):
        return self.__get_path_from_filename(MANIFEST_FILE_NAME)

    @property
    def is_filled(self):
        return bool(self.__manifest)
    
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
                final_filename = quote_plus(candidate_filename)
                final_path = self.__get_path_from_filename(final_filename)
                self.__create_file(character, final_path, next(noise_iter), next(noise_iter))
                self.__manifest[character].append(final_filename)
        self.__write_manifest_file()

    def clear(self):
        for _, image_files in self.__manifest.items():
            for image_file in image_files:
                os.remove(self.__get_path_from_filename(image_file))
        os.remove(self.manifest_filename)
        self.__manifest = {}

    def __write_manifest_file(self):
        with open(self.manifest_filename, 'w') as f:
            json.dump(self.__manifest, f)

    def __create_file(self, character: str, filename: Path, offset_x: float=0.0, offset_y: float=0.0):
        grey_scale_mode = "L"
        img = Image.new(grey_scale_mode, size=(ARTIFICIAL_WIDTH, ARTIFICIAL_HEIGHT))
        img.paste( (255,), (0, 0, ARTIFICIAL_WIDTH, ARTIFICIAL_HEIGHT))
        courier = ImageFont.truetype('Courier', 64)
        draw = ImageDraw.Draw(img)
        size = draw.textsize(character, font=courier)
        location = self.__get_location_for_text(offset_x, offset_y, *size)
        draw.text(location, character, font=courier, fill=(0,))
        img.save(filename)

    def __get_location_for_text(self, offset_x: float, offset_y: float, width: int, height: int) -> Tuple:
        location_x = (ARTIFICIAL_WIDTH-width)//2 + round(offset_x)
        location_y = (ARTIFICIAL_HEIGHT-height)//2 + round(offset_y)
        return location_x, location_y
    
    def __get_path_from_filename(self, filename):
        return self.__directory / filename

