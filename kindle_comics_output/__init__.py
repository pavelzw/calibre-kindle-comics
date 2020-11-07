from __future__ import (unicode_literals, division, absolute_import, print_function)

import os
import sys
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
    supported_platforms = ['windows', 'osx', 'linux']

    options = MOBIOutput.options

    def convert(self, oeb_book, output, input_plugin, opts, log):
        if input_plugin.name != "Kindle Comics Input":
            log.prints(INFO, "Executing default mobi plugin.")
            from calibre.ebooks.conversion.plugins.mobi_output import MOBIOutput
            plugin_path = os.path.join(sys.modules[MOBIOutput.__module__].__file__)
            mobi_output_plugin = MOBIOutput(plugin_path)
            mobi_output_plugin.convert(oeb_book, output, input_plugin, opts, log)
        else:
            log.prints(INFO, "Executing Kindle Comic Output plugin.")
            from calibre_plugins.kindle_comics_output.build_file \
                import build_meta_inf, make_zip, make_mobi, write_metadata_to_opf

            # convert oebbook to epub
            metadata = oeb_book.metadata
            path = os.path.join(oeb_book.container.rootdir, "..")
            write_metadata_to_opf(os.path.join(path, "OEBPS", "content.opf"), metadata)

            build_meta_inf(path)
            log.prints(INFO, "Make epub file...")
            zip_path = os.path.join(PersistentTemporaryDirectory("_epub"), "comic")
            zip_path = make_zip(zip_path, path)

            # convert epub to mobi with kindlegen
            mobi_output = make_mobi(zip_path)
            mobi_path = mobi_output[2]
            log.prints(INFO, "Created mobi.")

            # move mobi file to destination
            # todo what if output is directory
            move(mobi_path, output)
