import requests
import os
from dotenv import load_dotenv

# Hiding the env loading and the proxy call
# Makes it a bit easier to read code in the other files.
# 
# edit: I think it got deprecated lol, I'm using the 
# proxy through asyncio now, not requests
def url_get(url):

    load_dotenv('config.env')

    proxies_settings = {}

    # if os.getenv('PROXY_URL'):

    #     proxies_settings = {
    #         'http': f"socks5://{os.getenv('PROXY_URL')}",
    #         'https': f"socks5://{os.getenv('PROXY_URL')}"
    #     }

    return requests.get(url, proxies=proxies_settings)

        
