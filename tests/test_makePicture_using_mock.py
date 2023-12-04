import unittest
from unittest.mock import patch, MagicMock
from PIL import Image
from siena_mls import makePicture, JESImage 

class TestMakePicture(unittest.TestCase):
    @patch('siena_mls.Image.open') 
    @patch('siena_mls.JESImage')  
    def test_makePicture(self, mock_JESImage, mock_open):
        # Mock the Image object returned by Image.open
        mock_img = MagicMock(spec=Image.Image)
        mock_img.height = 500
        mock_img.width = 500
        mock_img.mode = 'RGB'
        mock_open.return_value = mock_img

        # Call the function with a test filename
        result = makePicture('test_filename')

        # Check that Image.open was called with the correct argument
        mock_open.assert_called_once_with('test_filename')

        # Check that JESImage was called with the correct arguments
        mock_JESImage.assert_called_once_with(mock_img, 'test_filename')

        # Check that the result is the mock JESImage instance
        self.assertEqual(result, mock_JESImage.return_value)
        print("Done")

if __name__ == '__main__':
    unittest.main()