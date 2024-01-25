from siena_mls import *
a = makePicture("tests/assets/siena-poster_resized.jpeg")
addRect(a, 10, 10, 100, 50, white)
showImage(a)
writePictureTo(a, "dut.jpg")