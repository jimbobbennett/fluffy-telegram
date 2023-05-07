from io import BytesIO
import os
import requests
import uuid

from azure.storage.blob import BlobServiceClient
from azure.storage.queue import QueueServiceClient

from PIL import Image

import shared.imageutils as imageutils

connection_string = os.environ['BLOB_STORAGE_CONNECTION_STRING']

blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_name = "images"
container_client = blob_service_client.get_container_client(container_name)

queue_service_client = QueueServiceClient.from_connection_string(connection_string)


def get_all_images(device: str) -> str:
    '''
    Returns a list of all images for a device

    :param device: The device to get the images for
    :type device: str
    :return: A list of all images for the device as JSON
    :rtype: str
    '''

    # Get a list of blobs for the device
    blobs = container_client.list_blobs(name_starts_with=f'{device}/')

    # return the blob list as json
    return '[{}]'.format(','.join([f'"{blob.name.replace(f"{device}/", "")}"' for blob in blobs]))


def get_image(device: str, image_name: str) -> BytesIO:
    '''
    Returns an image with the given name from the blob storage.

    :param device: The device to get the image for
    :type device: str
    :param image_name: The name of the image to get
    :type image_name: str
    :return: The image as a JPEG buffer
    :rtype: BytesIO
    '''
    # Get the blob
    blob_client = container_client.get_blob_client(f'{device}/{image_name}')
    blob = blob_client.download_blob()

    # Read the blob into a buffer
    bytes = blob.readall()

    # Open the image from the buffer using Pillow
    image = Image.open(BytesIO(bytes))

    # Make the image a rectangle
    image = imageutils.make_rectangle(image)

    # Save the image to the buffer in JPEG format
    buffer = BytesIO()
    image.save(buffer, format="JPEG")

    # return the blob as the response
    buffer.seek(0)
    return buffer


def __resize_and_upload_image(device: str, image: bytes) -> str:
    '''
    Resizes an image to 480x320 and uploads it to the blob storage, then returns the image name.

    :param device: The device to upload the image for
    :type device: str
    :param image: The image to upload
    :type image: bytes
    :return: The image name
    :rtype: str
    '''
    # Open the image using Pillow
    thumbnail_buffer = imageutils.resize_image(BytesIO(image))

    # create a new uuid for the image
    image_name = f'{device}/{str(uuid.uuid4())}.jpg'

    # Save the image to the blob storage
    blob_client = container_client.get_blob_client(image_name)
    blob_client.upload_blob(thumbnail_buffer.getvalue(), overwrite=True)

    # Return the image name
    return image_name


def upload_image(device: str, image: bytes) -> None:
    '''
    Uploads an image to the blob storage, then writes a message to the queue with the image name
    '''
    # Resize and upload the image
    image_name = __resize_and_upload_image(device, image)

    # Write to the queue that we have written a new image
    send_image_to_queue(device, image_name)


def upload_image_from_url(device: str, image_url: str) -> None:
    '''
    Uploads an image from a URL to the blob storage, then writes a message to the queue with the image name.

    :param device: The device to upload the image for
    :type device: str
    :param image_url: The URL of the image to upload
    :type image_url: str
    '''
    # Download the image from the URL
    response = requests.get(image_url)

    # Get the binary data from the response
    image = response.content

    # create a new uuid for the image
    image_name = __resize_and_upload_image(device, image)

    # Write to the queue that we have written a new image
    send_image_to_queue(device, image_name)


def send_image_to_queue(device: str, image_name: str) -> None:
    '''
    Sends a message to the device queue that a new image has been uploaded.

    :param device: The device to send the message for
    :type device: str
    :param image_name: The name of the image that was uploaded
    :type image_name: str
    '''
    # Write to the queue that we have written a new image
    queue_name = f"images-{device}"
    queue_client = queue_service_client.get_queue_client(queue_name)
    queue_client.send_message(image_name)
