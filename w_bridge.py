from PyQt4.QtCore import QUrl, QObject
from PyQt4.QtGui import QDesktopServices
from aqt.qt import *
import aqt
from webview import AnkiWebView
from anki.hooks import addHook, wrap


def new_bridge(s):
    print "new:",s
    return s


aqt.mw.web.setBridge(new_bridge)

# new_loadFinished()