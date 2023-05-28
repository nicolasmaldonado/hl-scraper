import csv
import time
from os.path import exists
import json
from .. import utils


class Sucursal:

    # Constructor
    def __init__(self, sc=1, sub_cat_paths="", csv_filename="", csv_path=""):
        # id of branch(sucursal)
        self.sc = str(sc)
        # int: amount of items in that branch
        self.sc_items_amount = 0
        # Stores each sub-category and how many items are in that sub-cat.
        # (I think that could be useful when making search queries)
        # Stores in this format:
        # [{'path': categoria/sub-categoria, 'quantity': x}]
        #self.sub_cats = self.__get_sub_info(sub_cat_paths)
        # This'll be the default name. 
        # I didn't assign it in the function declaration because 
        # I'd like to use the SC number.
        if csv_filename == "":
            csv_filename = f"sucursal-{sc}"
        self.csv_filename = csv_filename
        self.csv_path = csv_path
        # Create file and write the headers
        self.__write_first_row()

    # This method queries the api to get the quantity of items in each sub-category. 

    def __get_sub_info(self, paths, update=False):

        res = []
        # Query every category
        for path in paths:
            res.append({'subcat': path, 'quantity': utils.url_get(
                f'https://www.hiperlibertad.com.ar/api/catalog_system/pub/facets/search/{path}?map=c,c&sc={self.sc}').json()['Departments'][0]['Quantity']})
       
        return res

    # Write the first row for each column name

    def __write_first_row(self):
        fields = ['nombre', 'precio_lista', 'precio', 'categoria', 'product_id', 'item_id', 'url', 'stock', 'descripcion', 'marca']
        with open(f'{self.csv_path}{self.csv_filename}.csv', 'w+', newline='') as file:
            writer = csv.DictWriter(file, fieldnames = fields)
            writer.writeheader() 
            file.close()

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

    # This should be where the magic happens.
    # TODO: Try to not duplicate elements in the CSV. 
    # But, add an option to force the update. 
    # Maybe it could have an option to save the CSV with the DATE or version (1,2,3,etc...)
    # It should be useful to take snapshots and compare how the data changes.

    def get_catalog(self, items_per_query=50, queries_per_round=10, time_delay_per_round=5):

        fields = ['nombre', 'precio_lista', 'precio', 'categoria', 'product_id', 'item_id', 'url', 'stock', 'descripcion', 'marca']
        
        # Opening the CSV file
        with open(f'{self.csv_path}{self.csv_filename}.csv', 'a', newline='') as file:

            writer = csv.DictWriter(file, fieldnames = fields)

            # Iterating through every cat/subcat path
            for elem in self.sub_cats:

                # Querying 
                for i in range(0, elem['quantity'], items_per_query):

                    url = self.make_search_query_url(
                        elem['subcat'], i, i+items_per_query-1)

                    items_search_result = utils.url_get(url).json()

                    # I introduced a delay trying not to spam the server
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
                        
                        writer.writerow(item)
            
            file.close()

