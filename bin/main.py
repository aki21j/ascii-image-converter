from PIL import Image
import math
from colorama import Fore, Style
import sys

BRIGHTNESS_TYPES = {
    "AVERAGE": "average",
    "LIGHTNESS": "lightness",
    "LUMINOSITY": "luminosity"
}

ASCII_SUBSTRATE_SCALE = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
MAX_BRIGHTNESS = 255
bp_scale = MAX_BRIGHTNESS / len(ASCII_SUBSTRATE_SCALE)


def get_pixel_matrix(img, height):
    img.thumbnail((height, 200))
    pixels = list(img.getdata())
    pixel_matrix = []
    for i in range(0, len(pixels), img.width):
        pixel_matrix.append(pixels[i:i+img.width])
    return pixel_matrix


def create_brightness_matrix(pixel_matrix, brightness_type):
    brightness_matrix = []
    for row in pixel_matrix:
        brightness_row = []
        for pixel in row:
            if brightness_type == BRIGHTNESS_TYPES.get("AVERAGE"):
                brightness_row.append((pixel[0] + pixel[1] + pixel[2]) / 3)
            elif brightness_type == BRIGHTNESS_TYPES.get("LIGHTNESS"):
                brightness_row.append((max(pixel) + min(pixel)) / 2)
            elif brightness_type == BRIGHTNESS_TYPES.get("LUMINOSITY"):
                brightness_row.append((0.21 * pixel[0]) + (0.72 * pixel[1]) + (0.07 * pixel[2]))
        brightness_matrix.append(brightness_row)
    return brightness_matrix


# invert brightness, white to black and vice versa
def invert_brightness_matrix(brightness_matrix):
    inverted_matrix = []
    for row in brightness_matrix:
        inverted_row = []
        for pixel in row:
            inverted_pixel = MAX_BRIGHTNESS - pixel
            inverted_row.append(inverted_pixel)
        inverted_matrix.append(inverted_row)
    return inverted_matrix


def meth_ascii_matrix(brightness_matrix):
    ascii_matrix = []
    for row in brightness_matrix:
        ascii_row = []
        for pixel in row:
            try:
                ascii_row.append(ASCII_SUBSTRATE_SCALE[round(pixel/bp_scale)])
            except Exception as e:
                ascii_row.append(ASCII_SUBSTRATE_SCALE[math.floor(pixel/bp_scale)])
        ascii_matrix.append(ascii_row)
    return ascii_matrix


def main():
    infile_path = sys.argv[1]
    im = Image.open(infile_path)
    pixel_matrix = get_pixel_matrix(im, 1000)

    brightness_matrix = create_brightness_matrix(pixel_matrix,BRIGHTNESS_TYPES.get("LUMINOSITY"))
    inverted_matrix = invert_brightness_matrix(brightness_matrix)
    ascii_matrix = meth_ascii_matrix(inverted_matrix)

    for row in ascii_matrix:
        line = [p+p+p for p in row]
        print("".join(line))
    print(Style.RESET_ALL)


if __name__ == "__main__":
    main()
