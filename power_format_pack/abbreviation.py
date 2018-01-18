# -*- coding: utf-8 -*-
#
# Copyright 2014-2017 Stefan van den Akker <neftas@protonmail.com>
#
# This file is part of Power Format Pack.
#
# Power Format Pack is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Power Format Pack is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with Power Format Pack. If not, see http://www.gnu.org/licenses/.

import string
import random

from PyQt4 import QtGui
import utility


class Abbreviation(object):
    def __init__(self, other, parent_window, selected_text):
        self.editor_instance = other
        self.parent_window = parent_window
        self.selected_text = selected_text
        self.abbreviation_dialog()

    def abbreviation_dialog(self):
        """Creates a dialog window where the user can enter data for the HTML
        tag <abbr>, for both the abbreviation and the title attribute."""
        dialog = QtGui.QDialog(self.parent_window)
        dialog.setWindowTitle("Create an abbreviation")
        dialog.resize(350, 200)

        # OK and Cancel button
        ok_button = QtGui.QPushButton("&Ok", dialog)
        ok_button.setEnabled(False)
        ok_button.clicked.connect(lambda: self.insert_abbreviation(
            text_edit.text(), title_edit.text()))
        ok_button.clicked.connect(dialog.hide)

        cancel_button = QtGui.QPushButton("&Cancel", dialog)
        cancel_button.clicked.connect(dialog.hide)
        cancel_button.setAutoDefault(True)

        # two labels: one for the text, one for the title attribute
        text_label = QtGui.QLabel("Text:")
        title_label = QtGui.QLabel("Title:")

        # two text fields: one for the text,
        # the other for the content of the title attribute
        text_edit = QtGui.QLineEdit()
        text_edit.setPlaceholderText("Text")
        text_edit.textChanged.connect(lambda: self.enable_ok_button(
            ok_button, text_edit.text(), title_edit.text()))

        title_edit = QtGui.QLineEdit()
        title_edit.setPlaceholderText("Abbreviation")
        title_edit.textChanged.connect(lambda: self.enable_ok_button(
            ok_button, text_edit.text(), title_edit.text()))

        # if user already selected text, we put it in the text edit field
        if self.selected_text:
            text_edit.setText(self.selected_text)

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(cancel_button)
        hbox.addWidget(ok_button)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(text_label)
        vbox.addWidget(text_edit)
        vbox.addWidget(title_label)
        vbox.addWidget(title_edit)
        vbox.addLayout(hbox)

        dialog.setLayout(vbox)

        if self.selected_text:
            title_edit.setFocus()
        else:
            text_edit.setFocus()

        dialog.exec_()

    def enable_ok_button(self, button, text, title):
        if text and title:
            button.setEnabled(True)
        else:
            button.setEnabled(False)

    def insert_abbreviation(self, text, title):
        # escape HTML
        text = utility.escape_html_chars(text)
        title = utility.escape_html_chars(title)
        # unicode
        # assert isinstance(text, unicode)
        # assert isinstance(title, unicode)
        # create new tag
        div_id = "".join(random.choice(string.ascii_letters) for _ in xrange(20))
        self.editor_instance.web.eval("""\
                var abbr = document.createElement('abbr');
                var text = document.createTextNode('%s');
                abbr.appendChild(text);
                abbr.setAttribute('title', '%s');
                abbr.id = '%s';
                var marker = '@#!';
                var toBeInserted = marker + abbr.outerHTML + marker;
                document.execCommand('insertHTML', false, toBeInserted);
                var elem = document.getElementById('%s');
                var leftString = elem.previousSibling.nodeValue;
                var rightString = elem.nextSibling.nodeValue;
                elem.previousSibling.nodeValue =
                        leftString.substring(0, (leftString.length - marker.length));
                elem.nextSibling.nodeValue =
                        rightString.substring(marker.length);
                elem.removeAttribute('id');
        """ % (text, title, div_id, div_id))
