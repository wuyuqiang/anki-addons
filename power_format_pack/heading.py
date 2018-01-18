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
import BeautifulSoup

from PyQt4 import QtGui, QtCore
import utility
import const


class Heading(object):
    """
    Create a heading.
    """
    def __init__(self, other, parent_window, selected_text):
        self.editor_instance    = other
        self.selected_text      = selected_text
        self.parent_window      = parent_window
        self.create_heading_from_selection()

    def create_heading_from_selection(self):
        selection = self.selected_text
        if not selection:
            # if no text is selected, show a dialog
            self.create_custom_heading()
            return
        soup = BeautifulSoup.BeautifulSoup(selection)
        size = utility.check_size_heading(soup.text)
        if size == -1:
            self.create_custom_heading(soup.text)
            return
        # remove all headings from selection
        for tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            for match in soup.findAll(tag):
                match.replaceWithChildren()

        # delete leading hashes
        relevant_text = soup.text[size:]
        relevant_text = utility.strip_leading_whitespace(relevant_text)

        # wrap new heading around the selection
        result_soup = BeautifulSoup.BeautifulSoup()
        tag = BeautifulSoup.Tag(result_soup, "h{0!s}".format(size))
        result_soup.insert(0, tag)
        tag.insert(0, relevant_text)

        self.editor_instance.web.eval(
                "document.execCommand('insertHTML', false, %s);"
                % json.dumps(unicode(result_soup)))

        self.cleanup_headings()

    def create_custom_heading(self, selected_text=None):
        dialog = QtGui.QDialog(self.parent_window)
        dialog.setWindowTitle("Create custom heading")

        text_label = QtGui.QLabel("Text:", dialog)
        text_line_edit = QtGui.QLineEdit(dialog)
        if selected_text:
            text_line_edit.setText(selected_text)

        text_hbox = QtGui.QHBoxLayout()
        text_hbox.addWidget(text_label)
        text_hbox.addWidget(text_line_edit)

        groupbox = QtGui.QGroupBox("Choose a size", dialog)
        groupbox.setStyleSheet(const.QGROUPBOX_STYLE)

        radio_button1 = QtGui.QRadioButton("Biggest", dialog)
        radio_button1.setChecked(True)
        radio_button2 = QtGui.QRadioButton("Big", dialog)
        radio_button3 = QtGui.QRadioButton("Medium", dialog)
        radio_button4 = QtGui.QRadioButton("Small", dialog)
        radio_button5 = QtGui.QRadioButton("Smaller", dialog)
        radio_button6 = QtGui.QRadioButton("Tiny", dialog)

        radio_button_group = QtGui.QButtonGroup(dialog)
        radio_button_group.addButton(radio_button1)
        radio_button_group.setId(radio_button1, 1)
        radio_button_group.addButton(radio_button2)
        radio_button_group.setId(radio_button2, 2)
        radio_button_group.addButton(radio_button3)
        radio_button_group.setId(radio_button3, 3)
        radio_button_group.addButton(radio_button4)
        radio_button_group.setId(radio_button4, 4)
        radio_button_group.addButton(radio_button5)
        radio_button_group.setId(radio_button5, 5)
        radio_button_group.addButton(radio_button6)
        radio_button_group.setId(radio_button6, 6)

        radio_hbox = QtGui.QHBoxLayout()
        radio_hbox.addWidget(radio_button1)
        radio_hbox.addWidget(radio_button2)
        radio_hbox.addWidget(radio_button3)
        radio_hbox.addWidget(radio_button4)
        radio_hbox.addWidget(radio_button5)
        radio_hbox.addWidget(radio_button6)

        groupbox.setLayout(radio_hbox)

        button_box = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok |
                                            QtGui.QDialogButtonBox.Cancel,
                                            QtCore.Qt.Horizontal, dialog)

        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(text_hbox)
        vbox.addStretch(1)
        vbox.addWidget(groupbox)
        vbox.addWidget(button_box)

        vbox.setSizeConstraint(QtGui.QLayout.SetFixedSize)

        dialog.setLayout(vbox)

        if dialog.exec_() == QtGui.QDialog.Accepted:
            text = unicode(text_line_edit.text())
            size_heading = radio_button_group.id(
                    radio_button_group.checkedButton())
            heading_tag = "h" + str(size_heading)
            if text == "":
                return
            else:
                text = utility.escape_html_chars(text)
                start_tag = "<{0}>".format(heading_tag)
                end_tag = "</{0}>".format(heading_tag)
                if selected_text:
                    self.editor_instance.web.eval(
                            "wrap('{0}', '{1}')".format(start_tag, end_tag))
                    self.cleanup_headings()
                else:
                    result = u"{0}{1}{2}".format(start_tag, text, end_tag)
                    self.editor_instance.web.eval(
                            "document.execCommand('insertHTML', false, %s);"
                            % json.dumps(unicode(result)))

    def cleanup_headings(self):
        """
        Clean up empty headers from the card.
        """
        self.editor_instance.saveNow()
        self.editor_instance.web.setFocus()
        self.editor_instance.web.eval(
                "focusField(%d);" % self.editor_instance.currentField)

        html = self.editor_instance.note.fields[self.editor_instance.currentField]
        soup = BeautifulSoup.BeautifulSoup(html)

        for tag in const.HEADING_TAGS:
            for match in soup.findAll(tag):
                if match.parent.name in const.HEADING_TAGS:
                    match.parent.replaceWithChildren()

        self.editor_instance.note.fields[self.editor_instance.currentField] = \
            unicode(soup)
        self.editor_instance.loadNote()
