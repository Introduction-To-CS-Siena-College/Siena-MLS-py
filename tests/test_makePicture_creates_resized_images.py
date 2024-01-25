import unittest
import os
from PIL import Image, ImageChops
from siena_mls import makePicture, JESImage

class TestResizeLargeImage(unittest.TestCase):
    def setUp(self):
        self.test_image_path = 'tests/assets/siena-poster.jpeg'
        self.expected_resized_image_path = 'tests/assets/siena-poster_resized.jpeg'  
        self.model_resized_image_path = 'tests/assets/siena-poster_resized_model.jpeg'  


    def tearDown(self):
        # This should be
        if os.path.exists(self.expected_resized_image_path):
            os.remove(self.expected_resized_image_path)

    def test_resize_large_image(self):
        myPic = makePicture(self.test_image_path)
        # Check that the resized image was created
        self.assertTrue(os.path.exists(self.expected_resized_image_path))

        # Check that the resized image has the correct dimensions
        with Image.open(self.expected_resized_image_path) as img:
            width, height = img.size
            self.assertEqual(max(width, height), 600)
        # # Check if this new image matches the model image that has been resized as expected
        # with Image.open(self.model_resized_image_path) as model, Image.open(self.expected_resized_image_path) as resized:

        #     # Check that the processed image matches the expected image
        #     diff = ImageChops.difference(model, resized)
        #     self.assertTrue(not diff.getbbox(), "The resized image does not match the model image")

if __name__ == '__main__':
    unittest.main()