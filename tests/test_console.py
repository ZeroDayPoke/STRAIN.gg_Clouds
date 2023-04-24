#!/usr/bin/python3
"""Console Testing Module"""
import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from io import StringIO
from contextlib import redirect_stdout
from app.console import StrainConsole
from app.models import storage
from app.models.strain import Strain

class TestStrainConsole(unittest.TestCase):

    def setUp(self):
        self.console = StrainConsole()

    def test_create_strain(self):
        with StringIO() as buf, redirect_stdout(buf):
            self.console.onecmd('create Strain name=TestStrain type=Indica delta_nine_concentration=10 cbd_concentration=5 terpene_profile=test effects=test uses=test flavor=test')
            output = buf.getvalue()
        self.assertIn("TestStrain created with ID", output)
        strain = storage.all('Strain').values()
        self.assertEqual(len(strain), 1)

    def test_all_strains(self):
        self.console.onecmd('create Strain name=TestStrain1 type=Indica delta_nine_concentration=10 cbd_concentration=5 terpene_profile=test effects=test uses=test flavor=test')
        self.console.onecmd('create Strain name=TestStrain2 type=Sativa delta_nine_concentration=15 cbd_concentration=5 terpene_profile=test effects=test uses=test flavor=test')

        with StringIO() as buf, redirect_stdout(buf):
            self.console.onecmd('all Strain')
            output = buf.getvalue()

        self.assertIn("TestStrain1", output)
        self.assertIn("TestStrain2", output)

if __name__ == "__main__":
    unittest.main()
