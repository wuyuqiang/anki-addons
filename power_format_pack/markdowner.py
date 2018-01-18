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

import re

from PyQt4 import QtGui

import utility
from anki.utils import json
from power_format_pack import markdown, preferences, const
from power_format_pack.markdown.extensions.abbr import AbbrExtension
from power_format_pack.markdown.extensions.attr_list import AttrListExtension
from power_format_pack.markdown.extensions.codehilite import CodeHiliteExtension
from power_format_pack.markdown.extensions.def_list import DefListExtension
from power_format_pack.markdown.extensions.fenced_code import FencedCodeExtension
from power_format_pack.markdown.extensions.footnotes import FootnoteExtension
from power_format_pack.markdown.extensions.nl2br import Nl2BrExtension
from power_format_pack.markdown.extensions.sane_lists import SaneListExtension
from power_format_pack.markdown.extensions.smart_strong import SmartEmphasisExtension
from power_format_pack.markdown.extensions.tables import TableExtension


class Markdowner(object):
    """
    Convert HTML to Markdown and the other way around. Store the data in the
    field. Revert to previous Markdown or overwrite the data when conflicts
    arise.
    """

    def __init__(self, other, parent_window, note, html, current_field):
        # assert isinstance(html, unicode), "Input `html` is not Unicode"
        self.c              = preferences.CONFIG
        self.p              = preferences.PREFS
        self.editor         = other
        self.parent_window  = parent_window
        self.note           = note
        self.html           = html
        self.backup_html    = ""
        self.current_field  = current_field
        self.note_id_field  = str(self.note.id) + "-{:03}".format(self.current_field)
        self._id            = None
        self.isconverted    = None
        self.md             = None
        self._lastmodified  = None
        self.has_data       = self.get_data_from_field()

    # compare the Markdown that we can reverse engineer from the card's HTML
    # with the Markdown stored in the data structure
    def start(self):
        self.backup_html = self.html

        # definition lists have some quirks
        has_def_list = False
        if "<dl>" in self.html:
            has_def_list = True
            self.create_correct_md_for_def_list()
            self.html = self.note.fields[self.current_field]

        # first, we reverse engineer the Markdown from the rendered card
        clean_md = utility.strip_html_from_markdown(self.html)

        if has_def_list:
            clean_md = utility.remove_leading_whitespace_from_dd_element(clean_md)
        clean_md = utility.remove_whitespace_before_abbreviation_definition(clean_md)
        clean_md_escaped = utility.escape_html_chars(clean_md)

        if not clean_md:
            return

        # HTML --> Markdown
        if self.has_data and self.isconverted == "True":
            # check if the stored data and the current text differ from each other
            compare_md = Markdowner.convert_markdown_to_html(self.md)
            # handle quirks
            compare_md = utility.put_colons_in_html_def_list(compare_md)
            compare_md = utility.strip_html_from_markdown(compare_md)
            if has_def_list:
                compare_md = utility.remove_leading_whitespace_from_dd_element(compare_md)
            compare_md = utility.remove_whitespace_before_abbreviation_definition(compare_md)

            # escape HTML if we haven't done so already
            if not any(x in compare_md for x in("&amp;", "&quot;", "&apos;", "&gt;", "&lt;")):
                compare_md = utility.escape_html_chars(compare_md)
            if utility.is_same_markdown(clean_md_escaped, compare_md) or self.p.get(const.MARKDOWN_ALWAYS_REVERT):
                self.revert_to_stored_markdown()
            else:
                self.handle_conflict()

        # Markdown --> HTML
        else:
            new_html = Markdowner.convert_markdown_to_html(clean_md)
            # needed for proper display of images
            if "<img" in new_html:
                new_html = utility.unescape_html(new_html)
            html_with_data = utility.insert_md_data(self.note_id_field, "True", clean_md_escaped, new_html)
            self.insert_into_field(html_with_data, self.current_field)

            # resolve quirks
            self.align_elements()

    def get_data_from_field(self):
        """
        Get the HTML from the current field and try to extract Markdown data
        from it. The side effect of calling this function is that several
        instance variables get set. Return True when data was found in the
        field, False otherwise.
        """
        compr_dict = utility.get_md_data_from_string(self.html)
        md_dict = utility.decompress_and_json_load(compr_dict)
        if md_dict and md_dict == "corrupted":
            # TODO: fallback when JSON is corrupted
            # TODO: log this
            pass
        elif md_dict:
            self._id            = md_dict.get("id")
            self.md             = md_dict.get("md")
            self.isconverted    = md_dict.get("isconverted")
            self._lastmodified  = md_dict.get("lastmodified")
            return True
        return False

    def insert_into_field(self, markup, field):
        """
        Put markup in the specified field.
        """
        self.editor.web.eval("""
            document.getElementById('f%s').innerHTML = %s;
        """ % (field, json.dumps(unicode(markup))))

    @staticmethod
    def manage_style(editor_instance, field_no):
        editor_instance.web.eval("""
        var field = $('#f%s');
        if (field.html().indexOf('SBAdata:') > -1) {
            var mdstyleExists = false;
            var mdwarningExists = false;
            for (var i = 0, j = document.styleSheets.length; i < j; i++) {
                for (var k = 0, l = document.styleSheets.item(i).cssRules.length; k < l; k++) {
                    var cssRule = document.styleSheets.item(i).cssRules[k].selectorText;
                    if (cssRule.indexOf('.mdstyle') > -1) {
                        mdstyleExists = true;
                    }
                    if (cssRule.indexOf('.mdwarning') > -1) {
                        mdwarningExists = true;
                    }
                }
            }
            if (!mdstyleExists) {
                document.styleSheets.item(0).insertRule('.mdstyle { background-color: %s !important; }', 0);
            }
            if (!mdwarningExists) {
                document.styleSheets.item(0).insertRule('.mdwarning { margin: 10px 0px; }', 0);
            }
        }
        """ % (field_no, const.MARKDOWN_BG_COLOR))

    def add_warning_msg(self, editor_instance, field_no):
        # make sure the .mdwarn CSS class exists
        Markdowner.manage_style(editor_instance, field_no)

        markdown_warning_text = self.c.get(const.CONFIG_TOOLTIPS, "md_warning_editing_tooltip")

        editor_instance.web.eval("""
        var field = $('f%s');
        field.addClass('mdstyle');
        if (!$('#f%s + [class^=mdwarning]').length) {
            field.after($('<div/>', {class: 'mdwarning', text: '%s'}));
        }
        field.attr('title', '%s');
        """ % (field_no, field_no, markdown_warning_text, markdown_warning_text))

    @staticmethod
    def remove_warn_msg(editor_instance, field):
        editor_instance.web.eval("""
            $('#f%s').removeClass('mdstyle');
            $('#f%s + [class^=mdwarning]').remove();
            focusField(%s);
        """ % (field, field, field))

    def handle_conflict(self):
        """
        Show a warning dialog. Based on the user decision, either revert the
        changes to the text, replace the stored data, or cancel.
        """
        ret = self.show_overwrite_warning()
        if ret == 0:
            self.revert_to_stored_markdown()
        elif ret == 1:
            # overwrite data
            self.overwrite_stored_data()
        else:
            self.insert_into_field(self.backup_html, self.current_field)

    def overwrite_stored_data(self):
        """
        Create new Markdown from the current HTML.
        """
        clean_md = utility.strip_html_from_markdown(self.html, keep_empty_lines=True)
        clean_md = utility.remove_whitespace_before_abbreviation_definition(clean_md)
        if "<dl" in self.html:
            clean_md = utility.remove_leading_whitespace_from_dd_element(clean_md, add_newline=True)
        if re.search(const.IS_LINK_OR_IMG_REGEX, clean_md):
            clean_md = utility.escape_html_chars(clean_md)
        new_html = utility.convert_clean_md_to_html(clean_md, put_breaks=True)
        self.insert_into_field(new_html, self.current_field)
        self.remove_warn_msg(self.editor, self.current_field)

    def revert_to_stored_markdown(self):
        """
        Revert to the previous version of Markdown that was stored in the field.
        """
        new_html = utility.convert_clean_md_to_html(self.md, put_breaks=True)
        self.insert_into_field(new_html, self.current_field)
        self.remove_warn_msg(self.editor, self.current_field)

    def show_overwrite_warning(self):
        """
        Show a warning modal dialog box, informing the user that the changes
        have taken place in the formatted text that are not in the Markdown.
        Return a 0 for replacing the new changes with the stored version of
        the Markdown, 1 for overwriting the data, and QMessageBox.Cancel for
        no action.
        """
        mess = QtGui.QMessageBox(self.parent_window)
        mess.setIcon(QtGui.QMessageBox.Warning)
        mess.setWindowTitle(self.c.get(const.CONFIG_WINDOW_TITLES,
                                       "md_overwrite_warning"))
        mess.setText(self.c.get(const.CONFIG_WARNINGS,
                                "md_overwrite_warning_text"))
        mess.setInformativeText(self.c.get(const.CONFIG_WARNINGS,
                                "md_overwrite_warning_additional_text"))
        replace_button = QtGui.QPushButton("&Replace", mess)
        mess.addButton(replace_button, QtGui.QMessageBox.ApplyRole)
        mess.addButton("&Overwrite", QtGui.QMessageBox.ApplyRole)
        mess.setStandardButtons(QtGui.QMessageBox.Cancel)
        mess.setDefaultButton(replace_button)
        return mess.exec_()

    def align_elements(self):
        """
        Left align footnotes, lists, etc. that would otherwise get
        centered or be at the mercy of the general alignment CSS of the card.
        Code blocks can be given a specific `code_direction`.
        """
        # align text in code blocks to the left
        if not self.p.get(const.MARKDOWN_CLASSFUL_PYGMENTS):
            self.editor.web.eval("""
                $('.codehilite').attr('align', 'left');
            """)

        # align the code block itself
        if self.p.get(const.MARKDOWN_CODE_DIRECTION) != const.LEFT:
            self.editor.web.eval("""
                var table = '<table><tbody><tr><td></td></tr></tbody></table>';
                $('.codehilite:not(.codehilitetable .codehilite)').wrap(table);
                $('.codehilite').parents().filter('table').addClass('codehilitetable').attr('align', '%s');
            """ % self.p.get(const.MARKDOWN_CODE_DIRECTION))

        # definition lists, lists
        self.editor.web.eval("""
            $('dt,dd,li').css('text-align', 'left');
        """)

    def create_correct_md_for_def_list(self):
        """
        Change the input `md` to make sure it will transform to the
        correct HTML.
        """
        self.editor.web.eval("""\
            var dds = document.getElementsByTagName('dd');
            for (var i = 0; i < dds.length; i++) {
                var theDD = dds[i];
                firstChild = theDD.firstChild;
                if (firstChild === null) {
                    var text = document.createTextNode(': ');
                    theDD.appendChild(text);
                } else {
                    theDD.firstChild.nodeValue = ': ' + theDD.firstChild.nodeValue;
                }
                if (theDD.nextSibling !== null &&
                        theDD.nextSibling.tagName === 'DT') {
                    var br = document.createElement('br');
                    theDD.parentNode.insertBefore(br, theDD.nextSibling);
                }
            }
        """)
        self.editor.web.setFocus()
        self.editor.web.eval("focusField(%d);" % self.current_field)
        self.editor.saveNow()

    @staticmethod
    def convert_markdown_to_html(clean_md):
        """
        Take a string `clean_md` and return a string where the Markdown syntax is
        converted to HTML.

        >>> preferences.PREFS = {"markdown_classful_pygments": True, "markdown_syntax_style": "tango", "markdown_line_nums": False}
        >>> convert_markdown_to_html(u"this **was** a triumph")
        u'<p>this <strong>was</strong> a triumph</p>'
        """

        # assert isinstance(clean_md, unicode), "Input `clean_md` is not Unicode"

        new_html = markdown.markdown(clean_md, output_format="xhtml1",
            extensions=[
                SmartEmphasisExtension(),
                FencedCodeExtension(),
                FootnoteExtension(),
                AttrListExtension(),
                DefListExtension(),
                TableExtension(),
                AbbrExtension(),
                Nl2BrExtension(),
                CodeHiliteExtension(
                    noclasses=not preferences.PREFS.get(const.MARKDOWN_CLASSFUL_PYGMENTS),
                    pygments_style=preferences.PREFS.get(const.MARKDOWN_SYNTAX_STYLE),
                    linenums=preferences.PREFS.get(const.MARKDOWN_LINE_NUMS)),
                SaneListExtension()
            ], lazy_ol=False)

        # assert isinstance(new_html, unicode)

        return new_html
