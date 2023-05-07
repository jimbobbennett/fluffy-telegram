from io import BytesIO

from PIL import Image


def resize_image(buffer: BytesIO) -> BytesIO:
    '''
    Resizes an image to 480x320 and returns the image as a JPEG buffer

    :param buffer: The image buffer to resize
    :type buffer: BytesIO
    :return: The resized image buffer
    :rtype: BytesIO
    '''
    # Open the image from the buffer using Pillow
    image = Image.open(buffer)

    # Resize the image
    image = make_rectangle(image)

    # Save the image to the buffer in JPEG format
    thumbnail_buffer = BytesIO()
    image.save(thumbnail_buffer, format="JPEG")

    # Return the buffer
    return thumbnail_buffer


def make_rectangle(image: Image) -> Image:
    '''
    Resizes an image to 480x320, by scaling and padding with black bars where necessary,
    and returns the image as a JPEG buffer.

    :param image: The image to resize
    :type image: Image
    :return: The resized image
    :rtype: Image
    '''
    # Size the image
    image.thumbnail((480, 320))

    # Create a new blank black image with the correct size and paste the image into it
    x, y = image.size
    new_image = Image.new(image.mode, (480, 320), (0, 0, 0))
    new_image.paste(image, (int((480 - x) / 2), int((320 - y) / 2)))

    # Return the image
    return new_image
