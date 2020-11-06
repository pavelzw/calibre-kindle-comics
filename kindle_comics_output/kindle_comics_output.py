from __future__ import (unicode_literals, division, absolute_import, print_function)

from PyQt5 import (QtCore, QtWidgets)

from calibre.gui2.convert import Widget

class PluginWidget(Widget):
    TITLE = "Kindle Comics Output"
    HELP = "Options specific to Kindle Comics Output"
    # ICON = ...
    COMMIT_NAME = "kindle_comics_output"

    def __init__(self, parent, get_option, get_help, db=None, book_id=None):
        self.db = db                # db is set for conversion, but not default preferences
        self.book_id = book_id      # book_id is set for individual conversion, but not bulk

        Widget.__init__(self, parent, [])
        self.initialize_options(get_option, get_help, db, book_id)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowTitle("Form")
        Form.resize(588, 481)

        self.formLayout = QtWidgets.QFormLayout(Form)
        self.formLayout.setObjectName("formLayout")

        self.lbl = QtWidgets.QLabel("TODO")
        self.formLayout.addRow(self.lbl)

        QtCore.QMetaObject.connectSlotsByName(Form)
