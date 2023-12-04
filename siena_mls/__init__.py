##########################################
# JES Media Functions, Version 18
#
# Adapted from the textbook Introduction
# to Computing and Programming in PYTHON:
# A multimedia Approach
# by Mark Guzdial and Barbara Ericson
#
# DO NOT MODIFY ANY CODE IN THIS FILE!
#
# Authors: Robin Flatland and Ninad Chaudhari @SienaCollege
##########################################

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from scipy.io import wavfile
import sys
import math
import numpy
import PIL
import warnings
from os import walk
from os import listdir
import glob

#Replit Extension
from resizeimage import resizeimage
from pi_heif import register_heif_opener

register_heif_opener()

# To enable getting MES version using __version__
from importlib import metadata
__version__ = metadata.version("Siena-MLS")
class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'


JESColorWrapAround = False  #by default
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
magenta = (255, 0, 255)
orange = (255, 165, 0)
pink = (255, 20, 147)
gray = (165, 165, 165)
darkGray = (120, 120, 120)
lightGray = (210, 210, 210)


# Encapsulates the JESPixel data , which includes:
# Data type     Name             Description
# JESImage      self.JESimg      a JESImage object
# integer       self.x           pixel's x (column) location
# integer       self.y           pixel's y (row) location
class JESPixel:

  def __init__(self, JESimg, x, y):
    self.JESimg = JESimg
    self.x = x
    self.y = y

  def __str__(self):
    return "Pixel at (" + str(self.x) + "," + str(self.y) + ") red=" + str(
        getRed(self)) + " green=" + str(getGreen(self)) + " blue=" + str(
            getBlue(self))


# Encapsulates the JESSample data , which includes:
# Data type     Name             Description
# JESSound      self.JESsnd      a JESSound object
# integer       self.index       sample's index
class JESSample:

  def __init__(self, JESsnd, index):
    self.JESsnd = JESsnd
    self.index = index

  def __str__(self):
    return "Sample at index " + str(self.index) + " with value " + str(
        self.JESsnd.samples[self.index])


# Encapsulates the JESImage data , which includes:
# Data type     Name             Description
# PIL.Image     self.PILimg      a PIL.Image object
# string        self.filename    name of the image file
class JESImage:
  # constructor
  def __init__(self, PILimg, filename):
    self.PILimg = PILimg
    self.filename = filename

  # Used when print is called on a JESImage object.
  # Simulates JES behavior (see pg 28 of Guzdial/Ericson text)
  def __str__(self):
    return "Picture, filename " + self.filename + "\n   height " + str(
        self.PILimg.height) + " width " + str(self.PILimg.width)


# Encapsulates the JESSound data , which includes:
# Data type     Name             Description
# integer       self.sampleRate  the sample rate
# numpy.array   self.samples     1D array of sample values of type numpy.int16
# string        self.filename    name of sound file
class JESSound:
  # constructor
  def __init__(self, sampleRate, samples, filename):
    self.sampleRate = sampleRate
    self.samples = samples
    self.filename = filename

  def __str__(self):
    return "Sound, filename " + self.filename + "\n   number of samples " + str(
        len(self.samples)) + " sample rate " + str(self.sampleRate)


#########################################################
# JES Image Functions
#########################################################
def makePicture(filename):
  """
    Creates and returns a JESImage object from the specified image file.

    This function opens an image file and automatically resizes it if its area exceeds 360,000 pixels. It converts images in "RGBA" and "P" modes to "RGB".

    Args:
        filename (str): The path of the image file to be opened.

    Returns:
        JESImage: An object representing the opened image.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        IOError: If the file cannot be opened or read.
  """
  PILimg = Image.open(filename)
  iArea = PILimg.height * PILimg.width
  print(PILimg.mode)

  if (iArea > 360000):
    print(
        f"{bcolors.WARNING}Note: makePicture has automatically resized this image to better work with replit :) You are all set, Enjoy!{bcolors.ENDC}"
    )

    PILimg = resizeimage.resize_thumbnail(PILimg, [600, 600])
  if PILimg.mode in ("RGBA", "P"): PILimg = PILimg.convert("RGB")
  return JESImage(PILimg, filename)


