from typing import List

from PIL.Image import Image


def chop_image(image: Image, character_width: int, character_height: int) -> List[List]:
    nbr_width_chops = image.width // character_width
    nbr_height_chops = image.height // character_height
    result = []
    for y in range(nbr_height_chops-1):
        row = []
        for x in range(nbr_width_chops-1):
            box = (x*character_width, y*character_height,  (x + 1) * character_width, (y + 1) * character_height)
            row.append(image.crop(box))
        result.append(row)
    return result
