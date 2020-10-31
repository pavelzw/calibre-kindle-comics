__license__ = "GPL v2+"
__copyright__ = "2019, Mikhail Korobov <kmike84@gmail.com>"

# -*- coding: utf-8 -*-
import os
import sys
import zipfile

# .../Kindle Comics.zip/kindle_comic_lib/text_unidecode
module_path = os.path.dirname(sys.modules[__name__].__file__)
# .../Kindle Comics.zip
zip_path = os.path.join(module_path, '../..')
path_in_zip = "kindle_comic_lib/text_unidecode/data.bin"

archive = zipfile.ZipFile(zip_path, 'r')
data = archive.read(path_in_zip)

_replaces = data.decode('utf8').split('\x00')

def unidecode(txt):
    chars = []
    for ch in txt:
        codepoint = ord(ch)

        if not codepoint:
            chars.append('\x00')
            continue

        try:
            chars.append(_replaces[codepoint-1])
        except IndexError:
            pass
    return "".join(chars)
