import dotenv
import os
import pathlib
import time

from azure.storage.blob import BlobServiceClient
from azure.storage.queue import QueueServiceClient

current_path = pathlib.Path(__file__).parent.resolve()

dotenv.load_dotenv()

connection_string = os.getenv("STORAGE_CONNECTION_STRING")
device_id = os.getenv("DEVICE_ID")

queue_service_client = QueueServiceClient.from_connection_string(connection_string)
queue_name = f"images-{device_id}"
queue_client = queue_service_client.get_queue_client(queue_name)

blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_name = "images"
container_client = blob_service_client.get_container_client(container_name)

# Download all blobs from the container
blobs = container_client.list_blobs()
for blob in blobs:
    if blob.name.startswith(f"{device_id}/"):

        print(f"Downloading {blob.name}")

        blob_client = container_client.get_blob_client(blob.name)
        file_name = blob.name.split("/")[-1]

        # Check if the file exists
        if not os.path.exists(f'{current_path}/images/{file_name}'):

            with open(f'{current_path}/images/{file_name}', "wb") as f:
                data = blob_client.download_blob()
                data.readinto(f)

# kill the process
os.system("killall feh")
# Start feh
os.system(f"feh -xFY -D 30 --sort mtime {current_path}/images &")

def process_queue_messages():
    messages = queue_client.receive_messages()
    
    for message in messages:
        print(f"Processing message: {message.content}")

        try:

            print('Downloading image from blob storage')

            blob_client = container_client.get_blob_client(message.content)
            file_name = blob.name.split("/")[-1]
            with open(f'{current_path}/images/{file_name}', "wb") as f:
                data = blob_client.download_blob()
                data.readinto(f)
        except:
            pass

        # After processing, delete the message from the queue
        queue_client.delete_message(message)

        # kill the process
        os.system("killall feh")
        # Start feh
        os.system(f"feh -xFY -D 30 --sort mtime {current_path}/images &")


while True:
    process_queue_messages()
    time.sleep(5)  # Sleep for 5 seconds before checking for new messages
