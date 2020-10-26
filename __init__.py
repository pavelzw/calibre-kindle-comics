import os
import shutil, codecs, textwrap

from calibre.customize.conversion import InputFormatPlugin, OptionRecommendation
from calibre.ebooks.conversion.plugins.comic_input import ComicInput
from calibre.ebooks.conversion.plugins.epub_input import EPUBInput


class KindleComics(InputFormatPlugin):
    name = 'Kindle Comics'
    author = 'Pavel Zwerschke'
    supported_platforms = ['windows', 'osx', 'linux']
    file_types = {'cbz', 'cbr', 'cb7'}
    version = (0, 0, 1)
    description = 'Converts cbz and cbr files into a kindle format that is actually readable on Kindle devices.'

    minimum_calibre_version = (5, 0, 0)

    options = {
        OptionRecommendation(name='manga', recommended_value=False,
                             help='Used for right-to-left publications like manga.'),
        OptionRecommendation(name='webtoon', recommended_value=False,
                             help='Used for korean webtoons.'),
        OptionRecommendation(name='margins', choices=['auto', 'black', 'white'],
                             recommended_value='auto', help='What color should the margins have.'),
        OptionRecommendation(name='no_greyscale', recommended_value=False,
                             help='Don\'t convert the image to grayscale (black and white).'),
        OptionRecommendation(name='max_width', recommended_value=1264,
                             help='Maximum width.'),
        OptionRecommendation(name='max_height', recommended_value=1680,
                             help='Maximum height.'),
    }

    def gui_configuration_widget(self, parent, get_option_by_name, get_option_help, db, book_id=None):
        from calibre_plugins.kindle_comics.kindle_comics import PluginWidget
        return PluginWidget(parent, get_option_by_name, get_option_help, db, book_id)

    def convert(self, stream, options, file_ext, log, accelerators):
        pass
