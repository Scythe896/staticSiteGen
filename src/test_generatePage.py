import unittest
from generatePage import extract_title

class test_generatePage(unittest.TestCase):
    def header(self):
        md = "# header"
        self.assertEqual(extract_title(md), "header")
    def multi_header(self):
        md = '''
## double header

# header'''
        self.assertEqual(extract_title(md), "header")
    def triple_header(self):
        md = "### header"
        with self.assertRaises(ValueError):
            extract_title(md)

    