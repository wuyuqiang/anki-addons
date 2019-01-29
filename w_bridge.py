from PyQt4.QtCore import QUrl, QObject, QMimeData
from PyQt4.QtGui import QDesktopServices
import aqt

import Log

from aqt.reviewer import Reviewer
from anki.hooks import wrap, addHook
from aqt.editor import Editor, EditorWebView
from aqt.webview import AnkiWebView


LOG = Log.getLogger(__name__)


def launchHttpProxy():
    import urllib2

    opener = urllib2.build_opener(
                    urllib2.HTTPHandler(),
                    urllib2.HTTPSHandler(),
                    urllib2.ProxyHandler({'https': 'http://localhost:1087'}))
    urllib2.install_opener(opener)


launchHttpProxy()

def new_bridge(cmd):
    # LOG.debug("new_bridge cmd: %s." % cmd)
    str_result = ""
    # LOG.debug("loading....cmd: " + cmd)
    if cmd.startswith("focus"):
        LOG.debug("focus cmd start.")
        # LOG.debug(strr)
        # aqt.mw.reviewer.web.setFocus()
    elif cmd.startswith("cmp:"):
        # LOG.debug("compare cmd start.")
        cmp_str = cmd[4:]
        origin, input = cmp_str.split("|", 1)
        # LOG.debug("origin:"+origin+", input:"+input)
        str_result = aqt.mw.reviewer.correct(input, origin)
        # LOG.debug(str_result)

    return str_result


aqt.mw.web.setBridge(new_bridge)

_js="""
alert(currentField)
if (currentField) {
    // no field has been focused yet
    var ei = '<img src="__empty.jpg" alt="empty" style="display:none"/>'
    if(currentField.innerHTML == "<br>") {
        currentField.innerHTML = ei
    } else {
        currentField.innerHTML = ei + currentField.innerHTML;
    }
}
"""


def insertEmptyImage(self):
    LOG.debug("ddddd")
    self.addMedia(u"_w_placeholder.png")


def addInsertButtons(self):
    self._addButton("insert placeholder image", lambda s=self: insertEmptyImage(self), text="IPI", tip="insert placeholder image", size=True)


addHook("setupEditorButtons", addInsertButtons)


def focusWeb():
    # LOG.debug(aqt.mw.col.decks.current())
    aqt.mw.web.setFocus()


addHook("showQuestion", focusWeb)
addHook("showAnswer", focusWeb)
# Editor.setupButtons = wrap(Editor.setupButtons, ImageResizerButton, 'after')


def new_processUrls(self, mime, _old):
    urls = mime.urls()
    size = len(urls)
    if size == 1:
        return _old(self, mime)
    # LOG.debug("import %d urls" % size)
    newmime = QMimeData()
    newlink = ""
    for url in urls:
        url = url.toString()
        url = url.splitlines()[0]
        # LOG.debug("import %s" % url)
        newmime = QMimeData()
        link = self.editor.urlToLink(url)
        if link:
            newlink += link
        elif mime.hasImage():
            # if we couldn't convert the url to a link and there's an
            # image on the clipboard (such as copy&paste from
            # google images in safari), use that instead
            return self._processImage(mime)
        else:
            newmime.setText(url)
            return newmime
    if newlink != "":
        newmime.setHtml(newlink)
    return newmime


EditorWebView._processUrls = wrap(EditorWebView._processUrls, new_processUrls, 'around')


def new_dropEvent(self, evt, _old):
    mime = evt.mimeData()
    if evt.source():
        return _old(self, evt)

    urls = mime.urls()
    while mime.hasUrls() and len(urls) > 0:
        _old(self, evt)
        url = urls[0]
        LOG.debug(url.toString())
        urls.remove(url)


# EditorWebView.dropEvent = wrap(EditorWebView.dropEvent, new_dropEvent, 'around')
