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


import warnings
warnings.simplefilter("ignore", UserWarning)

from anki.utils import json
from aqt import editor, mw
from anki.hooks import wrap, addHook
from anki.utils import isWin, isMac
from PyQt4 import QtGui, QtCore
import BeautifulSoup

import utility
import const
import preferences
from preferences import Preferences
from prefhelper import PrefHelper
from menu import Options
from markdowner import Markdowner
from anki_modules.aqt import editor as myeditor
from anki_modules.aqt.editor import create_button
from abbreviation import Abbreviation
from orderedlist import OrderedList
from hyperlink import Hyperlink
from deflist import DefList
from table import Table
from blockquote import Blockquote
from heading import Heading

# Overrides
##################################################
editor.Editor.onHtmlEdit = myeditor.onHtmlEdit
editor.Editor._filterHTML = myeditor._filterHTML


# Buttons
##################################################


def setup_buttons(self):

    button_placement_pref = preferences.PREFS.get(const.BUTTON_PLACEMENT)

    self.supp_buttons_hbox = QtGui.QHBoxLayout()

    if preferences.PREFS.get(const.CODE):
        shortcut = preferences.KEYS.get(const.CODE)
        text = u"Code format text ({})".format(utility.key_to_text(shortcut))
        b = self.create_button(const.CODE,
                               lambda: self.wrap_in_tags("code",
                               preferences.PREFS.get(const.CODE_CLASS)),
                               shortcut,
                               _(text),
                               check=False)

    if preferences.PREFS.get(const.UNORDERED_LIST):
        shortcut = preferences.KEYS.get(const.UNORDERED_LIST)
        text = u"Create unordered list ({})".format(utility.key_to_text(shortcut))
        b = self.create_button(const.UNORDERED_LIST,
                               self.toggleUnorderedList,
                               shortcut,
                               _(text),
                               check=False)

    if preferences.PREFS.get(const.ORDERED_LIST):
        shortcut = preferences.KEYS.get(const.ORDERED_LIST)
        text = u"Create ordered list ({})".format(utility.key_to_text(shortcut))
        b = self.create_button(const.ORDERED_LIST,
                               self.toggleOrderedList,
                               shortcut,
                               _(text),
                               check=False)

    if preferences.PREFS.get(const.STRIKETHROUGH):
        shortcut = preferences.KEYS.get(const.STRIKETHROUGH)
        text = u"Strikethrough text ({})".format(utility.key_to_text(shortcut))
        b = self.create_button(const.STRIKETHROUGH,
                               self.toggleStrikeThrough,
                               shortcut,
                               _(text),
                               check=True)

    # FIXME: think of better symbol to represent a <pre> block
    if preferences.PREFS.get(const.PRE):
        shortcut = preferences.KEYS.get(const.PRE)
        text = u"Create a code block ({})".format(utility.key_to_text(shortcut))
        b = self.create_button(const.PRE,
                               lambda: self.wrap_in_tags("pre", preferences.PREFS.get(const.CODE_CLASS)),
                               shortcut,
                               tip=_(text),
                               check=False)

    if preferences.PREFS.get(const.HORIZONTAL_RULE):
        shortcut = preferences.KEYS.get(const.HORIZONTAL_RULE)
        text = u"Create a horizontal rule ({})".format(utility.key_to_text(shortcut))
        b = self.create_button(const.HORIZONTAL_RULE,
                               self.toggleHorizontalLine,
                               shortcut,
                               tip=_(text),
                               check=False)

    if preferences.PREFS.get(const.INDENT):
        shortcut = preferences.KEYS.get(const.INDENT)
        text = u"Indent text or list ({})".format(utility.key_to_text(shortcut))
        b = self.create_button(const.INDENT,
                               self.toggleIndent,
                               shortcut,
                               _(text),
                               check=False)

    if preferences.PREFS.get(const.OUTDENT):
        shortcut = preferences.KEYS.get(const.OUTDENT)
        text = u"Outdent text or list ({})".format(utility.key_to_text(shortcut))
        b = self.create_button(const.OUTDENT,
                               self.toggleOutdent,
                               shortcut,
                               _(text),
                               check=False)

    # FIXME: better symbol for <dl>
    if preferences.PREFS.get(const.DEFINITION_LIST):
        shortcut = preferences.KEYS.get(const.DEFINITION_LIST)
        text = u"Create definition list ({})".format(utility.key_to_text(shortcut))
        b = self.create_button(const.DEFINITION_LIST,
                               self.toggleDefList,
                               shortcut,
                               _(text),
                               check=False)

    if preferences.PREFS.get(const.TABLE):
        shortcut = preferences.KEYS.get(const.TABLE)
        text = u"Create a table ({})".format(utility.key_to_text(shortcut))
        b = self.create_button(const.TABLE,
                               self.toggleTable,
                               shortcut,
                               _(text),
                               check=False)

    if preferences.PREFS.get(const.KEYBOARD):
        shortcut = preferences.KEYS.get(const.KEYBOARD)
        text = u"Create a keyboard button ({})".format(utility.key_to_text(shortcut))
        b = self.create_button(const.KEYBOARD,
                               lambda: self.wrap_in_tags("kbd"),
                               shortcut,
                               _(text),
                               check=False)

    if preferences.PREFS.get(const.HYPERLINK):
        shortcut = preferences.KEYS.get(const.HYPERLINK)
        text = u"Insert link ({})".format(utility.key_to_text(shortcut))
        b1 = self.create_button(const.HYPERLINK,
                                self.toggleHyperlink,
                                shortcut,
                                _(text),
                                check=False)

        shortcut = preferences.KEYS.get(const.REMOVE_HYPERLINK)
        text = u"Unlink ({})".format(utility.key_to_text(shortcut))
        b2 = self.create_button(const.REMOVE_HYPERLINK,
                                self.unlink,
                                shortcut,
                                _(text),
                                check=False)

    if preferences.PREFS.get(const.BACKGROUND_COLOR):
        shortcut = preferences.KEYS.get(const.BACKGROUND_COLOR)
        text = u"Set background color ({})".format(utility.key_to_text(shortcut))
        b1 = self.create_button(const.BACKGROUND_COLOR,
                                self.on_background,
                                shortcut,
                                _(text),
                                text=" ")
        self.setup_background_button(b1)

        shortcut = preferences.KEYS.get(const.BACKGROUND_COLOR_CHANGE)
        text = u"Change color ({})".format(utility.key_to_text(shortcut))
        b2 = self.create_button(const.BACKGROUND_COLOR_CHANGE,
                                self.on_change_col, shortcut,
                                _(text),
                                # space is needed to center the arrow
                                text=utility.downArrow() + " ")
        b2.setFixedWidth(12)

    if preferences.PREFS.get(const.BLOCKQUOTE):
        shortcut = preferences.KEYS.get(const.BLOCKQUOTE)
        text = u"Insert blockquote ({})".format(utility.key_to_text(shortcut))
        b = self.create_button(const.BLOCKQUOTE,
                               self.toggleBlockquote,
                               shortcut,
                               _(text),
                               check=False)

    if preferences.PREFS.get(const.TEXT_ALLIGN):
        shortcut = preferences.KEYS.get(const.TEXT_ALLIGN_FLUSH_LEFT)
        text = u"Align text left ({})".format(utility.key_to_text(shortcut))
        b1 = self.create_button(const.TEXT_ALLIGN_FLUSH_LEFT,
                                self.justifyLeft,
                                shortcut,
                                _(text),
                                check=False)

        shortcut = preferences.KEYS.get(const.TEXT_ALLIGN_CENTERED)
        text = u"Align text center ({})".format(utility.key_to_text(shortcut))
        b2 = self.create_button(const.TEXT_ALLIGN_CENTERED,
                                self.justifyCenter,
                                shortcut,
                                _(text),
                                check=False)

        shortcut = preferences.KEYS.get(const.TEXT_ALLIGN_FLUSH_RIGHT)
        text = u"Align text right ({})".format(utility.key_to_text(shortcut))
        b3 = self.create_button(const.TEXT_ALLIGN_FLUSH_RIGHT,
                                self.justifyRight,
                                shortcut,
                                _(text),
                                check=False)

        shortcut = preferences.KEYS.get(const.TEXT_ALLIGN_JUSTIFIED)
        text = u"Justify text ({})".format(utility.key_to_text(shortcut))
        b4 = self.create_button(const.TEXT_ALLIGN_JUSTIFIED,
                                self.justifyFull,
                                shortcut,
                                _(text),
                                check=False)

    if preferences.PREFS.get(const.HEADING):
        shortcut = preferences.KEYS.get(const.HEADING)
        text = u"Insert heading ({})".format(utility.key_to_text(shortcut))
        b = self.create_button(const.HEADING,
                               self.toggleHeading,
                               shortcut,
                               _(text),
                               check=False)

    if preferences.PREFS.get(const.ABBREVIATION):
        shortcut = preferences.KEYS.get(const.ABBREVIATION)
        text = u"Insert abbreviation ({})".format(utility.key_to_text(shortcut))
        b = self.create_button(const.ABBREVIATION,
                               self.toggleAbbreviation,
                               shortcut,
                               _(text),
                               check=False)

    if preferences.PREFS.get(const.MARKDOWN):
        shortcut = preferences.KEYS.get(const.MARKDOWN)
        text = u"Toggle Markdown ({})".format(utility.key_to_text(shortcut))
        b = self.create_button(const.MARKDOWN,
                               self.toggleMarkdown,
                               shortcut,
                               _(text),
                               check=False)

    if button_placement_pref != "adjacent":
        self.supp_buttons_hbox.insertStretch(0, 1)
        if not isMac:
            self.supp_buttons_hbox.setMargin(6)
            self.supp_buttons_hbox.setSpacing(0)
        else:
            self.supp_buttons_hbox.setMargin(0)
            self.supp_buttons_hbox.setSpacing(14)

        if button_placement_pref == "below":
            self.outerLayout.insertLayout(1, self.supp_buttons_hbox)
        elif button_placement_pref == "above":
            self.outerLayout.insertLayout(0, self.supp_buttons_hbox)