# #Custom
# def showImage(JESimg):
#   win = Tk()
#   # Define the geometry of the window
#   win.geometry("700x500")

#   frame = Frame(win, width=600, height=400)
#   frame.pack()
#   frame.place(anchor='center', relx=0.5, rely=0.5)

#   # Create an object of tkinter ImageTk
#   img = ImageTk.PhotoImage(JESimg)

#   # Create a Label Widget to display the text or Image
#   label = Label(frame, image=img)
#   label.pack()

#   win.mainloop()


def makeEmptyPicture(width, height, color=(255, 255, 255)):
  """
    Creates an empty JESImage object with the specified dimensions and background color.

    Args:
        width (int): The width of the image in pixels.
        height (int): The height of the image in pixels.
        color (tuple, optional): The background color of the image, specified as a tuple of RGB values. Defaults to white (255, 255, 255).

    Returns:
        JESImage: An empty image with the specified dimensions and background color.
  """
  PILimg = PIL.Image.new("RGB", (int(width), int(height)), color)
  return JESImage(PILimg, "noFileName")


def duplicatePicture(JESimg):
  dup = JESimg.PILimg.copy()
  return JESImage(dup, "noFileName")


def copyInto(smJESimg, lgJESimg, startX, startY):
  lgJESimg.PILimg.paste(smJESimg.PILimg, (int(startX), int(startY)))


def setAllPixelsToAColor(JESimg, color):
  for y in range(0, getHeight(JESimg)):
    for x in range(0, getWidth(JESimg)):
      p = getPixel(JESimg, x, y)
      setColor(p, color)


def getWidth(JESimg):
  return JESimg.PILimg.width


def getHeight(JESimg):
  return JESimg.PILimg.height


def getPixel(JESimg, x, y):
  """
    Retrieves a JESPixel object representing the pixel at the specified coordinates in the given JESImage.

    Args:
        JESimg (JESImage): The image from which to retrieve the pixel.
        x (int): The x-coordinate (column) of the pixel.
        y (int): The y-coordinate (row) of the pixel.

    Returns:
        JESPixel: The pixel at the specified coordinates.

    Raises:
        RuntimeError: If the x or y coordinates are out of the image's range.
    """
  outOfXRange = ((x < 0) or (x >= getWidth(JESimg)))
  outOfYRange = ((y < 0) or (y >= getHeight(JESimg)))
  if (outOfXRange):
    raise RuntimeError(
        "getPixel(pic, x, y): x was out of range, either it was larger than (getWidth(pic) - 1) or it was less than 0."
    )
  if (outOfYRange):
    raise RuntimeError(
        "getPixel(pic, x, y): y was out of range, either it was larger than (getHeight(pic) - 1) or it was less than 0."
    )
  return JESPixel(JESimg, int(x), int(y))


def getPixels(JESimg):
  allPixels = []
  for y in range(0, getHeight(JESimg)):
    for x in range(0, getWidth(JESimg)):
      allPixels.append(getPixel(JESimg, x, y))
  return allPixels


def getAllPixels(JESimg):
  return getPixels(JESimg)


# helper function, not a JES function
def JESWrapAroundValue(value):
  global JESColorWrapAround
  value = int(value)
  if (JESColorWrapAround == True):
    value = value % 256
  elif value > 255:
    value = 255
  elif value < 0:
    value = 0
  return value


def setRed(JESpix, red):
  red = JESWrapAroundValue(red)
  color = JESpix.JESimg.PILimg.getpixel((JESpix.x, JESpix.y))
  JESpix.JESimg.PILimg.putpixel((JESpix.x, JESpix.y),
                                (red, color[1], color[2]))


def setBlue(JESpix, blue):
  blue = JESWrapAroundValue(blue)
  color = JESpix.JESimg.PILimg.getpixel((JESpix.x, JESpix.y))
  JESpix.JESimg.PILimg.putpixel((JESpix.x, JESpix.y),
                                (color[0], color[1], blue))


