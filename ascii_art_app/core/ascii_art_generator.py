import numpy as np
import cv2 as cv
import os
import sys
import errno

# import logging


class AsciiArtGenerator:
    def __init__(self):
        self.image = None
        self.grey = None

    def load_image(self, filepath):
        try:
            if os.path.isfile(filepath):
                self.image = cv.imread(filepath)
                self.grey = cv.imread(filepath, cv.COLOR_BGR2GRAY)

                if (self.image is None) or (self.grey is None):
                    raise TypeError("Filetype not supported")
            else:
                raise FileNotFoundError(
                    errno.ENOENT, os.strerror(errno.ENOENT), filepath
                )
        except OSError as e:
            if e.errno == errno.ENOENT:
                sys.exit(1)
            else:
                raise

    def trim_whitespace(self):
        # self.imageToGrey()
        canny = self.extract_edges()  # extract edges from greyscale image

        # grey = 255*(grey < 128).astype(np.uint8) # To invert the text to white

        coords = cv.findNonZero(canny)  # Find all non-zero points
        x, y, w, h = cv.boundingRect(coords)  # Find minimum spanning bounding box

        self.image = self.image[y : y + h, x : x + w]  # Crop the original image
        self.grey = self.grey[y : y + h, x : x + w]  # crop the grey image
        # return image

    def resize_image(self, max_height, max_width):
        # calculate scaling depending on max amount of characters in one direction
        original_height, original_width = self.image.shape

        # resize within max width/height
        if original_height > original_width:
            scaling_factor = max_height / original_height
        else:
            scaling_factor = max_width / original_width
        print(scaling_factor)
        # print(img.shape[0], img.shape[1])

        # print(height,width)

        # scale image
        self.image = cv.resize(
            self.image,
            None,
            fx=scaling_factor,
            fy=scaling_factor,
            interpolation=cv.INTER_AREA,
        )
        self.grey = cv.resize(
            self.grey,
            None,
            fx=scaling_factor,
            fy=scaling_factor,
            interpolation=cv.INTER_AREA,
        )
        # return image

    # def imageToGrey(self):
    # self.grey = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
    # self.grey = grey
    # return grey

    def extract_edges(self):
        median_greyscale = np.median(np.flatten(self.grey))
        lower_boundary = int(0.66 * median_greyscale)
        upper_boundary = int(1.33 * median_greyscale)
        canny = cv.Canny(self.grey, lower_boundary, upper_boundary)
        return canny

    def generate_output(self, filename, style):

        try:
            with open(filename, "w") as outfile:
                # regular output (greyscale)
                if style == "regular":
                    self.gen_regular_output(outfile)

                # only lines (edge detection)
                elif style == "lines":
                    self.gen_lines_output(outfile)

                # coloured regular "all" colours
                elif style == "regular_coloured":
                    self.gen_regular_coloured_output(outfile)

                # coloured regular 1 colour
                elif style == "regular_unicolour":
                    self.gen_regular_uni_coloured_output(outfile)

                # coloured edges 1 colour
                elif style == "lines_unicolour":
                    self.gen_lines_uni_coloured_output(outfile)

                # rubik's cube ascii coloured
                elif style == "rubik":
                    self.gen_rubik_output(outfile)

                # rubik's cube empty character only background colour
                elif style == "rubik_background":
                    self.gen_rubik_background_output(outfile)

                else:
                    raise NotImplementedError("Invalid arguments received")

        except OSError as e:
            if e.errno == errno.ENOENT:
                sys.exit(1)
            else:
                raise

    # DUMMIES
    # TODO: code real functions
    def gen_regular_output(self, outfile):
        ASCII_ARRAY = (
            "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`'."
        )

        ascii_resolution = round(256 / len(ASCII_ARRAY))

        height = self.grey.shape[0]
        width = self.grey.shape[1]
        for i in range(height):
            for j in range(width):
                greyvalue = self.grey[i, j]
                if greyvalue < 128:  # split in middle of greyscale spectrum
                    ascii_char = ASCII_ARRAY[(greyvalue // ascii_resolution)]
                else:
                    ascii_char = " "
                outfile.write(ascii_char)
            outfile.write("\n")
        outfile.close()
        print("done writing file")  # TODO: logging instead of print

    def gen_lines_output(self, outfile):
        return 0

    def gen_regular_coloured_output(self, outfile):
        return 0

    def gen_lines_uni_coloured_output(self, outfile):
        return 0

    def gen_rubik_output(self, outfile):
        return 0

    def gen_rubik_background_output(self, outfile):
        return 0
