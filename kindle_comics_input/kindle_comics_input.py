from __future__ import (unicode_literals, division, absolute_import, print_function)

from PyQt5 import (QtCore, QtWidgets)
from PyQt5.QtWidgets import QLabel

from calibre.gui2.convert import Widget


class PluginWidget(Widget):
    TITLE = "Kindle Comics Input"
    HELP = "Options specific to Kindle Comics Input"
    # ICON = ...
    COMMIT_NAME = "kindle_comics_input"

    def __init__(self, parent, get_option, get_help, db=None, book_id=None):
        self.db = db                # db is set for conversion, but not default preferences
        self.book_id = book_id      # book_id is set for individual conversion, but not bulk

        # todo webtoon
        # Widget.__init__(self, parent, ["manga", "webtoon", "margins", "no_greyscale", "max_width", "max_height"])
        Widget.__init__(self, parent, ["manga", "margins", "no_greyscale", "max_width", "max_height"])
        self.initialize_options(get_option, get_help, db, book_id)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowTitle("Form")
        Form.resize(588, 481)

        self.formLayout = QtWidgets.QFormLayout(Form)
        self.formLayout.setObjectName("formLayout")

        # Manga mode
        self.opt_manga = QtWidgets.QCheckBox(Form)
        self.opt_manga.setObjectName("manga")
        self.opt_manga.setText("Manga mode (right-to-left)")
        self.formLayout.addRow(self.opt_manga)

        # Webtoon mode todo not tested yet
        # self.opt_webtoon = QtWidgets.QCheckBox(Form)
        # self.opt_webtoon.setObjectName("webtoon")
        # self.opt_webtoon.setText("Korean webtoons")
        # self.formLayout.addRow(self.opt_webtoon)

        # W/B margins
        self.margins_label = QLabel('Margins')
        self.formLayout.addRow(self.margins_label)

        self.opt_margins = QtWidgets.QComboBox(Form)
        self.opt_margins.setObjectName("margins")
        self.opt_margins.addItem("auto")
        self.opt_margins.addItem("white")
        self.opt_margins.addItem("black")
        self.formLayout.addRow(self.opt_margins)

        # No greyscale
        self.opt_no_greyscale = QtWidgets.QCheckBox(Form)
        self.opt_no_greyscale.setObjectName("no_greyscale")
        self.opt_no_greyscale.setText("Don't convert to greyscale")
        self.formLayout.addRow(self.opt_no_greyscale)

        # Max width
        self.max_width_label = QLabel('Maximum width:')
        self.formLayout.addRow(self.max_width_label)

        self.opt_max_width = QtWidgets.QLineEdit(Form)
        self.opt_max_width.setObjectName("max_width")
        self.formLayout.addRow(self.opt_max_width)

        # Max height
        self.max_height_label = QLabel('Maximum height:')
        self.formLayout.addRow(self.max_height_label)

        self.opt_max_height = QtWidgets.QLineEdit(Form)
        self.opt_max_height.setObjectName("max_height")
        self.formLayout.addRow(self.opt_max_height)

        QtCore.QMetaObject.connectSlotsByName(Form)
