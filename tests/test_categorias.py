import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from source.classes.categorias import Categorias

class TestAdd(unittest.TestCase):
    def test_init(self):
        c = Categorias()
        self.assertIsInstance(c, Categorias)

    def test_attributes(self):
        c = Categorias()
        self.assertTrue( len(c.categorias) > 0 )
        self.assertTrue( len(c.subs_for_queries) > 0 )

if __name__ == '__main__':
    unittest.main()