def setGreen(JESpix, green):
  green = JESWrapAroundValue(green)
  color = JESpix.JESimg.PILimg.getpixel((JESpix.x, JESpix.y))
  JESpix.JESimg.PILimg.putpixel((JESpix.x, JESpix.y),
                                (color[0], green, color[2]))


def getRed(JESpix: JESPixel) -> int:
  color = JESpix.JESimg.PILimg.getpixel((JESpix.x, JESpix.y))
  return color[0]


def getBlue(JESpix):
  color = JESpix.JESimg.PILimg.getpixel((JESpix.x, JESpix.y))
  return color[2]


def getGreen(JESpix):
  color = JESpix.JESimg.PILimg.getpixel((JESpix.x, JESpix.y))
  return color[1]


def getColor(JESpix):
  return JESpix.JESimg.PILimg.getpixel((JESpix.x, JESpix.y))


def setColor(JESpix, color):
  r = JESWrapAroundValue(color[0])
  g = JESWrapAroundValue(color[1])
  b = JESWrapAroundValue(color[2])
  JESpix.JESimg.PILimg.putpixel((JESpix.x, JESpix.y), (r, g, b))


def setColorWrapAround(flag):
  global JESColorWrapAround
  if (flag != True) and (flag != False):
    print(
        "setColorWrapAround( flag ): input flag must be either 1 (True) or 0 (False)  "
    )
  else:
    JESColorWrapAround = flag


def getColorWrapAround():
  global JESColorWrapAround
  return JESColorWrapAround


def makeColor(r, g, b):
  r = JESWrapAroundValue(r)
  g = JESWrapAroundValue(g)
  b = JESWrapAroundValue(b)
  return (r, g, b)


def makeDarker(color):
  r = int(color[0] * 0.80)
  g = int(color[1] * 0.80)
  b = int(color[2] * 0.80)
  return (r, g, b)


def makeLighter(color):
  r = min(255, int(color[0] * 1.10))
  g = min(255, int(color[1] * 1.10))
  b = min(255, int(color[2] * 1.10))
  return (r, g, b)


def makeBrighter(color):
  makeLighter(color)


def getX(JESpix):
  return JESpix.x


def getY(JESpix):
  return JESpix.y


def distance(c1, c2):
  dist = (c1[0] - c2[0])**2 + (c1[1] - c2[1])**2 + (c1[2] - c2[2])**2
  return math.sqrt(dist)


def writePictureTo(JESimg, filename):
  """
    Saves the provided JESImage object to a file with the specified filename.

    This function writes the image in the JESImage object to a file. The filename extension determines the format of the saved image. Currently, it supports saving in JPEG and PNG formats. The function raises an error if the filename does not have an appropriate extension.

    Args:
        JESimg (JESImage): The JESImage object to be saved.
        filename (str): The path and name of the file where the image will be saved. Must end with '.jpg', '.jpeg', or '.png'.

    Raises:
        RuntimeError: If the filename does not end with '.jpg', '.jpeg', or '.png'.

    Examples:
        >>> img = makePicture("path/to/image.jpg")
        >>> writePictureTo(img, "path/to/save/image.jpg") # Saves the image in JPEG format.
        >>> writePictureTo(img, "path/to/save/image.png") # Saves the image in PNG format.
    """
  # determine if jpg extension on filename
  index = filename.rfind(".")
  if (index == -1):  # extension not found
    raise RuntimeError(
        "writePictureTo(pic, filename): filename must have either a .jpg, .jpeg, or .png extension"
    )
  extension = filename[index:len(filename)]
  if ((extension == ".jpg") or (extension == ".jpeg")):
    JESimg.PILimg.save(filename, format="JPEG")
  elif (extension == ".png"):
    JESimg.PILimg.save(filename, format="PNG")
  else:
    raise RuntimeError(
        "writePictureTo(pic, filename): filename must have a .jpg, .jpeg, or .png extension"
    )


