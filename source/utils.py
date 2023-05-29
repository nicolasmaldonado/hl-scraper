import requests
import os
from dotenv import load_dotenv
import json

# Hiding the env loading and the proxy call
# Makes it a bit easier to read code in the other files.
def url_get(url):

    load_dotenv('config.env')

    proxies_settings = {}

    if os.getenv('PROXY'):
        proxies_settings = json.loads(os.getenv('PROXY_URL'))

    return requests.get(url, proxies=proxies_settings)

        
