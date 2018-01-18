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

from prefhelper import PrefHelper


class Preferences(object):
    """
    Class to hold the preferences for the running program.
    """

    @staticmethod
    def init():
        global PREFS
        global KEYS
        global CONFIG
        PREFS = PrefHelper.get_preferences()
        KEYS = PrefHelper.get_keybindings()
        CONFIG = PrefHelper.get_config()
