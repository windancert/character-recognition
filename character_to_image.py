# This Python file uses the following encoding: utf-8

from pathlib import Path
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont

def create_image_from_character_in_file(filename: Path, character: str, image_width: int, image_height: int,
                                        offset_x: float=0.0, offset_y: float=0.0) -> None:
    img = create_image_for_character(character, image_width, image_height, offset_x, offset_y)
    img.save(filename)

def create_image_for_character(character: str, image_width: int, image_height: int, 
                               offset_x: float=0.0, offset_y: float=0.0) -> Image:
    grey_scale_mode = "L"
    img = Image.new(grey_scale_mode, size=(image_width, image_height))
    img.paste( (255,), (0, 0, image_width, image_height))
    courier = ImageFont.truetype('Courier', 64)
    draw = ImageDraw.Draw(img)
    text_width, text_height = draw.textsize(character, font=courier)
    location = __get_location_for_text(image_width, image_height, text_width, text_height, offset_x, offset_y)
    draw.text(location, character, font=courier, fill=(0,))
    return img

def __get_location_for_text(image_width: int, image_height: int, text_width: int, text_height: int,
                            offset_x: float, offset_y: float) -> Tuple:
    location_x = (image_width-text_width)//2 + round(offset_x)
    location_y = (image_height-text_height)//2 + round(offset_y)
    return location_x, location_y
