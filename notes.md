# Random notes that had to be written somewhere

Ignore for the most part.

## Exif Transformations

- Used the following website to change Exif orientation data https://www.imgonline.com.ua/eng/exif-editor.php 
- now modified the data for siena-poster, to confirm it shows as rotated. 
- Without the fix, it shows as straight (i.e. the exif data based transformations are ignored)
- After the fix it looks great.

This code demonstrate the ortientation exif

```python
from PIL import Image, ImageChops, ExifTags
original_image_path = 'tests/assets/siena-poster_resized.jpeg'  # replace with actual path
expected_image_path = 'tests/assets/rotate-180-resized.jpeg'  # replace with actual path
with Image.open(original_image_path) as original, Image.open(expected_image_path) as expected:
    img_exif = expected.getexif()
    print(type(img_exif))
    # <class 'PIL.Image.Exif'>

    if img_exif is None:
        print('Sorry, image has no exif data.')
    else:
        for key, val in img_exif.items():
            if key in ExifTags.TAGS:
                print(f'{ExifTags.TAGS[key]}:{val}')
            else:
                print(f'{key}:{val}')


```

## Exif modification called and there is some small diff change

These two images are basically just difference between resized when
exif based transforations are applied and when not. It gives a very small change
`(592, 312, 600, 315)` Interesting...

```python
from PIL import Image, ImageChops, ExifTags, ImageEnhance
original_image_path = 'tests/assets/siena-poster_resized_model.jpeg'  # replace with actual path
expected_image_path = 'tests/assets/siena-poster_resized.jpeg'  # replace with actual path
with Image.open(original_image_path) as original, Image.open(expected_image_path) as expected:
    diff = ImageChops.difference(original, expected)
    print(diff.getbbox())
    diff.show()
    enhancer = ImageEnhance.Contrast(diff)
    enhanced_diff = enhancer.enhance(2.0)  # Increase the contrast by a factor of 2
    enhanced_diff.save('enhanced_difference_image.jpg')
``````
