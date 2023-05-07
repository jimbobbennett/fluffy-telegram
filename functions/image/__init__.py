import logging
import shared.storage as storage

import azure.functions as func

import shared.validation as validation


def get(req: func.HttpRequest, device: str) -> func.HttpResponse:
    '''
    This function handles the GET request for the HTTP trigger.

    It handles the following scenarios:
    - If an image is specified, return that image
    - If no image is specified, return all images

    :param req: The HTTP request
    :type req: func.HttpRequest
    :param device: The device to get the images for
    :type device: str
    :return: The HTTP response
    :rtype: func.HttpResponse
    '''
    # get the parameters for the request - if an image is specified, return that image, otherwise return all images
    image = req.params.get('image')
    if image:
        logging.info(f'Image: {image}')
        return func.HttpResponse(body=storage.get_image(device, image).getvalue(), mimetype='image/jpeg')
    else:
        return func.HttpResponse(body=storage.get_all_images(device), mimetype='application/json')


def post(req: func.HttpRequest, device: str) -> func.HttpResponse:
    '''
    This function handles the POST request for the HTTP trigger.

    It handles the following scenarios:
    - If an image_url is specified, upload that image
    - If an image is specified in the body, upload that image

    If the image is uploaded successfully, return a 200
    If the image is malicious, return a 403

    :param req: The HTTP request
    :type req: func.HttpRequest
    :param device: The device to upload the image for
    :type device: str
    :return: The HTTP response
    :rtype: func.HttpResponse
    '''
    # get the parameters for the request - if an image_url is specified, upload that image, otherwise upload the body
    image_url = req.params.get('image_url')

    if image_url:
        logging.info(f'Image URL: {image_url}')

        # Check if the URL is malicious, and if so, return a 403
        if validation.is_url_malicious(image_url):
            logging.info('Malicious URL - this image will not be loaded')
            return func.HttpResponse('Malicious URL', status_code=403)

        storage.upload_image_from_url(device, image_url)

        # Return a 200
        return func.HttpResponse('ok')
    else:
        body = req.get_body()
        logging.info(f'Received body, length {len(body)}')

        # Check if the file is malicious, and if so, return a 403
        if validation.is_file_malicious(body):
            logging.info('Malicious file - this image will not be loaded')
            return func.HttpResponse('Malicious file', status_code=403)

        # Upload the image
        storage.upload_image(device, body)

        # Return a 200
        return func.HttpResponse('ok')


def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    This function is the entry point for the HTTP trigger.

    It handles the following verbs:
    - GET: Returns a list of images for the device, or the image specified
    - POST: Uploads an image to the device from an image as a binary body, or from a URL

    :param req: The HTTP request
    :type req: func.HttpRequest
    :return: The HTTP response
    :rtype: func.HttpResponse
    '''
    logging.info('Python HTTP trigger function processed a request.')

    # Get the device from the route parameters
    device = req.route_params.get('device')
    logging.info(f'Device {device}')

    # Verify we have a device
    if not device:
        return func.HttpResponse('Device not specified', status_code=400)

    # Handle the request based on the method
    if req.method.lower() == 'get':
        return get(req, device)
    elif req.method.lower() == 'post':
        return post(req, device)

    # For other verbs, drop out and return a 404
    return func.HttpResponse('Method not supported', status_code=405)
