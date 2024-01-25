import unittest
import os
from PIL import Image, ImageChops
from siena_mls import makePicture, addRectFilled, white, writePictureTo

class TestResizeLargeImage(unittest.TestCase):
    def setUp(self):
        self.exif_modified_image_path = 'tests/assets/siena_poster_exif_modified.jpeg'  
        self.expected_image_path = 'tests/assets/siena_poster_exif_modified_expected.jpeg'  
        self.temp_image_path = 'tests/assets/exif_temp.jpeg'
    # def tearDown(self):
    #     # This should be
    #     if os.path.exists(self.temp_image_path):
    #         os.remove(self.temp_image_path)

    def test_resize_large_image(self):
        myPic = makePicture(self.exif_modified_image_path)
        addRectFilled(myPic, 10, 10, 100, 50, white)
        writePictureTo(myPic, self.temp_image_path)
        
        # Check if this new image matches the model image that has been resized as expected
        with Image.open(self.expected_image_path) as expected, Image.open(self.temp_image_path) as modified:

            # Check that the processed image matches the expected image
            diff = ImageChops.difference(expected, modified)
            self.assertTrue(not diff.getbbox())

if __name__ == '__main__':
    unittest.main()