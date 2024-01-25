from siena_mls import *
a = makePicture("tests/assets/siena-poster.jpeg")
addRect(a, 10, 10, 100, 50, white)
writePictureTo(a, "dut.jpg")