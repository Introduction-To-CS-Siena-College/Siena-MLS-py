from siena_mls import *
# OR: from JES import *
a = makePicture("tests/assets/siena-poster_resized_model.jpeg")
addRectFilled(a, 10, 10, 100, 50, white)
showImage(a)
writePictureTo(a, "out.jpg")