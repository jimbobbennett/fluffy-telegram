import hashlib
import logging
import os

from pangea.config import PangeaConfig
from pangea.services import UrlIntel, FileIntel

# Load the Pangea config and create the URL and File Intel services
__domain = os.getenv("PANGEA_DOMAIN")
__token = os.getenv("PANGEA_TOKEN")

__config = PangeaConfig(domain=__domain)

__url_intel = UrlIntel(token=__token, config=__config)
__file_intel = FileIntel(token=__token, config=__config)

def is_url_malicious(image_url: str) -> bool: 
    '''
    Checks if the URL is malicious. If it is, returns True. If it is not, returns False.

    :param image_url: The URL to check
    :type image_url: str
    :return: True if the URL is malicious, False if it is not
    :rtype: bool
    '''
    reputation = __url_intel.reputation(image_url)
    logging.info(f'URL reputation: {reputation}')

    return reputation.result.data.score > 50

def is_file_malicious(file: bytes) -> bool: 
    '''
    Checks if the file is malicious. If it is, returns True. If it is not, returns False.

    :param file: The file to check
    :type file: bytes
    :return: True if the URL is malicious, False if it is not
    :rtype: bool
    '''
    hash = hashlib.sha256(file).hexdigest()
    reputation = __file_intel.hashReputation(hash=hash, hash_type="sha256")
    logging.info(f'File reputation: {reputation}')

    return reputation.result.data.score > 50