def wrap_in_tags(self, tag, class_name=None):
    """
    Wrap selected text in a tag, optionally giving it a class.
    """
    selection = self.web.selectedText()

    if not selection:
        return

    selection = utility.escape_html_chars(selection)

    tag_string_begin = ("<{0} class='{1}'>".format(tag, class_name) if
                        class_name else "<{0}>".format(tag))
    tag_string_end = "</{0}>".format(tag)

    html = self.note.fields[self.currentField]

    if "<li><br /></li>" in html:
        # an empty list means trouble, because somehow Anki will also make the
        # line in which we want to put a <code> tag a list if we continue
        replacement = tag_string_begin + selection + tag_string_end
        self.web.eval("document.execCommand('insertHTML', false, %s);"
                      % json.dumps(replacement))

        self.web.setFocus()
        self.web.eval("focusField(%d);" % self.currentField)
        self.saveNow()

        html_after = self.note.fields[self.currentField]

        if html_after != html:
            # you're in luck!
            return
        else:
            # nothing happened :( this is a quirk that has to do with <code> tags following <div> tags
            return

    # Due to a bug in Anki or BeautifulSoup, we cannot use a simple
    # wrap operation like with <a>. So this is a very hackish way of making
    # sure that a <code> tag may precede or follow a <div> and that the tag
    # won't eat the character immediately preceding or following it
    pattern = "@%*!"
    len_p = len(pattern)

    # first, wrap the selection up in a pattern that the user is unlikely
    # to use in its own cards
    self.web.eval("wrap('{0}', '{1}')".format(pattern, pattern[::-1]))

    # focus the field, so that changes are saved
    # this causes the cursor to go to the end of the field
    self.web.setFocus()
    self.web.eval("focusField(%d);" % self.currentField)

    self.saveNow()

    html = self.note.fields[self.currentField]

    begin = html.find(pattern)
    end = html.find(pattern[::-1], begin)

    html = (html[:begin] + tag_string_begin + selection + tag_string_end +
            html[end+len_p:])

    # delete the current HTML and replace it by our new & improved one
    self.note.fields[self.currentField] = html

    # reload the note: this is needed on OS X, because it will otherwise
    # falsely show that the formatting of the element at the start of
    # the HTML has spread across the entire note
    self.loadNote()

    # focus the field, so that changes are saved
    self.web.setFocus()
    self.web.eval("focusField(%d);" % self.currentField)
    self.saveNow()
    self.web.setFocus()
    self.web.eval("focusField(%d);" % self.currentField)


