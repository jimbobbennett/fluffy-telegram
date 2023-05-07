import logging
import os

import azure.functions as func
from azure.storage.blob import BlobServiceClient

connection_string = os.environ['BLOB_STORAGE_CONNECTION_STRING']

blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_name = "users"
container_client = blob_service_client.get_container_client(container_name)

# Get all blobs in the container
blobs = container_client.list_blobs()

# Add them to a dictionary
users = {}
for blob in blobs:
    # Load the blob content
    blob_client = container_client.get_blob_client(blob.name)
    blob_content = blob_client.download_blob().readall()
    user_name = blob.name.replace('.json', '')

    logging.info(f'Loading user user_name')

    users[user_name] = blob_content


def main(req: func.HttpRequest) -> func.HttpResponse:
    user_id = req.route_params.get('user_id')

    logging.info(f'Getting details for user {user_id}')

    if user_id in users:
        return func.HttpResponse(users[user_id], mimetype='application/json')

    return func.HttpResponse(f'User {user_id} not found', status_code=404)
