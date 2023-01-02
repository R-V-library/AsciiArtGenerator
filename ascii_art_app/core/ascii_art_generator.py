import numpy as np
import cv2 as cv
import os
import sys
import errno
import logging


class AsciiArtGenerator:
    def __init__(self):
        self.grey = None
        self.median = None

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s : %(levelname)s : %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.logger = logging.getLogger()

    def enable_logging(self):
        self.logger.setLevel(level=logging.DEBUG)
        self.logger.debug("Logging enabled")

    def load_image(self, filepath):
        try:
            if os.path.isfile(filepath):
                self.grey = cv.imread(filepath, cv.COLOR_BGR2GRAY)

                if self.grey is None:
                    self.logger.debug("Error loading file")
                    raise TypeError("Filetype not supported")

            else:
                self.logger.debug("Error opening file")
                raise FileNotFoundError(
                    errno.ENOENT, os.strerror(errno.ENOENT), filepath
                )
        except OSError:
            raise

        self.median = np.median(np.ndarray.flatten(self.grey))
        self.logger.debug("Done loading image file")

    def trim_whitespace(self):
        canny = self.extract_edges()

        coords = cv.findNonZero(canny)
        x, y, w, h = cv.boundingRect(coords)

        self.grey = self.grey[y : y + h, x : x + w]
        self.logger.debug("Done trimming whitespace")

    def resize_image(self, max_height, max_width):
        if (max_height <= 0) or (max_width <= 0):
            self.logger.debug(
                f"max_height: {max_height} and max_width: {max_width} should be greater than 0"
            )
            raise ValueError("Invalid max size arguments")

        if self.grey.shape[0] > self.grey.shape[1]:
            scaling_factor = max_height / self.grey.shape[0]
        else:
            scaling_factor = max_width / self.grey.shape[1]

        self.logger.debug(f"Scaling image with scaling factor: {scaling_factor}")

        self.grey = cv.resize(
            self.grey,
            None,
            fx=scaling_factor,
            fy=scaling_factor,
            interpolation=cv.INTER_AREA,
        )
        self.logger.debug("Done resizing image")

    def extract_edges(self):
        lower_boundary = int(0.66 * self.median)
        upper_boundary = int(1.33 * self.median)
        canny = cv.Canny(self.grey, lower_boundary, upper_boundary)
        self.logger.debug("Done extracting edges")
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

                else:
                    raise NotImplementedError("Invalid argument(s) received")

        except OSError as e:
            if e.errno == errno.ENOENT:
                sys.exit(1)
            elif e.errno == errno.EISDIR:
                raise IsADirectoryError(
                    "Filepath points to directory instead of file"
                ) from e
            else:
                raise

        self.logger.debug("Done generating output")

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
            "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,^`'."
        )
        ASCII_RESOLUTION = round(256 / len(ASCII_ARRAY))

        if colour:
            outfile.write(self.get_colour_prefix(colour))

        for i in range(self.grey.shape[0]):
            for j in range(self.grey.shape[1]):
                greyvalue = self.grey[i, j][0]
                if greyvalue < self.median:  # TODO: improve
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
                if greyvalue > self.median:  # TODO: improve
                    ascii_char = "*"
                else:
                    ascii_char = " "
                outfile.write(ascii_char)
            outfile.write("\n")

        if colour:
            outfile.write("\x1b[0m")

        outfile.close()