def unlink(self):
    self.web.eval("setFormat('unlink')")


def toggleUnorderedList(self):
    self.web.eval("""
        document.execCommand('insertUnorderedList');
        var ulElem = window.getSelection().focusNode.parentNode;
        if (ulElem !== null) {
            var setAttrs = true;
            while (ulElem.toString() !== "[object HTMLUListElement]") {
                ulElem = ulElem.parentNode;
                if (ulElem === null) {
                    setAttrs = false;
                    break;
                }
            }
            if (setAttrs) {
                ulElem.style.marginLeft = "20px";
            }
        }
    """)


def toggleOrderedList(self):
    if preferences.PREFS.get("fixed_ol_type"):
        OrderedList(self, self.parentWindow, True)
    else:
        OrderedList(self, self.parentWindow)


def toggleStrikeThrough(self):
    self.web.eval("setFormat('strikeThrough')")


def togglePre(self):
    self.web.eval("setFormat('formatBlock', 'pre')")


def toggleHorizontalLine(self):
    self.web.eval("setFormat('insertHorizontalRule')")


def toggleIndent(self):
    self.web.eval("setFormat('indent')")


def toggleOutdent(self):
    self.web.eval("setFormat('outdent')")


def toggleDefList(self):
    selection = self.web.selectedText()
    DefList(self, self.parentWindow, selection if selection else None)


