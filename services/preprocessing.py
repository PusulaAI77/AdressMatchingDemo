#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import string


def lower_turkish(text):
    if not isinstance(text, str):
        return str(text)
    
    turkish_char_map = {
        'ç': 'c', 'Ç': 'C',
        'ğ': 'g', 'Ğ': 'G',
        'ı': 'i', 'I': 'I',
        'İ': 'I', 'i': 'i',
        'ö': 'o', 'Ö': 'O',
        'ş': 's', 'Ş': 'S',
        'ü': 'u', 'Ü': 'U'
    }
    
    text = text.replace('I', 'ı')
    text = text.replace('İ', 'i')
    
    text = text.lower()
    
    for turkish_char, english_char in turkish_char_map.items():
        text = text.replace(turkish_char, english_char)
    
    return text


def expand_abbreviations(text):
    if not isinstance(text, str):
        return str(text)
    
    abbreviations = {
        'mah.': 'mahalle',
        'sk.': 'sokak',
        'cad.': 'cadde',
        'blv.': 'bulvar'
    }
    
    result = text
    for abbrev, full_form in abbreviations.items():
        result = result.replace(abbrev, full_form)
        result = result.replace(abbrev.upper(), full_form)
        result = result.replace(abbrev.capitalize(), full_form)
    
    return result

def temizle(text):
      text = lower_turkish(text)
      text = expand_abbreviations(text)
      return text
