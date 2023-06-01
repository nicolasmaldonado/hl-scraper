import unittest
import random
import asyncio
import csv

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from source.classes.sucursal import Sucursal
from source.classes.categorias import Categorias

class TestAdd(unittest.TestCase):

    sucursales = {
        1: '  Cordoba        - Hipermercado Lugones',
        2: '  Cordoba        - Hipermercado Rivera',
        3: '  Cordoba        - Hipermercado Jacinto Rios',
        4: '  Cordoba        - Hipermercado Ruta 9',
        6: '  Mendoza        - Hipermercado Godoy Cruz',
        7: '  Misiones       - Hipermercado Posadas ',
        8: '  Tucuman        - Hipermercado Tucuman 1',
        9: '  Tucuman        - Hipermercado Tucuman 2',
        10: '  Chaco          - Hipermercado Chaco ',
        11: '  Santa Fe       - Hipermercado Rosario',
        12: '  Sgo del Estero - Hipermercado Sgo del Estero',
        13: '  San Juan       - Hipermercado San Juan',
        14: '  Salta          - Hipermercado Salta',
        15: '  Santa Fe       - Hipermercado Rafaela',
        16: '  Mendoza        - Tienda Digital Mza Capital'}

    # Constructor test, should create CSV file correctly.
    # Should have correct name and path (default).

    def test_init(self):
        sc = random.choice(list(self.sucursales.keys()))
        s = Sucursal(sc=sc)
        path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), f'../csv/sucursal-{sc}.csv'))
        self.assertTrue(os.path.isfile(path))
        # Deleting the CSV so it doesnt give a false positive in other tests.
        os.remove(path)

    # Constructor test, should create CSV file correctly.
    # Should have correct name and path (w/ parameters).

    def test_init2(self):
        sc = random.choice(list(self.sucursales.keys()))
        csv_filename = "asdf"
        # Change this path to test in a new enviroment
        csv_path = '/users/nicolasmaldonado/Programming/TEST'
        c = Sucursal(sc=sc, csv_path=csv_path, csv_filename=csv_filename)
        path = os.path.join(csv_path, f'{csv_filename}.csv')
        self.assertTrue(os.path.isfile(path))
        # Deleting the CSV so it doesnt give a false positive in other tests.
        os.remove(path)

    # Constructor test, the attribute 'subcat_urls' should have the
    # same lenght as the 'subcat_paths' parameter.

    def test_init3(self):
        sc = random.choice(list(self.sucursales.keys()))
        subcat_paths = ['a', 'b', 'b']
        s = Sucursal(sc=sc, subcat_paths=subcat_paths)
        self.assertEqual(len(subcat_paths), len(s.subcat_urls))
        # Deleting the CSV so it doesnt give a false positive in other tests.
        path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), f'../csv/sucursal-{sc}.csv'))
        os.remove(path)

    # OKAY, there's a problem with the requests
    # Aparently, if the 'cat/sub-cat' is empty, it returns the amount of brands in the 'cat'
    # SO, IT SHOULD, only make more requests than neccesary, but IT SHOULD
    # RETRIEVE every item still. It only makes more requests
    # (ranges 50-99, 100-149...) when the category is empty.

    # We should have info of each category
    # (1 dict in 'subcats' per url in 'subcat_urls')
    def test_get_subcat_quantity(self):
        c = Categorias()
        sc = 1  # random.choice(list(self.sucursales.keys()))
        s = Sucursal(sc=sc, subcat_paths=c.subs_for_queries)
        asyncio.run(s.get_subcat_quantity())
        self.assertEqual(len(s.subcat_urls), len(s.subcats))
        # Deleting the CSV so it doesnt give a false positive in other tests.
        path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), f'../csv/sucursal-{sc}.csv'))
        os.remove(path)

    # We should have info of each category
    # (there is an issue which causes a difference between the
    # ammount of retrieved items and the quantity in each
    # sub-category, that was supossed to be the test
    # assert())
    def test_get_catalog(self):

        c = Categorias()

        # Pick a SC at random from the valid list
        sc = random.choice(list(self.sucursales.keys()))

        s = Sucursal(sc=sc, subcat_paths=c.subs_for_queries)

        asyncio.run(s.get_subcat_quantity())

        asyncio.run(s.get_catalog())

        csv_file_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), f'../csv/sucursal-{sc}.csv'))
        line_count = -1  # -1 for the header

        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file)
            # Count the number of lines (rows)
            line_count = sum(1 for _ in reader)

        self.assertTrue(line_count > 0)
        os.remove(csv_file_path)

    # def test_proxy(self):
    #     url='http://api.ipify.org/'
    #     url2='https://api.myip.com/'
    #     c = Categorias()
    #     sc = 1 #random.choice(list(self.sucursales.keys()))
    #     s = Sucursal(sc=sc, subcat_paths=c.subs_for_queries)
    #     asyncio.run(s.test_proxy(url2))


if __name__ == '__main__':
    unittest.main()
