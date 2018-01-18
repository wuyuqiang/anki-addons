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

import json

from PyQt4 import QtGui
import utility
import const


class Hyperlink(object):
    def __init__(self, other, parent_window, selected_text):
        self.editor_instance    = other
        self.parent_window      = parent_window
        self.selected_text      = selected_text
        self.hyperlink_dialog()

    def hyperlink_dialog(self):
        dialog = QtGui.QDialog(self.parent_window)
        dialog.setWindowTitle("Create a hyperlink")
        dialog.resize(const.DIALOG_SIZE_X, const.DIALOG_SIZE_Y)

        ok_button_anchor = QtGui.QPushButton("&OK", dialog)
        ok_button_anchor.setEnabled(False)
        ok_button_anchor.clicked.connect(lambda: self.insert_anchor(
            url_edit.text(), urltext_edit.text()))
        ok_button_anchor.clicked.connect(dialog.hide)

        ok_button_anchor.setAutoDefault(True)

        cancel_button_anchor = QtGui.QPushButton("&Cancel", dialog)
        cancel_button_anchor.clicked.connect(dialog.hide)
        cancel_button_anchor.setAutoDefault(True)

        url_label = QtGui.QLabel("Link to:")
        url_edit = QtGui.QLineEdit()
        url_edit.setPlaceholderText("URL")
        url_edit.textChanged.connect(lambda: self.enable_ok_button(
            ok_button_anchor, url_edit.text(), urltext_edit.text()))

        urltext_label = QtGui.QLabel("Text to display:")
        urltext_edit = QtGui.QLineEdit()
        urltext_edit.setPlaceholderText("Text")
        urltext_edit.textChanged.connect(lambda: self.enable_ok_button(
            ok_button_anchor, url_edit.text(), urltext_edit.text()))

        # if user already selected text, put it in urltext_edit
        if self.selected_text:
            urltext_edit.setText(self.selected_text)

        button_box = QtGui.QHBoxLayout()
        button_box.addStretch(1)
        button_box.addWidget(cancel_button_anchor)
        button_box.addWidget(ok_button_anchor)

        dialog_vbox = QtGui.QVBoxLayout()
        dialog_vbox.addWidget(url_label)
        dialog_vbox.addWidget(url_edit)
        dialog_vbox.addWidget(urltext_label)
        dialog_vbox.addWidget(urltext_edit)
        dialog_vbox.addLayout(button_box)

        dialog.setLayout(dialog_vbox)

        # give url_edit focus
        url_edit.setFocus()

        dialog.exec_()

    @staticmethod
    def enable_ok_button(button, url, text):
        if url and text:
            button.setEnabled(True)
        else:
            button.setEnabled(False)

    @staticmethod
    def create_anchor(url, text):
        """
        Create a hyperlink string, where `url` is the hyperlink reference
        and `text` the content of the tag.
        """
        # assert isinstance(url, unicode), "Input `url` is not Unicode"
        # assert isinstance(text, unicode), "Input `text` is not Unicode"

        text = utility.escape_html_chars(text)

        return u"<a href=\"{0}\">{1}</a>".format(url, text)

    def insert_anchor(self, url, text):
        """
        Inserts a HTML anchor `<a>` into the text field.
        """
        replacement = self.create_anchor(url, text)
        self.editor_instance.web.eval(
                "document.execCommand('insertHTML', false, %s);"
                % json.dumps(replacement))
