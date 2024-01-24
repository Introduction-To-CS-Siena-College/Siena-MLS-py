import unittest
from siena_mls import makePicture

class TestMakePicture(unittest.TestCase):
    def test_valid_image(self):
        with self.subTest("Testing with valid image"):
            picture = makePicture("tests/assets/siena-small-logo.png")
            self.assertIsNotNone(picture, "The picture should not be None")

if __name__ == '__main__':
    unittest.main()
