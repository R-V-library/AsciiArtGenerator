import os
import sys
import argparse

from .version import __version__
from .core.ascii_art_generator import AsciiArtGenerator


class App:
    def __init__(self):
        self.parse_config()
        self.build_argparse()

    def parse_config(self):
        if "PRJROOT" not in os.environ:
            raise RuntimeError("$PRJROOT was not set")

    def build_argparse(self):
        self.parser = argparse.ArgumentParser(
            prog="ASCII ART GENERATOR", description="Ascii art generator options"
        )

        self.parser.add_argument("filename", metavar="filename")

        self.parser.add_argument(
            "-c",
            "--colour",
            # action="store_true",
            default="",
            choices=[
                "black",
                "red",
                "green",
                "yellow",
                "blue",
                "magenta",
                "cyan",
                "white",
            ],
            help="Select output colour",
        )

        self.parser.add_argument(
            "-d", "--debug", action="store_true", default=False, help="Show debug logs"
        )

        self.parser.add_argument(
            "-l",
            "--max-lines",
            # action="store_true",
            type=int,
            default="200",
            help="Set max amount of lines",
        )

        self.parser.add_argument(
            "-o",
            "--output-dir",
            # action="store_true",
            type=str,
            default="./output.txt",
            help="Set output file name and directory",
        )

        self.parser.add_argument(
            "-s",
            "--style",
            # action="store_true",
            default="regular",
            choices=[
                "regular",
                "lines",
                "regular_coloured",
                "regular_unicolour",
                "lines_unicolour",
                "rubik",
                "rubik_background",
            ],
            help="Choose output style",
        )

        self.parser.add_argument(
            "-t",
            "--trim-whitespace",
            action="store_true",
            default=False,
            help="Trim image whitespace before converting to ascii art",
        )

        self.parser.add_argument(
            "-v", "--version", action="store_true", help="Ascii art generator version"
        )

        self.parser.add_argument(
            "-w",
            "--max-characters",
            # action="store_true",
            type=int,
            default="200",
            help="Set max amount of characters per line",
        )

    def run(self, argv):
        args = self.parser.parse_args(argv)

        if args.version:
            print(f"ASCII ART GENERATOR {__version__}")
            sys.exit(1)

        self.do_run(args)

    # TODO: define statemachine depending on arguments from parser
    def do_run(self, args):
        generator = AsciiArtGenerator()

        if args.debug:
            generator.enable_logging()

        generator.load_image(args.filename)

        if args.trim_whitespace:
            generator.trim_whitespace()

        generator.resize_image(args.max_lines, args.max_characters)

        generator.generate_output(args.output_dir, args.style, args.colour)
