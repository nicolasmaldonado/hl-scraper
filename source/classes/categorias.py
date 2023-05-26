from argparse import ArgumentError
import requests


class Categorias:

    # Description: Pass the URL directly to the API and only to get the JSON containing the info
    #           regarding the categories of Items.
    def __init__(self, url="https://www.hiperlibertad.com.ar/api/catalog_system/pub/category/tree/50"):
        # TODO: Find out how to name attributes according to PEP8
        # TODO: Try to find out how to implement singleton pattern
        # TODO: Check if you can make this attribute 'final'
        try:
            # categorias stores an array containig dicts of each Major categories.
            self.categorias = requests.get(url).json()
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

    # # Just trying to keep the constructor as clean as I can x_x
    # def __parse_categories_response(self, data_structure):
    #     if type(data_structure) == dict:
    #         res = {}
    #         keys = data_structure.keys()
    #         if data_structure['hasChildren'] == True:
    #             res['sub'] = self.__parse_categories_response(data_structure['children'])
    #         if 'name' in keys and 'id' in keys:
    #             res = {
    #                     'id': data_structure['id'],
    #                     'name' : data_structure['name'],
    #                 }
    #             if
    #         if 'children'
    #                 return self.__parse_categories_response(data_structure[key])

    # # Returns dictionary with only the 'name' key (if it exist, else {})
    # def __filter_attribute(self, dic, key='name'):
    #     new_dic = {}
    #     for k in dic.keys():
    #         if k == key:
    #             new_dic[key] = dic[key]
    #     return new_dic
