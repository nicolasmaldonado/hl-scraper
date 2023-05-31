from argparse import ArgumentError
import sys
import os

from .. import utils


class Categorias:

    # Description: Pass the URL directly to the API and only to get the JSON containing the info
    #           regarding the categories of Items.
    def __init__(self, url="https://www.hiperlibertad.com.ar/api/catalog_system/pub/category/tree/50"):
        # TODO: Try to find out how to implement singleton pattern
        try:
            # categorias stores an array containig dicts of each Major categories.
            self.categorias = utils.url_get(url).json()
            self.subs_for_queries = self.__list_subcats()
        except:
            raise Exception("URL or JSON format returned are not valid.")

    def __list_subcats(self):
        res = []
        for cat in self.categorias:
            for sub in cat['children']:
                res.append((cat['name'] + "/" + sub['name']
                            ).replace(" ", "-").lower())
        return res
