from __future__ import (unicode_literals, division, absolute_import, print_function)

from calibre.customize.conversion import OutputFormatPlugin
from calibre.ebooks.conversion.plugins.mobi_output import MOBIOutput


class KindleComicsOutput(OutputFormatPlugin):
    name = "Kindle Comics Output"
    author = "Pavel Zwerschke"
    file_type = "epub"
    version = (0, 0, 1)
    minimum_calibre_version = (5, 0, 0)
    supported_platforms = ["windows", "linux", "osx"]

    options = MOBIOutput.options

    def gui_configuration_widget(self, parent, get_option_by_name, get_option_help, db, book_id=None):
        from calibre_plugins.kindle_comics_output.kindle_comics_output import PluginWidget
        return PluginWidget(parent, get_option_by_name, get_option_help, db, book_id)

    def convert(self, oeb_book, output, input_plugin, opts, log):
        raise ValueError("END")