def addText(JESimg, xpos, ypos, text, size, color=(0, 0, 0)):
  # get font
  fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                           size)
  #fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', size)
  # get a drawing context
  d = ImageDraw.Draw(JESimg.PILimg, mode="RGB")
  # draw text, full opacity
  d.text((int(xpos), int(ypos)), text, font=fnt, fill=color)


def addTextWithStyle(JESimg, xpos, ypos, text, style, color=(0, 0, 0)):
  # get a drawing context
  d = ImageDraw.Draw(JESimg.PILimg, mode="RGB")
  # draw text, full opacity
  d.text((int(xpos), int(ypos)), text, font=style, fill=color)


# only allows the size of the font to change
# because I'm not sure what other fonts are available on repl...
def makeStyle(fontName, emphasis, size):
  return ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', int(size))


def addRect(JESimg, startX, startY, width, height, color=(0, 0, 0)):
  d = ImageDraw.Draw(JESimg.PILimg, mode="RGB")
  d.rectangle(
      [int(startX),
       int(startY),
       int(startX + width),
       int(startY + height)],
      outline=color,
      fill=None)


def addRectFilled(JESimg, startX, startY, width, height, color=(0, 0, 0)):
  d = ImageDraw.Draw(JESimg.PILimg, mode="RGB")
  d.rectangle(
      [int(startX),
       int(startY),
       int(startX + width),
       int(startY + height)],
      outline=color,
      fill=color)


def addLine(JESimg, startX, startY, endX, endY, color=(0, 0, 0)):
  d = ImageDraw.Draw(JESimg.PILimg, mode="RGB")
  d.line([int(startX), int(startY), int(endX), int(endY)], fill=color, width=2)


def addOval(JESimg, startX, startY, width, height, color=(0, 0, 0)):
  d = ImageDraw.Draw(JESimg.PILimg, mode="RGB")
  d.ellipse(
      [int(startX),
       int(startY),
       int(startX + width),
       int(startY + height)],
      outline=color,
      fill=None)


def addOvalFilled(JESimg, startX, startY, width, height, color=(0, 0, 0)):
  d = ImageDraw.Draw(JESimg.PILimg, mode="RGB")
  d.ellipse(
      [int(startX),
       int(startY),
       int(startX + width),
       int(startY + height)],
      outline=color,
      fill=color)


def addArc(JESimg,
           startX,
           startY,
           width,
           height,
           start,
           angle,
           color=(0, 0, 0)):
  d = ImageDraw.Draw(JESimg.PILimg, mode="RGB")
  d.arc([int(startX),
         int(startY),
         int(startX + width),
         int(startY + height)],
        int(360 - start - angle),
        int(360 - start),
        fill=color)


def addArcFilled(JESimg,
                 startX,
                 startY,
                 width,
                 height,
                 start,
                 angle,
                 color=(0, 0, 0)):
  d = ImageDraw.Draw(JESimg.PILimg, mode="RGB")
  d.pieslice(
      [int(startX),
       int(startY),
       int(startX + width),
       int(startY + height)],
      int(360 - start - angle),
      int(360 - start),
      outline=color,
      fill=color)


#########################################################
# JES Sound Functions
#########################################################
def makeSound(filename):
  """
    Creates and returns a JESSound object from the specified audio file.

    This function reads an audio file and creates a JESSound object. 
    It handles mono audio directly, and for stereo audio, it extracts and uses the first channel only. 

    Args:
        filename (str): The path of the audio file to be opened.

    Returns:
        JESSound: An object representing the opened audio file.

    Raises:
        FileNotFoundError: If the specified audio file does not exist.
        IOError: If the file cannot be opened, read, or is in an unsupported format.
        Warning: If any issues are encountered during the reading of the file.

    Examples:
        >>> snd = makeSound("path/to/sound.wav")
        >>> # snd is now a JESSound object representing the sound file.
  """
  warnings.filterwarnings("ignore")
  sampleRate, samples = wavfile.read(filename)
  # Check and see if samples is single channel (mono).
  # It is mono if samples[0] is a number, it is
  # multi-channeled if samples[0] is a numpy.ndarray
  if (type(samples[0]) is numpy.ndarray):
    # copy data from 1st channel into data (make it mono)
    data = numpy.zeros(len(samples), dtype=numpy.int16)
    for i in range(0, len(samples)):
      data[i] = samples[i][0]  # take just 1st channel
  else:
    data = numpy.copy(samples)
  # samples is read-only array, so make copy that is writeable
  return JESSound(sampleRate, data, filename)


