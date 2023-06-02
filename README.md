# hl-scraper

(Recommended) Install and activate a virtual enviroment first:

https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/


Install packages:

    pip install -r requirements.txt

To run the script, execute the main.py file on source:

    python source/main.py

Follow the instructions on the terminal.


========================================================


The proxy URL should be inside the config.env file.
Configure Proxies (as a dictionary) in the config.env file
E.g:
    PROXY_URL=url


Notes:
The proxy implementation it's supossed to work with SOCKS5,
but it's returning a Time out exception, idk if it's fault of 
the library or the proxy.

