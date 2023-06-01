import asyncio
# import sys
# import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from classes.sucursal import Sucursal
from classes.categorias import Categorias


if __name__ == '__main__':

    c = Categorias()

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

    while True:
        op = int(input(
            '1. Generar csv de una sucursal.\n2. Generar csv de todas las sucursales.\n0. Salir\n\t'))
        if op == 0:
            break
        if op == 1:
            print("\n")
            for suc in sucursales:
                print(suc, sucursales[suc])
            sc = int(input('\tIngrese un numero:'))

            csv_path = input(
                '\nIngrese carpeta de destino (por default \'csv\' del proyecto):')
            csv_filename = input('Nombre del CSV (default \'sucursal-#sc\'):')
            s = Sucursal(sc=sc, subcat_paths=c.subs_for_queries,
                         csv_filename=csv_filename, csv_path=csv_path)

            # We run this command in order to get an estimate of
            # how many queries to process per category.
            asyncio.run(s.get_subcat_quantity())
            asyncio.run(s.get_catalog())
        else:
            for sc in sucursales:
                s = Sucursal(sc=sc, subcat_paths=c.subs_for_queries)
                asyncio.run(s.get_subcat_quantity())
                asyncio.run(s.get_catalog())
