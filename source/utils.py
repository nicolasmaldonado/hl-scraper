import requests
import os
from dotenv import load_dotenv
import json

# Hiding the env loading and the proxy call
# Makes it a bit easier to read code in the other files.
def url_get(url):

    load_dotenv('config.env')

    return requests.get(url, proxies=json.loads(os.getenv('PROXY')))
        
