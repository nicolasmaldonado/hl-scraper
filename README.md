# hl-scraper

(Not final version)

Create a virtual environment, decide upon a directory where you want to place it, and run the venv module as a script with the directory path:

    python -m venv tutorial-env

On Windows, run:

    tutorial-env\Scripts\activate.bat

On Unix or MacOS, run:

    source tutorial-env/bin/activate

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

