import os

from calibre.customize.conversion import InputFormatPlugin, OptionRecommendation


class KindleComics(InputFormatPlugin):
    name = 'Kindle Comics Input'
    author = 'Pavel Zwerschke'
    supported_platforms = ['windows', 'osx', 'linux']
    file_types = {'cbz', 'cbr'}
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
                             help='Maximum height.')
    }

    def gui_configuration_widget(self, parent, get_option_by_name, get_option_help, db, book_id=None):
        from calibre_plugins.kindle_comics.kindle_comics_input import PluginWidget
        return PluginWidget(parent, get_option_by_name, get_option_help, db, book_id)

    def convert(self, stream, options, file_ext, log, accelerators):
        from calibre_plugins.kindle_comics.make_book import make_book
        book = os.path.abspath(stream.name)
        stream.close()
        opt_file = make_book(_convert_options_to_dict(options), book, log)

        return opt_file


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
    if options.margins == 'auto':
        black_borders = False
        white_borders = False
        borders_color = None
    elif options.margins == 'white':
        black_borders = False
        white_borders = True
        borders_color = 'white'
    else:  # black
        black_borders = True
        white_borders = False
        borders_color = 'black'

    opts = {
        'manga': options.manga,
        'webtoon': options.webtoon,
        'margins': options.margins,
        'no_greyscale': options.no_greyscale,
        'max_width': int(options.max_width),
        'max_height': int(options.max_height),

        'black_borders': black_borders,
        'white_borders': white_borders,
        'bordersColor': borders_color,
        'profileData': ('Kindle Paperwhite 3/4/Voyage/Oasis', (int(options.max_width), int(options.max_height)),
                        palette, 1.8),
        'profile': 'KV',
        'hq': False,
        'forcecolor': options.no_greyscale,
        'forcepng': False,
        'gamma': 0.0,
        'stretch': False,
        'kfx': False,
        'upscale': False,
        'format': "MOBI",
        'cropping': 2,
        'croppingp': 1.0,
        'splitter': 0,
        'iskindle': True,
        'panelview': True,
        'covers': [],
        'autoscale': False,
        'righttoleft': options.manga,
        'summary': "",
        'authors': ["unknown"],
        'chapters': False,
        'batchsplit': 1,
        'customheight': 0,
        'customwidth': 0,
        'output': None,
        'title': 'defaulttitle'
    }
    return opts
