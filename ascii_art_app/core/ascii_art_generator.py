import numpy as np
import cv2 as cv
import os
import sys
import errno
import logging


class AsciiArtGenerator:
    def __init__(self):
        self.image = None
        self.grey = None

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s : %(levelname)s : %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.logger = logging.getLogger()

    def enable_logging(self):
        self.logger.setLevel(level=logging.DEBUG)

    def load_image(self, filepath):
        try:
            if os.path.isfile(filepath):
                self.image = cv.imread(filepath, cv.COLOR_BGR2HSV)
                print(self.image.shape)
                self.grey = cv.imread(filepath, cv.COLOR_BGR2GRAY)

                if (self.image is None) or (self.grey is None):
                    self.logger.debug("Error loading file")
                    raise TypeError("Filetype not supported")

            else:
                self.logger.debug("Error opening file")
                raise FileNotFoundError(
                    errno.ENOENT, os.strerror(errno.ENOENT), filepath
                )
        except OSError as e:
            if e.errno == errno.ENOENT:
                sys.exit(1)
            else:
                raise
        self.logger.debug("Done loading image files")

    def trim_whitespace(self):
        canny = self.extract_edges()  # extract edges from greyscale image

        coords = cv.findNonZero(canny)  # Find all non-zero points
        x, y, w, h = cv.boundingRect(coords)  # Find minimum spanning bounding box

        self.image = self.image[y : y + h, x : x + w]  # Crop the original image
        self.grey = self.grey[y : y + h, x : x + w]  # crop the grey image
        self.logger.debug("Done trimming whitespace")

    def resize_image(self, max_height, max_width):
        # calculate scaling depending on max amount of characters in one direction
        # original_height, original_width, _ = self.grey.shape

        print(max_height, max_width)
        print(self.grey.shape[0], self.grey.shape[1])
        # resize within max width/height
        # if original_height > original_width:
        if self.grey.shape[0] > self.grey.shape[1]:
            scaling_factor = max_height / self.image.shape[0]
            grey_scaling_factor = max_height / self.grey.shape[0]  # original_height
        else:
            scaling_factor = max_width / self.image.shape[1]
            grey_scaling_factor = max_width / self.grey.shape[1]  # original_width

        self.logger.debug(f"Scaling image with scaling factor: {scaling_factor}")

        # scale image
        self.image = cv.resize(
            self.image,
            None,
            fx=scaling_factor,
            fy=scaling_factor,
            interpolation=cv.INTER_AREA,
        )
        print(scaling_factor, self.image.shape)
        self.grey = cv.resize(
            self.grey,
            None,
            fx=grey_scaling_factor,
            fy=grey_scaling_factor,
            interpolation=cv.INTER_AREA,
        )
        self.logger.debug("Done resizing image")

    def extract_edges(self):
        median_greyscale = np.median(np.ndarray.flatten(self.grey))
        lower_boundary = int(0.66 * median_greyscale)
        upper_boundary = int(1.33 * median_greyscale)
        canny = cv.Canny(self.grey, lower_boundary, upper_boundary)
        self.logger.debug("Done extracting edges")
        # print(canny)
        # self.grey = canny
        return canny

    def generate_output(self, filename, style, colour):
        try:
            with open(filename, "w") as outfile:
                # regular output (greyscale)
                if style == "regular":
                    self.gen_regular_output(outfile, colour)

                # only lines (edge detection)
                elif style == "lines":
                    self.gen_lines_output(outfile, colour)

                # coloured regular "all" colours
                elif style == "regular_coloured":
                    self.gen_regular_coloured_output(outfile)

                # TODO: write function to output
                # coloured regular 1 colour
                elif style == "regular_unicolour":
                    self.gen_regular_uni_coloured_output(outfile)

                # TODO: remove
                # coloured edges 1 colour
                elif style == "lines_unicolour":
                    self.extract_edges()
                    self.gen_lines_uni_coloured_output(outfile)

                # TODO: write function for rubik style output
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

        self.logger.debug("Done generating output")

    # TODO: code real functions
    # TODO: code generic reusable function

    def get_colour_prefix(self, colour):
        colour_prefix = ""
        if colour:
            if colour == "black":
                colour_prefix = "\x1b[30m"

            elif colour == "red":
                colour_prefix = "\x1b[31m"

            elif colour == "green":
                colour_prefix = "\x1b[32m"

            elif colour == "yellow":
                colour_prefix = "\x1b[33m"

            elif colour == "blue":
                colour_prefix = "\x1b[34m"

            elif colour == "magenta":
                colour_prefix = "\x1b[35m"

            elif colour == "cyan":
                colour_prefix = "\x1b[36m"

            elif colour == "white":
                colour_prefix = "\x1b[37m"

            else:
                self.logger.debug("Invalid colour argument")
                raise NotImplementedError

            return colour_prefix

    def gen_regular_output(self, outfile, colour=None):
        ASCII_ARRAY = (
            "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`'."
        )
        ASCII_RESOLUTION = round(256 / len(ASCII_ARRAY))

        if colour:
            outfile.write(self.get_colour_prefix(colour))

        for i in range(self.grey.shape[0]):
            for j in range(self.grey.shape[1]):
                greyvalue = self.grey[i, j][0]
                if (
                    greyvalue < 128  # self.median_greyscale
                ):  # split in middle of greyscale spectrum TODO: improve, use median?
                    ascii_char = ASCII_ARRAY[(greyvalue // ASCII_RESOLUTION)]
                else:
                    ascii_char = " "
                outfile.write(ascii_char)
            outfile.write("\n")

        if colour:
            outfile.write("\x1b[0m")

        outfile.close()

    def gen_lines_output(self, outfile, colour=None):
        if colour:
            outfile.write(self.get_colour_prefix(colour))

        self.grey = self.extract_edges()

        for i in range(self.grey.shape[0]):
            for j in range(self.grey.shape[1]):
                greyvalue = self.grey[i, j]
                if greyvalue > 128:
                    ascii_char = "*"
                else:
                    ascii_char = " "
                outfile.write(ascii_char)
            outfile.write("\n")

        if colour:
            outfile.write("\x1b[0m")

        outfile.close()

    def gen_rubik_output(self, outfile):  # TODO: width must be multiple of 3
        ascii_char = "*"

        line_split = 0
        column_split = 0
        print(self.image.shape)
        for i in range(self.image.shape[0]):
            for j in range(self.image.shape[1]):
                pixvalue = np.array(self.image[i, j][0:3])
                prefix = self.extract_colour(
                    pixvalue
                )  # TODO: extract colour from pixel
                outfile.write(prefix + ascii_char + "\x1b[0m")
                column_split += 1
                if column_split % 3 == 0:
                    outfile.write("|")
                    column_split = 0
            line_split += 1
            if (line_split % 3) == 0:
                outfile.write("-" * self.grey.shape[1])
                line_split = 0
            outfile.write("\n")

        outfile.close()

    def gen_regular_coloured_output(
        self, outfile
    ):  # TODO: determine limit when to insert character and when not
        ASCII_ARRAY = (
            "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`'."
        )
        ASCII_RESOLUTION = round(256 / len(ASCII_ARRAY))
        for i in range(self.image.shape[0]):
            for j in range(self.image.shape[1]):
                pixvalue = np.array(self.image[i, j][0:3])
                prefix = self.extract_colour(pixvalue)
                ascii_char = ASCII_ARRAY[-(self.image[i, j][2] // ASCII_RESOLUTION)]
                outfile.write(prefix + ascii_char + "\x1b[0m")
            outfile.write("\n")

        outfile.close()

        return 0

    def extract_colour(self, pixel):  # TODO: tune colours, invert ?
        #        print(pixel)
        if pixel[0] < 10:
            return self.get_colour_prefix("white")
        elif pixel[0] > 10 and pixel[0] < 40:
            return self.get_colour_prefix("red")
        elif pixel[0] > 40 and pixel[0] < 80:
            return self.get_colour_prefix("green")
        elif pixel[0] > 80 and pixel[0] < 120:
            return self.get_colour_prefix("yellow")
        elif pixel[0] > 120 and pixel[0] < 160:
            return self.get_colour_prefix("blue")
        elif pixel[0] > 160 and pixel[0] < 200:
            return self.get_colour_prefix("magenta")
        elif pixel[0] > 200 and pixel[0] < 240:
            return self.get_colour_prefix("cyan")
        else:
            return self.get_colour_prefix("black")