def toggleTable(self):
    selection = self.web.selectedText()
    Table(self, self.parentWindow, selection if selection else None)


def setup_background_button(self, but):
    self.background_frame = QtGui.QFrame()
    self.background_frame.setAutoFillBackground(True)
    self.background_frame.setFocusPolicy(QtCore.Qt.NoFocus)
    self.bg_color = preferences.PREFS.get("last_bg_color", "#00f")
    self.on_bg_color_changed()
    hbox = QtGui.QHBoxLayout()
    hbox.addWidget(self.background_frame)
    hbox.setMargin(5)
    but.setLayout(hbox)


# use last background color
def on_background(self):
    self._wrap_with_bg_color(self.bg_color)


# choose new color
def on_change_col(self):
    new = QtGui.QColorDialog.getColor(QtGui.QColor(self.bg_color), None)
    # native dialog doesn't refocus us for some reason
    self.parentWindow.activateWindow()
    if new.isValid():
        self.bg_color = new.name()
        self.on_bg_color_changed()
        self._wrap_with_bg_color(self.bg_color)


def _update_background_button(self):
    self.background_frame.setPalette(QtGui.QPalette(QtGui.QColor(self.bg_color)))


def on_bg_color_changed(self):
    self._update_background_button()
    preferences.PREFS["last_bg_color"] = self.bg_color
    PrefHelper.save_prefs(preferences.PREFS)


def _wrap_with_bg_color(self, color):
    """Wrap the selected text in an appropriate tag with a background color."""
    # On Linux, the standard 'hiliteColor' method works. On Windows and OSX
    # the formatting seems to get filtered out by Anki itself

    self.web.eval("""
        if (!setFormat('hiliteColor', '%s')) {
            setFormat('backcolor', '%s');
        }
        """ % (color, color))

    if isWin or isMac:
        # remove all Apple style classes thus enabling
        # text highlighting for other platforms besides Linux
        self.web.eval("""
        var matches = document.querySelectorAll(".Apple-style-span");
        for (var i = 0; i < matches.length; i++) {
            matches[i].removeAttribute("class");
        }
        """)


def power_remove_format(self):
    """Remove formatting from selected text."""
    # For Windows and OS X we need to override the standard removeFormat
    # method, because it currently doesn't work as it should in (Anki 2.0.31).
    # Specifically, the background-color <span> gives trouble. This method
    # should work fine in all but a few rare cases that are easily avoided,
    # such as a <pre> at the beginning of the HTML.

    selection = self.web.selectedText()

    # normal removeFormat method
    self.web.eval("setFormat('removeFormat');")

    self.web.eval("setFormat('selectAll')")
    complete_sel = self.web.selectedText()

    # if we have selected the complete card, we can remove more thoroughly
    if selection == complete_sel:
        self.remove_garbage()

    # deselect all text
    self.web.eval("window.getSelection().removeAllRanges();")

    # on Linux just refocus the field
    if not isWin and not isMac:
        # refocus on the field we're editing
        self.web.eval("focusField(%d);" % self.currentField)
        return

    # reload the note: this is needed on OS X and possibly Windows to
    # display in the editor that the markup is indeed gone
    self.loadNote()

    self.saveNow()
    self.web.setFocus()
    self.web.eval("focusField(%d);" % self.currentField)


def remove_garbage(self):
    """
    Remove HTML that doesn't get deleted automatically.
    """
    self.saveNow()
    self.web.setFocus()
    self.web.eval("focusField(%d);" % self.currentField)

    html = self.note.fields[self.currentField]
    soup = BeautifulSoup.BeautifulSoup(html)

    for tag in const.HEADING_TAGS + const.HTML_TAGS:
        for match in soup.findAll(tag):
            match.replaceWithChildren()

    self.note.fields[self.currentField] = unicode(soup)
    self.loadNote()


