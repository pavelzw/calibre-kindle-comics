import os
import time

from calibre.customize.conversion import InputFormatPlugin, OptionRecommendation


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
        OptionRecommendation(name='max_width', recommended_value="1264",
                             help='Maximum width.'),
        OptionRecommendation(name='max_height', recommended_value="1680",
                             help='Maximum height.'),

        OptionRecommendation(name='bordersColor', recommended_value=True,
                             help='PLACEHOLDER.'),
        OptionRecommendation(name='profileData', recommended_value=0, #todo gamma
                             help='PLACEHOLDER.'),
        OptionRecommendation(name='hq', recommended_value=True,
                             help='PLACEHOLDER.'),
        OptionRecommendation(name='forceColor', recommended_value=False,
                             help='PLACEHOLDER.'),
        OptionRecommendation(name='forcepng', recommended_value=False,
                             help='PLACEHOLDER.'),
        OptionRecommendation(name='gamma', recommended_value=0,
                             help='PLACEHOLDER.'),
        OptionRecommendation(name='stretch', recommended_value=False,
                             help='PLACEHOLDER.'),
        OptionRecommendation(name='kfx', recommended_value=False,
                             help='PLACEHOLDER.'),
        OptionRecommendation(name='upscale', recommended_value=True,
                             help='PLACEHOLDER.'),
        OptionRecommendation(name='format', recommended_value="CBR",
                             help='PLACEHOLDER.'),
    }

    def gui_configuration_widget(self, parent, get_option_by_name, get_option_help, db, book_id=None):
        from calibre_plugins.kindle_comics.kindle_comics import PluginWidget
        return PluginWidget(parent, get_option_by_name, get_option_help, db, book_id)

    def convert(self, stream, options, file_ext, log, accelerators):
        from calibre_plugins.kindle_comics.make_book import make_book
        book = os.path.abspath(stream.name)
        stream.close()
        make_book(_convert_options_to_dict(options), book, log)

        print("SLEEPING 30")
        if options.manga:
            time.sleep(30)
        return None


def _convert_options_to_dict(options):
    # self.options is only usable in __init__.py, it needs to be converted for other modules
    palette = [
        0x00, 0x00, 0x00,
        0x11, 0x11, 0x11,
        0x22, 0x22, 0x22,
        0x33, 0x33, 0x33,
        0x44, 0x44, 0x44,
        0x55, 0x55, 0x55,
        0x66, 0x66, 0x66,
        0x77, 0x77, 0x77,
        0x88, 0x88, 0x88,
        0x99, 0x99, 0x99,
        0xaa, 0xaa, 0xaa,
        0xbb, 0xbb, 0xbb,
        0xcc, 0xcc, 0xcc,
        0xdd, 0xdd, 0xdd,
        0xee, 0xee, 0xee,
        0xff, 0xff, 0xff,
    ]
    opts = {
        'manga': options.manga,
        'webtoon': options.webtoon,
        'margins': options.margins,
        'no_greyscale': options.no_greyscale,
        'max_width': int(options.max_width),
        'max_height': int(options.max_height),

        'bordersColor': None,
        'profileData': ['Kindle Paperwhite 3/4/Voyage/Oasis', (1072, 1448), palette, 1.8],
        'hq': False,
        'forceColor': False,
        'forcecolor': False,
        'forcepng': False,
        'gamma': 0,
        'stretch': False,
        'kfx': False,
        'upscale': True,
        'format': "MOBI",
        'cropping': 2,
        'croppingp': 1.0,
        'splitter': 1,

        # 'bordersColor': options.bordersColor,
        # 'profileData': options.profileData,
        # 'hq': options.hq,
        # 'forceColor': options.forcecolor,
        # 'forcepng': options.forcepng,
        # 'gamma': options.gamma,
        # 'stretch': options.stretch,
        # 'kfx': options.kfx,
        # 'upscale': options.upscale,
        # 'format': options.format,
    }
    return opts
