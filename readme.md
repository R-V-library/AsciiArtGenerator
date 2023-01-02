# ASCII ART GENERATOR: contents
CLI tool to convert images to ascii art
- [Overview](#overview)
- [Usage](#usage)
- [How it works](#how-it-works)
- [Dependencies](#dependencies)

## Overview
This CLI program can be used to convert images in popular formats (.jpg, .png, .gif etc.) into ASCII art.

## Usage
1. Setup environment by running the sourceme.sh bash script
> `source sourceme.sh -a`
2. To see all CLI parameters and their functions type:
> `ascii_art_generator -h/--help`

## How it works
When an image is loaded as a greyscale image, the RGB pixel values are converted into one 8-bit number (value: 0-255).
This 8-bit number is subsequently mapped onto an array of ascii characters. <br>
An example of ascii char mapping: [example ascii char mapping](http://mewbies.com/geek_fun_files/ascii/ascii_art_light_scale_and_gray_scale_chart.htm)

Additionally an output colour can be specified. This functionality uses the ascii escape codes to colour the output when viewed in a terminal. <br>
[Info about terminal colours](https://chrisyeh96.github.io/2020/03/28/terminal-colors.html)

## Dependencies
This program uses the opencv library for image processing.
The install guide for the opencv library can be found at: <br>
[Opencv installation docs](https://docs.opencv.org/4.7.0/da/df6/tutorial_py_table_of_contents_setup.html)