def toggleBlockquote(self):
    selected = self.web.selectedHtml()
    Blockquote(self, selected)


def justifyCenter(self):
    self.web.eval("setFormat('justifyCenter');")


def justifyLeft(self):
    self.web.eval("setFormat('justifyLeft');")


def justifyRight(self):
    self.web.eval("setFormat('justifyRight');")


def justifyFull(self):
    self.web.eval("setFormat('justifyFull');")


def toggleHeading(self):
    selected = self.web.selectedText()
    Heading(self, self.parentWindow, selected)


def toggleAbbreviation(self):
    selected = self.web.selectedText()
    Abbreviation(self, self.parentWindow, selected)


def toggleHyperlink(self):
    selected = self.web.selectedText()
    Hyperlink(self, self.parentWindow, selected)


def toggleMarkdown(self):
    self.saveNow()
    current_field = self.currentField
    html_field = self.note.fields[current_field]
    if not html_field:
        html_field = u""
    markdowner = Markdowner(self, self.parentWindow, self.note, html_field, current_field)
    markdowner.start()
    # self.saveNow()
    self.web.setFocus()
    self.web.eval("focusField(%d);" % self.currentField)


def on_focus_gained(self, note, current_field_no):
    """
    Check if the current field contains Markdown. Change the appearance of
    the field if it does, or do nothing if not.
    """

    if not note.fields[current_field_no]:
        return

    Markdowner.manage_style(self, current_field_no)
    self.web.eval("""
    var field = $('#f%s');
    if (field.html().indexOf('SBAdata:') > -1) {
        var mdData = /<!----SBAdata:([a-zA-Z0-9+/]+=*)---->/.exec(field.html());
        var json = JSON.parse(atob(mdData[1]));
        if (json.isconverted) {
            if (!field.hasClass('mdstyle')) {
                field.addClass('mdstyle');
            }
            if (!$('#f%s + [class^=mdwarning]').length) {
                field.after($('<div/>', {class: 'mdwarning', text: '%s'}));
            }
            field.attr('title', '%s');
        }
    }
    """ % (current_field_no, current_field_no, markdown_warning_text, markdown_warning_text))


def init_hook(self, mw, widget, parentWindow, addMode=False):
    addHook("editFocusGained", self.on_focus_gained)

Preferences.init()

if preferences.PREFS.get(const.MARKDOWN):
    editor.Editor.on_focus_gained = on_focus_gained
    editor.Editor.__init__ = wrap(editor.Editor.__init__, init_hook)

markdown_warning_text = preferences.CONFIG.get(const.CONFIG_TOOLTIPS, "md_warning_editing_tooltip")

editor.Editor.create_button = create_button
editor.Editor.toggleMarkdown = toggleMarkdown
editor.Editor.toggleHeading = toggleHeading
editor.Editor.toggleAbbreviation = toggleAbbreviation
editor.Editor.toggleHyperlink = toggleHyperlink
editor.Editor.remove_garbage = remove_garbage
editor.Editor.unlink = unlink
editor.Editor.justifyFull = justifyFull
editor.Editor.justifyRight = justifyRight
editor.Editor.justifyLeft = justifyLeft
editor.Editor.justifyCenter = justifyCenter
editor.Editor.toggleBlockquote = toggleBlockquote
editor.Editor.removeFormat = power_remove_format
editor.Editor.on_background = on_background
editor.Editor.setup_background_button = setup_background_button
editor.Editor.on_bg_color_changed = on_bg_color_changed
editor.Editor._update_background_button = _update_background_button
editor.Editor.on_change_col = on_change_col
editor.Editor._wrap_with_bg_color = _wrap_with_bg_color
editor.Editor.wrap_in_tags = wrap_in_tags
editor.Editor.toggleOrderedList = toggleOrderedList
editor.Editor.toggleUnorderedList = toggleUnorderedList
editor.Editor.toggleStrikeThrough = toggleStrikeThrough
editor.Editor.togglePre = togglePre
editor.Editor.toggleHorizontalLine = toggleHorizontalLine
editor.Editor.toggleIndent = toggleIndent
editor.Editor.toggleOutdent = toggleOutdent
editor.Editor.toggleDefList = toggleDefList
editor.Editor.toggleTable = toggleTable
editor.Editor.setupButtons = wrap(editor.Editor.setupButtons, setup_buttons)

mw.ExtraButtons_Options = Options(mw)
mw.ExtraButtons_Options.setup_power_format_pack_options()
