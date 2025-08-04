
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))
from preprocessing import lower_turkish, expand_abbreviations


class TestPreprocessing(unittest.TestCase):
    
    def test_lower_turkish(self):
        self.assertEqual(lower_turkish("İSTANBUL"), "istanbul")
        self.assertEqual(lower_turkish("Çağ"), "cag")
        self.assertEqual(lower_turkish("ĞÜNEŞ"), "gunes")
        self.assertEqual(lower_turkish("Öğretmen"), "ogretmen")
        self.assertEqual(lower_turkish("ŞARKICI"), "sarkici")
        self.assertEqual(lower_turkish("Ümit"), "umit")
        self.assertEqual(lower_turkish("I love Istanbul"), "i love istanbul")
    
    def test_expand_abbreviations(self):
        self.assertEqual(expand_abbreviations("Atatürk cad. No: 5"), "Atatürk cadde No: 5")
        self.assertEqual(expand_abbreviations("Atatürk Cad. No: 5"), "Atatürk cadde No: 5")
        self.assertEqual(expand_abbreviations("Beşiktaş mah."), "Beşiktaş mahalle")
        self.assertEqual(expand_abbreviations("İstiklal sk."), "İstiklal sokak")
        self.assertEqual(expand_abbreviations("mah. ve cad."), "mahalle ve cadde")
        self.assertEqual(expand_abbreviations("Normal metin"), "Normal metin")


if __name__ == '__main__':
    unittest.main()