def writeSoundTo(JESsnd, filename):
    """
    Saves the provided JESSound object to a file with the specified filename.

    This function writes the sound data contained in the JESSound object to an audio file. The format of the saved audio is determined by the file extension of the specified filename. Currently, it supports WAV format. The function raises an error if the filename does not have an appropriate extension.

    Args:
        JESsnd (JESSound): The JESSound object to be saved.
        filename (str): The path and name of the file where the sound will be saved. Must end with '.wav'.

    Raises:
        RuntimeError: If the filename does not end with '.wav'.
        IOError: If there's an error in writing the file.

    Examples:
        >>> snd = makeSound("path/to/sound.wav")
        >>> writeSoundTo(snd, "path/to/save/sound.wav") # Saves the sound in WAV format.
    """
    #print(JESsnd.samples)
    wavfile.write(filename, JESsnd.sampleRate, JESsnd.samples)


def getLength(JESsnd):
  return len(JESsnd.samples)


def getNumSamples(JESsnd):
  return getLength(JESsnd)


def getSampleValueAt(JESsnd, index):
    """
    Retrieves the sample value at a specified index in a JESSound object.

    This function returns the value of the audio sample at the given index from the JESSound object. The index should be within the range of the sound's length. 

    Args:
        JESsnd (JESSound): The JESSound object containing the sound samples.
        index (int): The index of the sample value to retrieve.

    Returns:
        int: The sample value at the specified index.

    Raises:
        IndexError: If the index is out of the range of the sound's sample array.

    Examples:
        >>> snd = makeSound("path/to/sound.wav")
        >>> value = getSampleValueAt(snd, 0) # Retrieves the first sample value.
    """
    return JESsnd.samples[index]


def setSampleValueAt(JESsnd, index, val):
    """
    Sets the sample value at a specified index in a JESSound object.

    This function updates the value of the audio sample at the given index in the JESSound object. The index should be within the range of the sound's length, and the value should be within the audio's valid sample value range.

    Args:
        JESsnd (JESSound): The JESSound object containing the sound samples.
        index (int): The index of the sample value to set.
        val (int): The new value to set for the sample at the specified index.

    Raises:
        IndexError: If the index is out of the range of the sound's sample array.
        ValueError: If the provided value is outside the permissible range for audio samples.

    Examples:
        >>> snd = makeSound("path/to/sound.wav")
        >>> setSampleValueAt(snd, 0, 123) # Sets the first sample value to 123.
    """
    JESsnd.samples[index] = val


def getSamplingRate(JESsnd):
  return JESsnd.sampleRate


def getSound(JESsam):
  return JESsam.JESsnd


def getSampleValue(JESsam):
  return JESsam.JESsnd.samples[JESsam.index]


def setSampleValue(JESsam, value):
  JESsam.JESsnd.samples[JESsam.index] = value


def getSampleObjectAt(JESsnd, index):
  return JESSample(JESsnd, index)


def getDuration(JESsnd):
  return getLength(JESsnd) / getSamplingRate(JESsnd)


def getSamples(JESsnd):
  allSamples = []
  for index in range(0, getLength(JESsnd)):
    allSamples.append(getSampleObjectAt(JESsnd, index))
  return allSamples


def duplicateSound(JESsnd):
  return JESSound(JESsnd.sampleRate, numpy.copy(JESsnd.samples), "noFileName")


