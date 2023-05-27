import requests
import csv
import time
from os.path import exists


class Sucursal:

    # Constructor
    def __init__(self, sc=1, sub_cat_paths="", csv_filename="", csv_path="../../csv/"):
        # int: id of branch(sucursal)
        self.sc = str(sc)
        # int: amount of items in that branch
        self.sc_items_amount = 0
        # Stores each sub-category and how many items are in that sub-cat.
        # (I think that could be useful when making search queries)
        # Stores in this format:
        # [{'path': categoria/sub-categoria, 'quantity': x}]
        self.sub_cats = self.__get_sub_info(sub_cat_paths)
        # This'll be the default name. 
        # I didn't assign it in the function declaration because 
        # I'd like to use the SC number.
        if csv_filename == "":
            csv_filename = f"sucursal-{sc}"
        self.csv_filename = csv_filename
        self.csv_path = csv_path
        # Create file and write the headers
        self.__write_first_row()

    # This method queries the api to get the quantity of items in each sub-category

    def __get_sub_info(self, paths):
        #TODO: DELETE THIS, JUST FOR TESTING 
        res = [{'subcat': 'tecnología/tv-y-video', 'quantity': 29}, {'subcat': 'tecnología/audio', 'quantity': 57}, {'subcat': 'tecnología/informática', 'quantity': 13}, {'subcat': 'tecnología/celulares-y-tablets', 'quantity': 40}, {'subcat': 'tecnología/videojuegos', 'quantity': 140}, {'subcat': 'tecnología/smartwatch', 'quantity': 140}, {'subcat': 'bebidas/aperitivos', 'quantity': 64}, {'subcat': 'bebidas/cervezas', 'quantity': 74}, {'subcat': 'bebidas/gaseosas', 'quantity': 95}, {'subcat': 'bebidas/jugos', 'quantity': 75}, {'subcat': 'bebidas/aguas', 'quantity': 88}, {'subcat': 'bebidas/vinos-y-espumantes', 'quantity': 374}, {'subcat': 'bebidas/isotónicas-y-energizantes', 'quantity': 25}, {'subcat': 'bebidas/bebidas-blancas-y-licores', 'quantity': 93}, {'subcat': 'deportes/fitness', 'quantity': 18}, {'subcat': 'deportes/bicicletas', 'quantity': 21}, {'subcat': 'deportes/accesorios-deportivos', 'quantity': 27}, {'subcat': 'deportes/patinaje', 'quantity': 5}, {'subcat': 'vehículos/accesorios-para-automóviles', 'quantity': 113}, {'subcat': 'vehículos/accesorios-para-motos', 'quantity': 3}, {'subcat': 'vehículos/neumáticos', 'quantity': 12}, {'subcat': 'librería/librería-y-papelería', 'quantity': 295}, {'subcat': 'aire-libre-y-jardín/camping', 'quantity': 19}, {'subcat': 'aire-libre-y-jardín/piletas', 'quantity': 130}, {'subcat': 'aire-libre-y-jardín/cuidado-del-jardín', 'quantity': 126}, {'subcat': 'aire-libre-y-jardín/muebles-de-exterior', 'quantity': 52}, {'subcat': 'aire-libre-y-jardín/asador', 'quantity': 11}, {'subcat': 'aire-libre-y-jardín/iluminación-exterior', 'quantity': 6}, {'subcat': 'hogar/muebles-de-interior', 'quantity': 69}, {'subcat': 'hogar/cocina-y-comedor', 'quantity': 536}, {'subcat': 'hogar/baño', 'quantity': 67}, {'subcat': 'hogar/organización', 'quantity': 106}, {'subcat': 'hogar/iluminación', 'quantity': 26}, {'subcat': 'hogar/dormitorio', 'quantity': 146}, {'subcat': 'hogar/herramientas-y-mantenimiento', 'quantity': 190}, {'subcat': 'hogar/deco', 'quantity': 179}, {'subcat': 'bebés-y-niños/higiene-y-salud', 'quantity': 49}, {'subcat': 'bebés-y-niños/lactancia-y-alimentación', 'quantity': 69}, {'subcat': 'bebés-y-niños/seguridad-del-bebé', 'quantity': 364}, {'subcat': 'bebés-y-niños/paseo-del-bebé', 'quantity': 2}, {'subcat': 'bebés-y-niños/vehículos-infantiles', 'quantity': 4}, {'subcat': 'bebés-y-niños/muebles-infantiles', 'quantity': 5}, {'subcat': 'bebés-y-niños/juguetería', 'quantity': 152}, {'subcat': 'bebés-y-niños/accesorios', 'quantity': 364}, {'subcat': 'bebés-y-niños/pañales-y-toallitas-húmedas', 'quantity': 82}, {'subcat': 'electrodomésticos/climatización', 'quantity': 69}, {'subcat': 'electrodomésticos/pequeños-electrodomésticos', 'quantity': 60}, {'subcat': 'electrodomésticos/lavado', 'quantity': 26}, {'subcat': 'electrodomésticos/cocinas-y-hornos', 'quantity': 25}, {'subcat': 'electrodomésticos/heladeras-y-freezers', 'quantity': 23}, {'subcat': 'electrodomésticos/hogar-y-limpieza', 'quantity': 4}, {'subcat': 'electrodomésticos/cuidado-personal-y-salud', 'quantity': 23}, {'subcat': 'electrodomésticos/termotanques-y-calefones', 'quantity': 7}, {'subcat': 'mascotas/alimentos', 'quantity': 101}, {'subcat': 'mascotas/accesorios-para-mascotas', 'quantity': 22}, {'subcat': 'almacén/aceites-y-vinagres', 'quantity': 62}, {'subcat': 'almacén/aceitunas-y-encurtidos', 'quantity': 48}, {'subcat': 'almacén/aderezos', 'quantity': 78}, {'subcat': 'almacén/arroz-y-legumbres', 'quantity': 22}, {'subcat': 'almacén/caldos,-sopas-y-puré', 'quantity': 45}, {'subcat': 'almacén/conservas', 'quantity': 82}, {'subcat': 'almacén/desayuno-y-merienda', 'quantity': 469}, {'subcat': 'almacén/golosinas-y-chocolates', 'quantity': 225}, {'subcat': 'almacén/harinas', 'quantity': 16}, {'subcat': 'almacén/sin-tacc', 'quantity': 17}, {'subcat': 'almacén/panificados', 'quantity': 94}, {'subcat': 'almacén/para-preparar', 'quantity': 53}, {'subcat': 'almacén/pastas-secas-y-salsas', 'quantity': 50}, {'subcat': 'almacén/sal,-pimienta-y-especias', 'quantity': 100}, {'subcat': 'almacén/snacks', 'quantity': 69}, {'subcat': 'lácteos/dulce-de-leche', 'quantity': 14}, {'subcat': 'lácteos/leches', 'quantity': 42}, {'subcat': 'lácteos/cremas', 'quantity': 10}, {'subcat': 'lácteos/yogures', 'quantity': 67}, {'subcat': 'lácteos/mantecas-y-margarinas', 'quantity': 2}, {'subcat': 'lácteos/postres-y-flanes', 'quantity': 20}, {'subcat': 'perfumería/cuidado-capilar', 'quantity': 515}, {'subcat': 'perfumería/cuidado-oral', 'quantity': 130}, {'subcat': 'perfumería/cuidado-personal', 'quantity': 322}, {'subcat': 'perfumería/cuidado-de-la-piel', 'quantity': 209}, {'subcat': 'perfumería/protección-femenina', 'quantity': 78}, {'subcat': 'perfumería/protección-para-adultos', 'quantity': 25}, {'subcat': 'perfumería/farmacia', 'quantity': 73}, {'subcat': 'limpieza/accesorios-de-limpieza', 'quantity': 157}, {'subcat': 'limpieza/calzado', 'quantity': 14}, {'subcat': 'limpieza/cuidado-de-la-ropa', 'quantity': 77}, {'subcat': 'limpieza/desodorantes-de-ambiente', 'quantity': 56}, {'subcat': 'limpieza/insecticidas', 'quantity': 3}, {'subcat': 'limpieza/lavandina', 'quantity': 7}, {'subcat': 'limpieza/limpieza-de-baño', 'quantity': 31}, {'subcat': 'limpieza/limpieza-de-cocina', 'quantity': 84}, {'subcat': 'limpieza/limpieza-de-pisos-y-muebles', 'quantity': 98}, {'subcat': 'limpieza/papeles', 'quantity': 29}, {'subcat': 'frutas-y-verduras/frutas', 'quantity': 46}, {'subcat': 'frutas-y-verduras/verduras', 'quantity': 25}, {'subcat': 'frutas-y-verduras/huevos', 'quantity': 6}, {'subcat': 'frutas-y-verduras/legumbres-y-semillas', 'quantity': 17}, {'subcat': 'frutas-y-verduras/hierbas-aromáticas', 'quantity': 3}, {'subcat': 'frutas-y-verduras/leña-y-carbón', 'quantity': 4}, {'subcat': 'quesos-y-fiambres/quesos', 'quantity': 154}, {'subcat': 'quesos-y-fiambres/fiambres', 'quantity': 60}, {'subcat': 'quesos-y-fiambres/salchichas', 'quantity': 12}, {'subcat': 'carnes/carne-vacuna', 'quantity': 14}, {'subcat': 'carnes/carne-de-cerdo', 'quantity': 2}, {'subcat': 'carnes/carne-de-pollo', 'quantity': 1}, {'subcat': 'carnes/embutidos', 'quantity': 2}, {'subcat': 'carnes/pescados', 'quantity': 9}, {'subcat': 'carnes/mariscos', 'quantity': 9}, {'subcat': 'pastas-frescas-y-tapas/levaduras-y-grasas', 'quantity': 5}, {'subcat': 'pastas-frescas-y-tapas/fideos-y-ñoquis', 'quantity': 8}, {'subcat': 'pastas-frescas-y-tapas/pastas-rellenas', 'quantity': 28}, {'subcat': 'pastas-frescas-y-tapas/tapas', 'quantity': 25}, {'subcat': 'congelados/frutas-congeladas', 'quantity': 3}, {'subcat': 'congelados/verduras-congeladas', 'quantity': 15}, {'subcat': 'congelados/papas-congeladas', 'quantity': 14}, {'subcat': 'congelados/comidas-preparadas', 'quantity': 62}, {'subcat': 'congelados/prefritos-congelados', 'quantity': 16}, {'subcat': 'congelados/helados-y-postres', 'quantity': 53}, {'subcat': 'congelados/carnes-y-pollo', 'quantity': 3}, {'subcat': 'congelados/hamburguesas-y-milanesas', 'quantity': 62}, {'subcat': 'taeq/almacen-taeq', 'quantity': 9}, {'subcat': 'taeq/frutas-y-verduras-taeq', 'quantity': 14}, {'subcat': 'taeq/congelados-taeq', 'quantity': 9}]
        # for path in paths:
        #     res.append({'subcat': path, 'quantity': requests.get(
        #         f'https://www.hiperlibertad.com.ar/api/catalog_system/pub/facets/search/{path}?map=c,c&sc={self.sc}').json()['Departments'][0]['Quantity']})
        return res

    # Write the first row for each column name

    def __write_first_row(self):
        fields = ['nombre', 'precio_lista', 'precio', 'categoria', 'product_id', 'item_id', 'url', 'stock', 'descripcion', 'marca']
        with open(f'{self.csv_path}{self.csv_filename}.csv', 'w', newline='') as file:
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
        
        with open(f'{self.csv_path}{self.csv_filename}.csv', 'a', newline='') as file:

            writer = csv.DictWriter(file, fieldnames = fields)

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
                        
                        writer.writerow(item)
            
            file.close()

