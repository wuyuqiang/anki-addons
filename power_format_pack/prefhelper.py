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


import codecs
import copy
import os
import pickle

from PyQt4 import QtGui

from anki.utils import json, isMac
from aqt import mw as main_window
from power_format_pack import const
from power_format_pack.python_modules import ConfigParser


class PrefHelper(object):
    """
    Static methods related to preference handling.
    """

    CONFIG = None

    @staticmethod
    def get_preference_path():
        c = PrefHelper.get_config()
        return os.path.join(PrefHelper.get_addons_folder(),
                            c.get(const.CONFIG_DEFAULT, "FOLDER_NAME"),
                            c.get(const.CONFIG_FILENAMES, "PREFERENCES_FILENAME"))

    @staticmethod
    def get_keybindings_path():
        c = PrefHelper.get_config()
        if isMac:
            filename = c.get(const.CONFIG_FILENAMES, "KEYBINDINGS_MACOSX")
        else:
            filename = c.get(const.CONFIG_FILENAMES, "KEYBINDINGS_LINUX_WINDOWS")

        return os.path.join(PrefHelper.get_addons_folder(),
                            c.get(const.CONFIG_DEFAULT, "FOLDER_NAME"),
                            filename)

    @staticmethod
    def normalize_user_prefs(default_prefs, user_prefs):
        """
        Check if the user preferences are compatible with the currently used
        preferences within the addon. Add keys if they don't exist, and remove
        those that are not recognized. Return a dictionary with the checked
        preferences.
        >>> default_prefs   = dict(b="two")
        >>> user_prefs      = dict(a="one")
        >>> normalize_user_prefs(default_prefs, user_prefs)
        {u'b': u'two'}
        """

        result_dict = user_prefs
        # add items that are not in prefs, but should be (e.g. after update)
        for key, value in default_prefs.iteritems():
            user_val = user_prefs.get(key)
            if user_val is None:
                result_dict[key] = value
        # delete items in prefs that should not be there (e.g. after update)
        for key in user_prefs.keys()[:]:
            if default_prefs.get(key) is None:
                del result_dict[key]

        return result_dict

    @staticmethod
    def get_default_preferences():
        # the default preferences that are used when no custom preferences
        # are found, or when the user preferences are corrupted
        _default_conf = {
                const.CODE_CLASS:                   const.CODE_AND_PRE_CLASS,
                const.LAST_BG_COLOR:                "#00f",
                const.FIXED_OL_TYPE:                "",
                const.MARKDOWN_SYNTAX_STYLE:        "tango",
                const.MARKDOWN_CODE_DIRECTION:      "left",
                const.MARKDOWN_LINE_NUMS:           False,
                const.MARKDOWN_ALWAYS_REVERT:       False,
                const.MARKDOWN_OVERRIDE_EDITING:    True,
                const.MARKDOWN_CLASSFUL_PYGMENTS:   False,
                const.BUTTON_PLACEMENT:             "adjacent",
                const.CODE:                         True,
                const.UNORDERED_LIST:               True,
                const.ORDERED_LIST:                 True,
                const.STRIKETHROUGH:                True,
                const.PRE:                          True,
                const.HORIZONTAL_RULE:              True,
                const.INDENT:                       True,
                const.OUTDENT:                      True,
                const.DEFINITION_LIST:              True,
                const.TABLE:                        True,
                const.STYLE_TABLE:                  True,
                const.KEYBOARD:                     True,
                const.HYPERLINK:                    True,
                const.BACKGROUND_COLOR:             True,
                const.BLOCKQUOTE:                   True,
                const.TEXT_ALLIGN:                  True,
                const.HEADING:                      True,
                const.ABBREVIATION:                 True,
                const.MARKDOWN:                     False
        }

        return _default_conf

    @staticmethod
    def get_default_keybindings():
        # the default keybindings that are used when no custom keybindings
        # are found, or when the user keybindings are corrupted
        _default_keybindings_linux_windows = {
                const.CODE:                         QtGui.QKeySequence(u"ctrl+,"),
                const.UNORDERED_LIST:               QtGui.QKeySequence(u"ctrl+["),
                const.ORDERED_LIST:                 QtGui.QKeySequence(u"ctrl+]"),
                const.STRIKETHROUGH:                QtGui.QKeySequence(u"alt+shift+5"),
                const.PRE:                          QtGui.QKeySequence(u"ctrl+."),
                const.HORIZONTAL_RULE:              QtGui.QKeySequence(u"ctrl+shift+alt+_"),
                const.INDENT:                       QtGui.QKeySequence(u"ctrl+shift+]"),
                const.OUTDENT:                      QtGui.QKeySequence(u"ctrl+shift+["),
                const.DEFINITION_LIST:              QtGui.QKeySequence(u"ctrl+shift+d"),
                const.TABLE:                        QtGui.QKeySequence(u"ctrl+shift+3"),
                const.KEYBOARD:                     QtGui.QKeySequence(u"ctrl+shift+k"),
                const.HYPERLINK:                    QtGui.QKeySequence(u"ctrl+shift+h"),
                const.REMOVE_HYPERLINK:             QtGui.QKeySequence(u"ctrl+shift+alt+h"),
                const.BACKGROUND_COLOR:             QtGui.QKeySequence(u"ctrl+shift+b"),
                const.BACKGROUND_COLOR_CHANGE:      QtGui.QKeySequence(u"ctrl+shift+n"),
                const.BLOCKQUOTE:                   QtGui.QKeySequence(u"ctrl+shift+y"),
                const.TEXT_ALLIGN_FLUSH_LEFT:       QtGui.QKeySequence(u"ctrl+shift+alt+l"),
                const.TEXT_ALLIGN_FLUSH_RIGHT:      QtGui.QKeySequence(u"ctrl+shift+alt+r"),
                const.TEXT_ALLIGN_JUSTIFIED:        QtGui.QKeySequence(u"ctrl+shift+alt+s"),
                const.TEXT_ALLIGN_CENTERED:         QtGui.QKeySequence(u"ctrl+shift+alt+b"),
                const.HEADING:                      QtGui.QKeySequence(u"ctrl+alt+1"),
                const.ABBREVIATION:                 QtGui.QKeySequence(u"shift+alt+a"),
                const.MARKDOWN:                     QtGui.QKeySequence(u"ctrl+shift+0")
        }
        # Mac OS keybindings are the same as Linux/Windows bindings,
        # except for the following
        _default_keybindings_macosx = \
            copy.deepcopy(_default_keybindings_linux_windows)
        _default_keybindings_macosx[const.CODE] = QtGui.QKeySequence(u"ctrl+shift+,")
        _default_keybindings_macosx[const.PRE] = QtGui.QKeySequence(u"ctrl+shift+.")

        if isMac:
            return _default_keybindings_macosx
        else:
            return _default_keybindings_linux_windows

    @staticmethod
    def get_addons_folder():
        """
        Return the addon folder used by Anki.
        """
        return main_window.pm.addonFolder()

    @staticmethod
    def save_prefs(prefs):
        """
        Save the preferences to disk.
        """
        with codecs.open(PrefHelper.get_preference_path(), "w", encoding="utf8") as f:
            json.dump(prefs, f, indent=4, sort_keys=True)

    @staticmethod
    def get_preferences():
        """
        Load the current preferences from disk. If no preferences file is
        found, or if it is corrupted, return the default preferences.
        """
        prefs = None
        try:
            with codecs.open(PrefHelper.get_preference_path(), encoding="utf8") as f:
                prefs = json.load(f)
        except:
            prefs = PrefHelper.get_default_preferences()
        else:
            prefs = PrefHelper.normalize_user_prefs(
                        PrefHelper.get_default_preferences(), prefs)

        return prefs

    @staticmethod
    def are_dicts_different(one, other):
        """
        Return `True` if `one` and `other` contain different values for the
        same key, `False` if all values for the same keys are equal.
        """
        for k, v in one.iteritems():
            if one.get(k) != other.get(k):
                return True
        return False

    @staticmethod
    def save_keybindings(keybindings):
        """
        Pickle the provided keybindings into a binary file. `keybindings` should
        be a hashmap containing Unicode strings as key and `QtGui.QKeySequence`s
        as value.
        """
        with codecs.open(PrefHelper.get_keybindings_path(), mode="wb") as f:
            pickle.dump(keybindings, f)

    @staticmethod
    def get_keybindings():
        """
        Unpickle keybindings from a binary file. Return a hashmap that contains keys
        of type Unicode string and values of type `QtGui.QKeySequence`.
        """
        keybindings = None
        try:
            with codecs.open(PrefHelper.get_keybindings_path(), mode="rb") as f:
                keybindings = pickle.load(f)
        except IOError:
            return PrefHelper.get_default_keybindings()
        else:
            default_keybindings = PrefHelper.get_default_keybindings()
            return PrefHelper.normalize_user_prefs(default_keybindings, keybindings)

    @staticmethod
    def set_icon(button, name):
        """
        Define the path for the icon the corresponding button should have.
        """
        c = PrefHelper.get_config()
        icon_path = os.path.join(PrefHelper.get_addons_folder(),
                                 c.get(const.CONFIG_DEFAULT, "FOLDER_NAME"),
                                 "icons",
                                 "{}.png".format(name))
        button.setIcon(QtGui.QIcon(icon_path))

    @staticmethod
    def get_config():
        """
        Return a RawConfigParser for the specified path.
        """
        if PrefHelper.CONFIG is not None:
            return PrefHelper.CONFIG

        path = os.path.join(PrefHelper.get_addons_folder(),
                            "power_format_pack",
                            "config.ini")
        config_parser = ConfigParser.ConfigParser()
        successfully_read_files = config_parser.read(path)
        if not successfully_read_files:
            raise Exception("Could not read config file {!r}".format(path))

        PrefHelper.CONFIG = config_parser

        return config_parser