def makeEmptySound(numSamples, sampleRate=22050):
  if ((numSamples <= 0) or (sampleRate <= 0)):
    raise RuntimeError(
        "makeEmptySound(numSamples[, sampleRate]): numSamples and sampleRate must each be greater than 0"
    )
  if (numSamples / sampleRate > 400):
    raise RuntimeError(
        "makeEmptySound(numSamples[, sampleRate]): empty sound length must not exceed 400 seconds"
    )
  samples = numpy.zeros(numSamples, dtype=numpy.int16)
  return JESSound(sampleRate, samples, "noname")


def makeEmptySoundBySeconds(duration, sampleRate=22050):
  if (sampleRate <= 0):
    raise RuntimeError(
        "makeEmptySoundBySeconds(duration[, sampleRate]): sampleRate must be greater than 0"
    )
  if (duration > 400):
    raise RuntimeError(
        "makeEmptySoundBySeconds(numSamples[, sampleRate]): empty sound length must not exceed 400 seconds"
    )
  samples = numpy.zeros(int(duration * sampleRate), dtype=numpy.int16)
  return JESSound(sampleRate, samples, "noname")


# Animation
#


# returns a list of all files in the folder
def fileList(folder):
  found_files = []
  for (dirpath, dirnames, filenames) in walk(folder):
    found_files.extend(filenames)
    break
  return found_files


def writeMovieTo(images, filename):

  images[0].save(filename,
                 save_all=True,
                 append_images=images[1:],
                 optimize=False,
                 duration=40)  #loop=3)


def makeMovieFromInitialFile(firstFile):
  # Extract path and fileName from firstFile.
  # E.g., if firstFile is animation\frame020.jpg
  # then path will be animation and fileName
  # will be frame020.jpg
  # valid path deliminators are //, /, and \
  if "//" in firstFile:
    path = firstFile[0:firstFile.rfind("//")]
    fileName = firstFile[firstFile.rfind("//") + 2:len(firstFile)]
  elif "/" in firstFile:
    path = firstFile[0:firstFile.rfind("/")]
    fileName = firstFile[firstFile.rfind("/") + 1:len(firstFile)]
  elif "\\" in firstFile:
    path = firstFile[0:firstFile.rfind("\\")]
    fileName = firstFile[firstFile.rfind("\\") + 1:len(firstFile)]
  else:
    path = ""
    fileName = firstFile

  # get names of all files in the folder and
  # then sort them
  imageFiles = fileList(path)
  imageFiles.sort()

  # find fileName in the list of files in the folder
  try:
    index = imageFiles.index(fileName)
  except ValueError:
    # fileName not in list
    raise RuntimeError(
        "makeMovieFromInitialFile(firstFile)#: did not find a file with that name"
    )

  # remove all names that come before fileName
  imageFiles = imageFiles[index:len(imageFiles)]
  # read in images and put into a list
  images = []
  for f in imageFiles:
    pic = makePicture(path + "//" + f)
    images.append(pic.PILimg)

  return images


def writeAnimatedGif(movie, fileName, frameRate=24):
  if frameRate <= 0:
    raise RuntimeError(
        "writeAnimatedGIF(movie, filename[, frameRate]): frameRate must be greater than zero"
    )
  movie[0].save(fileName,
                save_all=True,
                append_images=movie[1:],
                optimize=False,
                duration=1000 / frameRate,
                loop=0)


def writeSlideShowTo(fileName, delay=1):
  # get names of all files in the folder
  allFiles = []
  for fn in listdir():
    allFiles.append(fn)

  # create list containing only
  # files that start with slide
  # and end with jpg or jpeg
  slideFiles = []
  for fn in allFiles:
    if fn.startswith("slide") and (fn.endswith(".jpg")
                                   or fn.endswith(".jpeg")):
      slideFiles.append(fn)
  slideFiles.sort()

  # read in images and put into a list
  images = []
  for fn in slideFiles:
    pic = makePicture(fn)
    images.append(pic.PILimg)

  # write images as animated gif
  writeAnimatedGif(images, fileName, 1.0 / delay)


