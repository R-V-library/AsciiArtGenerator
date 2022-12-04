import numpy as np 
import cv2 as cv
import os
import sys
import errno
import logging

#from matplotlib import pyplot as plt

# load image 
img = cv.imread("./test_image.png")


# resize image 
#img = cv.resize(img,(50,50), interpolation=cv.INTER_CUBIC)

original_height = img.shape[0]
original_width = img.shape[1]

desired_height = 200 
desired_width = 30

# resize within max width/height
if original_height > original_width:
    scaling_factor = (desired_height/original_height)
else: 
    scaling_factor = (desired_width/original_width)
print(scaling_factor)
#print(img.shape[0], img.shape[1])

#print(height,width)

# scale image 
img = cv.resize(img, None, fx=scaling_factor,fy=scaling_factor, interpolation=cv.INTER_AREA)

# convert to greyscale
grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)


# spread greyscale accross the spectrum 
#clahe = cv.createCLAHE()
#grey = clahe.apply(grey)

#ascii_array = ["$","@","B","%","8","&","W","M","#","*","o","a","h","k","b","d","p","q","w",
#"m","Z","O","0","Q","L","C","J","U","Y","X","z","c","v","u","n","x","r","j","f","t","/","\","(",")","1","{","}","[","]","?",
#"-","_","+","~","<",">","i","!","l","I",";",":",",","^","`","'","."]

# ascii characters from dark to light
ascii_array = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`'."
#ascii_array[:-1]  

# make empty matrix to store chars 
height,width = grey.shape
print(width,height)

# perform edge detection 
#grey = cv.Canny(grey, 85, 170)

# binary thresholding
#grey = cv.adaptiveThreshold(grey,255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 0)

#char_matrix = [['' for j in range(width)] for i in range(height)] #np.zeros((width,height),dtype='S1')
#print(char_matrix.nbytes)

# fill matrix with ascii character
ascii_resolution = round(256/len(ascii_array))
f = open("testfile_4.txt","w")
for i in range(height):
    for j in range(width):
        greyvalue = grey[i,j]
        if greyvalue < 128: # split in middle of greyscale spectrum 
            ascii_char = ascii_array[(greyvalue // ascii_resolution )]
        else:
            ascii_char = ' '
        f.write(ascii_char)
    f.write("\n")
f.close()
print("done writing file")
        #print(ascii_char)
        #char_matrix[i][j] = ascii_char

# save to text 
#f = open("testfile_2.txt","w")
#f.write(str(char_matrix))
#f.close()

# spread greyscale accross the sprectrum 
#hist, bins = np.histogram(grey.flatten(), 256, [0,256])
#
#cdf = hist.cumsum()
#cdf_normalized = cdf * float(hist.max()) / cdf.max()
#
#plt.plot(cdf_normalized, color='b')
#plt.hist(img.flatten(),256,[0,256], color = 'r')
#plt.xlim([0,256])
#plt.legend(('cdf','histogram'), loc = 'upper left')
#plt.show()

#cv.imshow('test',grey)
#cv.waitKey(0)
#cv.destroyAllWindows()

class AsciiArtGenerator():
    def __init__(self):
        self.image = None
        self.grey = None

    def load_image(self, filepath):
        try:
            if os.path.isfile(filepath):
                self.image = cv.imread(filepath)
                self.grey = cv.imread(filepath, cv.COLOR_BGR2GRAY)

                if ((self.image == None) or (self.grey == None)):
                    raise TypeError("Filetype not supported")
            else:
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filepath)
        except OSError as e:
            if e.errno == errno.ENOENT:
                sys.exit(1)
            else:
                raise

    def trim_whitespace(self):
        #self.imageToGrey() 
        canny = self.extract_edges() # extract edges from greyscale image 

        #grey = 255*(grey < 128).astype(np.uint8) # To invert the text to white

        coords = cv.findNonZero(canny) # Find all non-zero points 
        x, y, w, h = cv.boundingRect(coords) # Find minimum spanning bounding box

        self.image = self.image[y:y+h, x:x+w] # Crop the original image
        self.grey = self.grey[y:y+h, x:x+w] # crop the grey image  
        #return image

    def resize_image(self, max_height, max_width):
        # calculate scaling depending on max amount of characters in one direction 
        original_height, original_width = self.image.shape

        # resize within max width/height
        if original_height > original_width:
            scaling_factor = (max_height/original_height)
        else: 
            scaling_factor = (max_width/original_width)
        print(scaling_factor)
        #print(img.shape[0], img.shape[1])

        #print(height,width)

        # scale image 
        self.image = cv.resize(self.image, None, fx=scaling_factor,fy=scaling_factor, interpolation=cv.INTER_AREA)
        self.grey = cv.resize(self.grey, None, fx=scaling_factor,fy=scaling_factor, interpolation=cv.INTER_AREA)
        #return image

    #def imageToGrey(self):
        #self.grey = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        #self.grey = grey
        #return grey

    def extract_edges(self):
        median_greyscale = np.median(np.flatten(self.grey))
        lower_boundary = int(0.66 * median_greyscale)
        upper_boundary = int(1.33 * median_greyscale)
        canny = cv.Canny(self.grey, lower_boundary, upper_boundary) 
        return canny

    def generate_output(self, filename, style, background):

        try:
            with open(filename, 'w') as outfile:
                # regular output (greyscale)
                if (style == "regular" ):
                    self.gen_regular_output(outfile)
                
                # only lines (edge detection)
                elif (style == "lines"):
                    self.gen_lines_output(outfile)

                # coloured regular "all" colours
                elif (style == "regular_coloured"):
                    self.gen_regular_coloured_output(outfile)

                # coloured regular 1 colour
                elif (style == "regular_unicolour"):
                    self.gen_regular_uni_coloured_output(outfile)


                # coloured edges 1 colour
                elif (style == "lines_unicolour"):
                    self.gen_lines_uni_coloured_output(outfile)

                # rubik's cube ascii coloured
                elif (style == "rubik"):
                    self.gen_rubik_output(outfile)

                # rubik's cube empty character only background colour
                elif (style == "rubik_background"):
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
    def gen_regular_output(self, outfile, background):
        return 0
    
    def gen_lines_output(self, outfile, background):
        return 0

    def gen_regular_coloured_output(self, outfile, background):
        return 0

    def gen_lines_uni_coloured_output(self, outfile, background):
        return 0

    def gen_rubik_output(self, outfile, background):
        return 0
    
    def gen_rubik_background_output(self, outfile, background):
        return 0
