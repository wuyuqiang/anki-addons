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

import HTMLParser
import re
import string
import sys

# Constants
##################################################

OPERATING_SYSTEMS = {
    "linux2": "Linux",
    "win32" : "Windows",
    "cygwin": "Windows",
    "darwin": "Mac OS X"
}
PLATFORM = sys.platform

# size of the dialog windows
DIALOG_SIZE_X         = 350
DIALOG_SIZE_Y         = 200
MIN_COMBOBOX_WIDTH    = 140

HTML_TAGS = ("b", "i", "u", "span", "font", "sup", "sub",
             "dl", "dt", "dd", "code", "s", "pre", "kbd",
             "a", "strike", "blockquote", "abbr")

HEADING_TAGS = ("h1", "h2", "h3", "h4", "h5", "h6")

# buttons placement positions
PLACEMENT_POSITIONS   = ("adjacent", "below", "above")
BUTTONS               = list()

CODE_AND_PRE_CLASS = "myCodeClass"

# names of the buttons used for the keybindings
CODE                          = "code"
UNORDERED_LIST                = "unordered_list"
ORDERED_LIST                  = "ordered_list"
STRIKETHROUGH                 = "strikethrough"
PRE                           = "pre"
HORIZONTAL_RULE               = "horizontal_rule"
INDENT                        = "indent"
OUTDENT                       = "outdent"
DEFINITION_LIST               = "definition_list"
TABLE                         = "table"
KEYBOARD                      = "keyboard"
HYPERLINK                     = "hyperlink"
REMOVE_HYPERLINK              = "remove_hyperlink"
BACKGROUND_COLOR              = "background_color"
BACKGROUND_COLOR_CHANGE       = "background_color_change"
BLOCKQUOTE                    = "blockquote"
TEXT_ALLIGN                   = "text_align"
TEXT_ALLIGN_FLUSH_LEFT        = "text_align_flush_left"
TEXT_ALLIGN_FLUSH_RIGHT       = "text_align_flush_right"
TEXT_ALLIGN_JUSTIFIED         = "text_align_justified"
TEXT_ALLIGN_CENTERED          = "text_align_centered"
HEADING                       = "heading"
ABBREVIATION                  = "abbreviation"
MARKDOWN                      = "markdown"
CODE_CLASS                    = "code_class"
LAST_BG_COLOR                 = "last_bg_color"
FIXED_OL_TYPE                 = "fixed_ol_type"
MARKDOWN_SYNTAX_STYLE         = "markdown_syntax_style"
MARKDOWN_LINE_NUMS            = "markdown_line_nums"
MARKDOWN_CODE_DIRECTION       = "markdown_code_direction"
MARKDOWN_ALWAYS_REVERT        = "markdown_always_revert"
MARKDOWN_OVERRIDE_EDITING     = "markdown_override_editing"
MARKDOWN_CLASSFUL_PYGMENTS    = "markdown_classful_pygments"
BUTTON_PLACEMENT              = "button_placement"
STYLE_TABLE                   = "style_table"

# constants for key sequence
KEY_MODIFIERS                 = ("ctrl", "alt", "shift")
KEY_MODIFIERS_MACOSX          = ("meta",)
KEYS_SEQUENCE                 = tuple(string.ascii_lowercase) + \
                                      tuple(string.punctuation) + \
                                      tuple(string.digits)
FUNCTION_KEYS                 = ("f1", "f2", "f3", "f4", "f5", "f6",
                                       "f7", "f8", "f9", "f10", "f11", "f12")

# markers to be wrapped around Markdown data in fields
START_HTML_MARKER             = "<!----SBAdata:"
END_HTML_MARKER               = "---->"

# change field to this background color
MARKDOWN_BG_COLOR             = "#FFEDD3"

# max number of bytes read from preference file
MAX_BYTES_PREFS               = 32768

# check if image present in Markdown
IS_LINK_OR_IMG_REGEX = re.compile(r"!\[[^\]]*\](\(.*?(?<!\\)\))")
# to unescape image data
HTML_PARSER                   = HTMLParser.HTMLParser()

# config file
CONFIG_DEFAULT                = "DEFAULT"
CONFIG_FILENAME               = "config.ini"
CONFIG_LABELS                 = "Labels"
CONFIG_TOOLTIPS               = "ToolTips"
CONFIG_WINDOW_TITLES          = "WindowTitles"
CONFIG_MENU_NAMES             = "MenuNames"
CONFIG_ABOUT                  = "About"
CONFIG_DIALOG_SIZES           = "DialogSizes"
CONFIG_KEYBINDINGS            = "Keybindings"
CONFIG_WARNINGS               = "Warnings"
CONFIG_QT                     = "Qt"
CONFIG_FORMAT_SETTINGS        = "FormatSettings"
CONFIG_FILENAMES              = "Filenames"

# stylesheet for QGroupBox
QGROUPBOX_STYLE = """
QGroupBox { border: 1px solid lightgrey;
                    border-radius: 5px;
                    margin-top: 10px;
                    font-weight: bold; }
QGroupBox::title {  subcontrol-origin: margin;
                    subcontrol-position: top;
                    padding:0 3px 0 3px; }
"""

HBOX                          = "hbox"
VBOX                          = "vbox"
WIDGET                        = "widget"
LAYOUT                        = "layout"

# Markdown code directions
LEFT                          = "left"
CENTER                        = "center"
RIGHT                         = "right"
CODE_DIRECTIONS               = (LEFT, CENTER, RIGHT)
