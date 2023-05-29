from classes.sucursal import Sucursal
from classes.categorias import Categorias

import asyncio
import aiohttp

# Logging:
# I was thinking about making a CLI if it doesn't take too much time.
#

if __name__ == '__main__':

    c = Categorias()
    s = Sucursal(sc=1, subcat_paths=c.subs_for_queries, csv_path="csv/")

    asyncio.run(s.get_subcat_quantity())
    print(s.subcats)
    print("\n")
    #asyncio.run(s.get_catalog())
