# -*- coding: utf-8 -*-

# AwesomeTTS text-to-speech add-on for Anki
# Copyright (C) 2010-Present  Anki AwesomeTTS Development Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Path and directory initialization
"""

import os
import sys
import tempfile

__all__ = [
    'ADDON',
    'ADDON_IS_LINKED',
    'CACHE',
    'CONFIG',
    'LOG',
    'TEMP',
    'CUSTOME_CONFIG',
]


# n.b. When determining the code directory, abspath() is needed since
# the __file__ constant is not a full path by itself.

ADDON = os.path.dirname(os.path.abspath(__file__)) \
    .decode(sys.getfilesystemencoding())  # sqlite (and others?) needs unicode

ADDON_IS_LINKED = os.path.islink(ADDON)

BLANK = os.path.join(ADDON, 'blank.mp3')

CACHE = os.path.join(ADDON, '.cache')
if not os.path.isdir(CACHE):
    os.mkdir(CACHE)

CONFIG = os.path.join(ADDON, 'config.db')

LOG = os.path.join(ADDON, 'addon.log')

CUSTOME_CONFIG = os.path.join(ADDON, '_custom_config.json')

TEMP = tempfile.gettempdir()
