import dotenv
import os
import pathlib
import time

from azure.storage.blob import BlobServiceClient
from azure.storage.queue import QueueServiceClient

# Get the current path as this is where we will load images from
current_path = pathlib.Path(__file__).parent.resolve()

# Get the connection string and device ID for this device
dotenv.load_dotenv()
connection_string = os.getenv("STORAGE_CONNECTION_STRING")
device_id = os.getenv("DEVICE_ID")

# Create a connection to the queue to receive notifications of updated images
queue_service_client = QueueServiceClient.from_connection_string(connection_string)
queue_name = f"images-{device_id}"
queue_client = queue_service_client.get_queue_client(queue_name)

# Create a connection to the blob storage to download images
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_name = "images"
container_client = blob_service_client.get_container_client(container_name)

# Download all blobs from the container
blobs = container_client.list_blobs()
for blob in blobs:
    # Only download blobs that are for this device
    if blob.name.startswith(f"{device_id}/"):

        print(f"Downloading {blob.name}")

        # Download the blob
        blob_client = container_client.get_blob_client(blob.name)
        file_name = blob.name.split("/")[-1]

        # Check if the file exists - if not don't overwrite it
        if not os.path.exists(f'{current_path}/images/{file_name}'):
            # Write the blob to the file
            with open(f'{current_path}/images/{file_name}', "wb") as f:
                data = blob_client.download_blob()
                data.readinto(f)

def restart_feh() -> None:
    '''
    feh is used to show the slide show. Kill and restart it so the images get displayed.
    https://feh.finalrewind.org
    '''
    # kill the feh process if it is running
    os.system("killall feh")
    # Start feh.
    # -x: hide the mouse cursor
    # -F: fullscreen
    # -Y: hide the toolbar
    # -D 30: change the image every 30 seconds
    # --sort mtime: sort the images by the time they were last modified so we show the latest first
    os.system(f"feh -xFY -D 30 --sort mtime {current_path}/images &")

def process_queue_messages():
    '''
    Look for new messages in the queue and process them. Each message contains the name of a new image, so download it and add it to the slideshow
    '''
    # Block waiting for messages
    messages = queue_client.receive_messages()

    # Track if we process any messages
    processed_messages = False
    
    # Loop through each message
    for message in messages:
        print(f"Processing message: {message.content}")
        try:
            print('Downloading image from blob storage')

            # Download the blob
            blob_client = container_client.get_blob_client(message.content)
            file_name = blob.name.split("/")[-1]

            # Write the blob to the file in the images folder
            with open(f'{current_path}/images/{file_name}', "wb") as f:
                data = blob_client.download_blob()
                data.readinto(f)
            
            # We processed a message
            processed_messages = True
        except:
            pass

        # After processing, delete the message from the queue
        queue_client.delete_message(message)

    # restart the slideshow if we processed any messages
    if processed_messages:
        restart_feh()

# Start the slideshow
restart_feh()

while True:
    try:
        # Check for new messages
        process_queue_messages()
    except:
        # If there is an error, just ignore it and try again later
        pass

    # Sleep for 5 seconds before checking for new messages
    time.sleep(5)
