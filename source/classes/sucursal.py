import os
from dotenv import load_dotenv
import aiohttp
import asyncio
import csv

class Sucursal:

    # Constructor
    def __init__(self, sc=1, subcat_paths="", csv_filename="", csv_path=""):
        self.sc = str(sc)
        self.subcat_urls = self.__get_sub_info(subcat_paths)
        if csv_filename == "":
            csv_filename = f"sucursal-{sc}"
        self.csv_filename = csv_filename
        if csv_path == "":
            csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"../../csv/")
        self.csv_path = csv_path
        self.__write_first_row()

    # This method queries the api to get the quantity of items in each sub-category.

    def __get_sub_info(self, paths, update=False):

        res = []
        for path in paths:
            res.append(
                f'https://www.hiperlibertad.com.ar/api/catalog_system/pub/facets/search/{path}?map=c,c&sc={self.sc}')
        return res

        # Let's give it a shot to async calls.
        # load_dotenv('config.env')
        # res = []
        # if os.getenv('PROXY'):
        #     proxy = aiohttp.ProxyConnector(proxy_url=os.getenv('PROXY'))
        #     async with aiohttp.ClientSession(connector=proxy) as session:
        #         # Make your HTTP requests using the session
        #         for path in paths:
        #             response = await session.get(f'https://www.hiperlibertad.com.ar/api/catalog_system/pub/facets/search/{path}?map=c,c&sc={self.sc}')
        #             res.append({'subcat': path, 'quantity': response.json()['Departments'][0]['Quantity']})
        #             print(response.json)
        # return res

    # Write the first row for each column name

    def __write_first_row(self):
        fields = ['nombre', 'precio_lista', 'precio', 'categoria',
                  'product_id', 'item_id', 'url', 'stock', 'descripcion', 'marca']
        with open(f'{self.csv_path}{self.csv_filename}.csv', 'w+', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            file.close()

    # Updates the amount of items in a SC using the data recorded for each category/sub-category

    def update_sc_items_amount(self):
        try:
            # I guess it's redundant to check for sub-categories data. Whatever
            assert len(self.subcats) > 0
            # Using list comprehension to shorten code.
            self.sc_items_amount = sum(
                [subcats_entry['quantity'] for subcats_entry in self.subcats])
        except AssertionError:
            print(
                "Whooops! Seems like something went wrong retrieving the sub-categories data.")

    # Return the amount of queries needed to get info of each item. Could be useful?

    def calculate_search_queries(self, max_per_search_query=50):
        # Using list comprehension to shorten code.
        return sum([int(subcats_entry['quantity'] / max_per_search_query) + 1 for subcats_entry in self.subcats])

    # Let's compose the URL for the search query

    def make_search_query_url(self, path, a, b):
        return f'https://www.hiperlibertad.com.ar/api/catalog_system/pub/products/search/{path}?O=OrderByTopSaleDESC&_from={a}&_to={b}&ft&sc={self.sc}'

    # TODO: comment this function

    async def fetch_quantity(self, session, url):
        async with session.get(url) as response:
            cat = '/'.join(url.split('?')[0].split('/')[-2:])
            quantity = (await response.json())['Departments'][0]['Quantity']
            return {'cat': cat, 'quantity': quantity}

    # TODO: comment this function

    async def get_subcat_quantity(self):
        # Setting the proxy
        proxy_connector = None
        load_dotenv('config.env')
        if os.getenv('PROXY_URL'):
            proxy_connector = aiohttp.ProxyConnector(
                proxy_url=os.getenv('PROXY_URL'))

        async with aiohttp.ClientSession(connector=proxy_connector) as session:
            # Make your HTTP requests using the session
            tasks = []
            for url in self.subcat_urls:
                task = asyncio.create_task(self.fetch_quantity(session, url))
                tasks.append(task)
            results = await asyncio.gather(*tasks)
        self.subcats = results

    # TODO: comment this function

    async def fetch_items(self, session, url, csv_writer):

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
                    'descripcion': item['description'],
                    # Could be useful
                    'marca': item['brand']
                }
                # Write the result to the CSV file
                csv_writer.writerow(item)

    # TODO: comment this function

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
            load_dotenv('config.env')
            if os.getenv('PROXY_URL'):
                proxy_connector = aiohttp.ProxyConnector(
                    proxy_url=os.getenv('PROXY_URL'))

            # Creating session through aiohttp.
            async with aiohttp.ClientSession(connector=proxy_connector) as session:
                tasks = []
                for url in urls:
                    task = asyncio.create_task(
                        self.fetch_items(session, url, csv_writer))
                    tasks.append(task)

                # Wait for all tasks to complete
                await asyncio.gather(*tasks)
