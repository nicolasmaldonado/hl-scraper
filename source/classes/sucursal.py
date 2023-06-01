import os
from dotenv import load_dotenv
import aiohttp
import asyncio
from aiohttp_socks import ProxyConnector
import csv


class Sucursal:

    # Constructor
    def __init__(self, sc=1, subcat_paths=[], csv_filename="", csv_path=""):
        self.sc = str(sc)
        self.subcats = []
        self.subcat_urls = self.__get_subcat_urls(subcat_paths)
        if csv_filename == "":
            csv_filename = f"sucursal-{sc}"
        self.csv_filename = csv_filename
        # I'm just realizing that I'm assuming it should end in a '/'
        # Add a warning or manually check and add it.
        if csv_path == "":
            csv_path = os.path.join(os.path.dirname(
                os.path.abspath(__file__)), "../../csv/")
        else:
            if csv_path[-1] != '/':
                csv_path += '/'
        self.csv_path = csv_path
        self.__write_first_row()

    # This method queries the api to get the quantity of items in each sub-category.

    def __get_subcat_urls(self, paths):
        res = []
        for path in paths:
            res.append(
                f'https://www.hiperlibertad.com.ar/api/catalog_system/pub/facets/search/{path}?map=c,c&sc={self.sc}')
        return res

    # Write the first row for each column name

    def __write_first_row(self):
        fields = ['nombre', 'precio_lista', 'precio', 'categoria',
                  'product_id', 'item_id', 'url', 'stock', 'descripcion', 'marca']
        with open(f'{self.csv_path}{self.csv_filename}.csv', 'w+', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            file.close()

    # This function is used in get_subcat_quantity.
    # makes the req and parses the result.

    async def __fetch_quantity(self, session, url):
        async with session.get(url) as response:
            cat = '/'.join(url.split('?')[0].split('/')[-2:])
            quantity = (await response.json())['Departments'][0]['Quantity']
            return {'cat': cat, 'quantity': quantity}

    # This function retrieves the quantity of items of each category/sub-category
    # This helps a lot when making the queries (it only returns 50 items at once)

    async def get_subcat_quantity(self):
        # Setting the proxy
        load_dotenv('config.env')

        proxy_connector = None
        if os.getenv('PROXY_URL'):
            url = f'socks5://{os.getenv("PROXY_URL")}'
            print(url)
            proxy_connector = ProxyConnector.from_url(url=url)

        async with aiohttp.ClientSession(proxy_connector) as session:
            # Make your HTTP requests using the session
            tasks = []
            for url in self.subcat_urls:
                task = asyncio.create_task(self.__fetch_quantity(session, url))
                tasks.append(task)
            results = await asyncio.gather(*tasks)
        self.subcats = results

        # Let's compose the URL for the search query

    # Parses the path into the query.

    def make_search_query_url(self, path, a, b):
        return f'https://www.hiperlibertad.com.ar/api/catalog_system/pub/products/search/{path}?O=OrderByTopSaleDESC&_from={a}&_to={b}&ft&sc={self.sc}'

    # This function is called in get_catalog.
    # makes the req, parses the result and stores it in the CSV file

    async def __fetch_items(self, session, url, csv_writer):

        fields = ['nombre', 'precio_lista', 'precio', 'categoria',
                  'product_id', 'item_id', 'url', 'stock', 'descripcion', 'marca']
        async with session.get(url) as response:
            # Return array with Items as dictionaries
            result = (await response.json())
            # Iterate through every item
            for item in result:
                item = {
                    'nombre': item['productName'],
                    'precio_lista': item['items'][0]['sellers'][0]['commertialOffer']['ListPrice'],
                    'precio': item['items'][0]['sellers'][0]['commertialOffer']['Price'],
                    'categoria': item['categories'],
                    'product_id': item['productId'],
                    'item_id': item['items'][0]['itemId'],
                    'url': (item['link'] + "?sc=" + self.sc),
                    'stock': item['items'][0]['sellers'][0]['commertialOffer']['AvailableQuantity'],
                    'descripcion': (item['description']).encode("utf-8"),
                    # Could be useful
                    'marca': item['brand']
                }
                # Write the result to the CSV file
                csv_writer.writerow(item)

    # This is basically the principal function.
    # Sets up everything and calls __fetch_items to parse and save the data.

    async def get_catalog(self, items_per_query=50):

        fields = ['nombre', 'precio_lista', 'precio', 'categoria',
                  'product_id', 'item_id', 'url', 'stock', 'descripcion', 'marca']
        # Opening the CSV file
        with open(f'{self.csv_path}{self.csv_filename}.csv', 'a', newline='') as file:
            csv_writer = csv.DictWriter(file, fieldnames=fields)

            # Building the urls for the search queries
            urls = []
            for elem in self.subcats:
                for i in range(0, elem['quantity'], items_per_query):
                    urls.append(self.make_search_query_url(
                        elem['cat'], i, i+items_per_query-1))

            # Setting the proxy
            proxy_connector = None
            if os.getenv('PROXY_URL'):
                proxy_connector = ProxyConnector.from_url(
                    f'socks5://{os.getenv("PROXY_URL")}')

            # Creating session through aiohttp.
            async with aiohttp.ClientSession(trust_env=True) as session:
                tasks = []
                for url in urls:
                    task = asyncio.create_task(
                        self.__fetch_items(session, url, csv_writer))
                    tasks.append(task)

                # Wait for all tasks to complete
                await asyncio.gather(*tasks)

    # TODO: Fix the timeout error when connecting to the proxy
    # Couldn't make it work yet.

    async def test_proxy(self, url):
        # load_dotenv('config.env')
        connector = ProxyConnector.from_url('socks5://144.217.197.151:38611')
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url) as response:
                res = (await response.text())
                print(res)
                return res
            # tasks = []
            # task = asyncio.create_task(self.__get_ip(session, url))
            # tasks.append(task)
            # results = await asyncio.gather(*tasks)
