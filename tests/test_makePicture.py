import unittest
from siena_mls import makePicture

class TestMakePicture(unittest.TestCase):
    def test_valid_image(self):
        picture = makePicture("tests/assets/siena-small-logo.png")
        self.assertIsNotNone(picture)

if __name__ == '__main__':
    unittest.main()
