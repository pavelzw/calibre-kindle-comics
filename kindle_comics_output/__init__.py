from __future__ import (unicode_literals, division, absolute_import, print_function)

import os
import time
from shutil import move

from calibre.customize.conversion import OutputFormatPlugin
from calibre.ebooks.conversion.plugins.mobi_output import MOBIOutput
from calibre.ptempfile import PersistentTemporaryDirectory
from calibre.utils.logging import INFO


class KindleComicsOutput(OutputFormatPlugin):
    name = "Kindle Comics Output"
    author = "Pavel Zwerschke"
    file_type = "mobi"
    version = (0, 0, 1)
    minimum_calibre_version = (5, 0, 0)
    supported_platforms = ["windows", "linux", "osx"]

    options = MOBIOutput.options

    def gui_configuration_widget(self, parent, get_option_by_name, get_option_help, db, book_id=None):
        from calibre_plugins.kindle_comics_output.kindle_comics_output import PluginWidget
        return PluginWidget(parent, get_option_by_name, get_option_help, db, book_id)

    def convert(self, oeb_book, output, input_plugin, opts, log):
        print(input_plugin)

        from calibre_plugins.kindle_comics_output.build_file import build_meta_inf, make_zip, make_mobi

        path = os.path.join(oeb_book.container.rootdir, "..")
        print(path)
        # convert oebbook to epub
        build_meta_inf(path)
        zip_path = os.path.join(PersistentTemporaryDirectory("_epub"), "comic")
        zip_path = make_zip(zip_path, path)

        # convert epub to mobi with kindlegen
        output = make_mobi(zip_path)
        mobi_path = output[2]
        log.prints(INFO, "Created mobi.")

        print(mobi_path, output)
        # move mobi file to destination
        # todo what if output is directory
        move(mobi_path, output)