# RETURNS a new sound that is the portion of "source" from "start" to "end"
# doesn't alter the original sound
def clip(source, start, end):
  target = makeEmptySound(end - start)
  targetIndex = 0
  for sourceIndex in range(start, end):
    sourceValue = getSampleValueAt(source, sourceIndex)
    setSampleValueAt(target, targetIndex, sourceValue)
    targetIndex = targetIndex + 1
  return target


# copies the "source" sound into the "target" sound starting at "start" in "target"
def copy(source, target, start):
  targetIndex = start
  for sourceIndex in range(0, getLength(source)):
    sourceValue = getSampleValueAt(source, sourceIndex)
    setSampleValueAt(target, targetIndex, sourceValue)
    targetIndex = targetIndex + 1


# Implementation notes
#
# Implementation of JES image/sound functions
#
# Version 18 4/14/2022
#
# Replit changed something or libraries were
# upgraded, and it resulted in new fonts located
# in a new location.  This broke the addText
# function.  Modified it to look in the right place
# for one of the newly available fonts.
#
# Version 17 3/31/2021
#
# Had trouble installing and running opencv.
# But we were only using it for AVI movies, which are
# not part of the curriculum.  So opencv (cv2) and
# the two AVI movie functions were removed.  JES
# runs now.  Not sure why we started getting
# issues with cv2. Something on replit's end
# must have changed and caused the
# problem, as best I can tell.
#
# Version 16 11/1/2020
#
# modified makeMovieFromInitialFile to allow for "/" or "//"
# or "\\" path delimiters
#
# Version 15  10/23/2020
#  problem occur with "import ImageDraw" when poetry and
#  and pyproject.toml files are not provided with repl. Changed
#  this to from PIL import ImageDraw and this fixes the problem
#  Same change made for ImageFont.
#
# Version 14  10/20/2020
#   switched getPixels to return a list of pixels
#   in row order, rather than column order
#
# Version 13 10/6/2020
#   added clip/copy functions for Lab 6
#
# Version 12 8/24/2020 for Img Seq project
#   added writeSlideShowTo function
#
# Version 11, 8/4/2020, Robin Flatland
#
#  8/4/2020
#     writePictureTo allows .jpeg file extension
#  7/30/2020
#     added size input to addText
#     fixed addArcFilled so that it
#     fills the spanned angle.
#  7/23/2020
#    fixed colorWrapAround to mod by 256
#      rather than 255
#    writePictureTo can write
#      either png or jpg images
#      now, depending on the
#      file extension.
#    getPixel now raises a runtime Exception
#       if x or y is out of range
#  7/20/2020
#    took out sys.exit() and sys.quit() &
#      replaced with raising RuntimeException
#      because the exit/quit were resetting the
#      console and forcing the play button to be pressed
#
# Status of implementation of JES functions
#
# For images, all functions are implemented
# except for:
# makeStyle - only partially implemented.
#    Currently it only allows the font size
#    to change. You cannot change the font
#    type or the font formatting (like bold,
#    italics, etc...) Need to check the default
#    font size also, to see if it is approx.
#    the same as the default in JES.
# pickAColor, pickAFile - WILL NOT BE IMPLEMENTED
# show, repaint - WILL NOT BE IMPLEMENTED
#
# For sounds, all functions are implemented
# except for:
# play, stopPlaying, blockingPlay - WILL NOT BE IMPLEMENTED
# playNote - WILL NOT BE IMPLEMENTED
#
# For animation, we only implemented the functions
# necessary for the animation project.  Note that
# repl did not allow for easy viewing of AVI movies,
# so for the course we are going with generating
# an animated GIF instead (using the first two
# functions below). Note that the last three functions
# do not exist in JES by these names:
#    makeMovieFromInitialFile
#    writeAnimatedGif (new function) - one
#       thing is that the animation
#       plays repeatedly.  Did not find a
#       way to make it play only once.
#    makeAVIMovieFromInitialFile (new function)
#    writeAVI (new function)
#
