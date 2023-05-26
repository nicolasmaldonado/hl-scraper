import requests
import csv
import time


class Sucursal:

    # Constructor
    def __init__(self, sc=1, sub_cat_paths=""):
        # int: id of branch(sucursal)
        self.sc = str(sc)
        # int: amount of items in that branch
        self.sc_items_amount = 0
        # Stores each sub-category and how many items are in that sub-cat.
        # (I think that could be useful when making search queries)
        # Stores in this format:
        # [{'path': categoria/sub-categoria, 'quantity': x}]
        self.sub_cats = self.__get_sub_info(sub_cat_paths)
        # Hopefully here is where all item data will go
        # TODO: I'm having second doubts about storing everything in
        # memory, maybe each query should be automatically stored in a CSV.
        self.catalog = []

    # This method queries the api to get the quantity of items in each sub-category

    def __get_sub_info(self, paths):
        res = []
        for path in paths:
            res.append({'subcat': path, 'quantity': requests.get(
                f'https://www.hiperlibertad.com.ar/api/catalog_system/pub/facets/search/{path}?map=c,c&sc={self.sc}').json()['Departments'][0]['Quantity']})
        return res

    # Updates the amount of items in a SC using the data recorded for each category/sub-category

    def update_sc_items_amount(self):
        try:
            # I guess it's redundant to check for sub-categories data. Whatever
            assert len(self.sub_cats) > 0
            # Using list comprehension to shorten code.
            self.sc_items_amount = sum(
                [sub_cat_entry['quantity'] for sub_cat_entry in self.sub_cats])
        except AssertionError:
            print(
                "Whooops! Seems like something went wrong retrieving the sub-categories data.")

    # Return the amount of queries needed to get info of each item. Could be useful?

    def calculate_search_queries(self, max_per_search_query=50):
        # Using list comprehension to shorten code.
        return sum([int(sub_cat_entry['quantity'] / max_per_search_query) + 1 for sub_cat_entry in self.sub_cats])

    # Let's compose the URL for the search query

    def make_search_query_url(self, path, a, b):
        return f'https://www.hiperlibertad.com.ar/api/catalog_system/pub/products/search/{path}?O=OrderByTopSaleDESC&_from={a}&_to={b}&ft&sc={self.sc}'

    # TODO: TEST THIS TOMORROW
    # This should be where the magic happens.

    def get_catalog(self, items_per_query=50, queries_per_round=10, time_delay_per_round=5):

        for elem in self.sub_cats:

            for i in range(0, elem['quantity'], items_per_query):

                url = self.make_search_query_url(
                    elem['subcat'], i, i+items_per_query-1)

                items_search_result = requests.get(url).json()

                time.sleep(time_delay_per_round)

                for j in items_search_result:
                    item = {
                        'nombre': j['productName'],
                        'precio_lista': j['items'][0]['sellers'][0]['commertialOffer']['ListPrice'],
                        'precio': j['items'][0]['sellers'][0]['commertialOffer']['Price'],
                        'categoria': j['categories'],
                        'product_id': j['productId'],
                        'item_id': j['items'][0]['itemId'],
                        'url': (j['link'] + "?sc=" + self.sc),
                        'stock': j['items'][0]['sellers'][0]['commertialOffer']['AvailableQuantity'],
                        'descripcion': j['description'],
                        # Agrego este campo, quizas sea util.
                        'marca': j['brand']
                    }
                    print(item)
