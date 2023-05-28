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

Configure CSV folder path in the config.env file
Configure Proxies (as a dictionary) in the config.env file
E.g:
    PROXY={'http': '', 'https': ''}

