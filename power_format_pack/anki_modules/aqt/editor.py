# -*- coding: utf-8 -*-
# Copyright: Damien Elmes <anki@ichi2.net>
# Changes: Stefan van den Akker <neftas@protonmail.com>

from aqt.qt import *
from aqt.utils import openHelp
from aqt.utils import shortcut

import aqt
from BeautifulSoup import BeautifulSoup
from power_format_pack import const
from power_format_pack import preferences
from power_format_pack.prefhelper import PrefHelper


def onHtmlEdit(self):
    self.saveNow()
    d = QDialog(self.widget)
    form = aqt.forms.edithtml.Ui_Dialog()
    form.setupUi(d)
    d.connect(form.buttonBox, SIGNAL("helpRequested()"),
              lambda: openHelp("editor"))
    orgHTML = self.note.fields[self.currentField]
    HTMLWithoutData = orgHTML
    start_md_data = orgHTML.find(const.START_HTML_MARKER)
    end_md_data = orgHTML.find(const.END_HTML_MARKER, start_md_data)
    containsData = start_md_data != -1 and end_md_data != -1
    if containsData:
        mdData = orgHTML[start_md_data:(end_md_data+len(const.END_HTML_MARKER))]
        HTMLWithoutData = orgHTML[:start_md_data]
    form.textEdit.setPlainText(HTMLWithoutData)
    form.textEdit.moveCursor(QTextCursor.End)
    d.exec_()
    html = form.textEdit.toPlainText()
    if containsData:
        html += mdData
    # filter html through beautifulsoup so we can strip out things like a
    # leading </div>
    html = unicode(BeautifulSoup(html))
    self.note.fields[self.currentField] = html
    self.loadNote()
    # focus field so it's saved
    self.web.setFocus()
    self.web.eval("focusField(%d);" % self.currentField)


def create_button(self, name, func, key=None, tip=None, size=True, text="",
                  check=False, native=False, canDisable=True):

    button = QPushButton(text)

    if check:
        button.clicked[bool].connect(func)
    else:
        button.clicked.connect(func)

    if size:
        button.setFixedHeight(20)
        button.setFixedWidth(20)

    if not native:
        if self.plastiqueStyle:
            button.setStyle(self.plastiqueStyle)
        button.setFocusPolicy(Qt.NoFocus)
    else:
        button.setAutoDefault(False)

    if key:
        button.setShortcut(key)

    if tip:
        button.setToolTip(shortcut(tip))

    if check:
        button.setCheckable(True)

    if canDisable:
        self._buttons[name] = button

    PrefHelper.set_icon(button, name)

    const.BUTTONS.append(button)

    button_placement_pref = preferences.PREFS.get(const.BUTTON_PLACEMENT)

    if button_placement_pref == "adjacent":
        self.iconsBox.addWidget(button)
    else:
        self.supp_buttons_hbox.addWidget(button)

    return button


def _filterHTML(self, html, localize=False):
    doc = BeautifulSoup(html)
    # remove implicit regular font style from outermost element
    if doc.span and doc.span.parent.name != u"th":
        try:
            attrs = doc.span['style'].split(";")
        except (KeyError, TypeError):
            attrs = []
        if attrs:
            new = []
            for attr in attrs:
                sattr = attr.strip()
                if sattr and sattr not in ("font-style: normal", "font-weight: normal"):
                    new.append(sattr)
            doc.span['style'] = ";".join(new)
        # filter out implicit formatting from webkit
    for tag in doc("span", "Apple-style-span"):
        preserve = ""
        for item in tag['style'].split(";"):
            try:
                k, v = item.split(":")
            except ValueError:
                continue
            if k.strip() == "color" and not v.strip() == "rgb(0, 0, 0)":
                preserve += "color:%s;" % v
            if k.strip() in ("font-weight", "font-style"):
                preserve += item + ";"
        if preserve:
            # preserve colour attribute, delete implicit class
            tag['style'] = preserve
            del tag['class']
        else:
            # strip completely
            tag.replaceWithChildren()
    for tag in doc("font", "Apple-style-span"):
        # strip all but colour attr from implicit font tags
        if 'color' in dict(tag.attrs):
            for attr in tag.attrs:
                if attr != "color":
                    del tag[attr]
                # and apple class
            del tag['class']
        else:
            # remove completely
            tag.replaceWithChildren()
        # now images
    for tag in doc("img"):
        # turn file:/// links into relative ones
        try:
            if tag['src'].lower().startswith("file://"):
                tag['src'] = os.path.basename(tag['src'])
            if localize and self.isURL(tag['src']):
                # convert remote image links to local ones
                fname = self.urlToFile(tag['src'])
                if fname:
                    tag['src'] = fname
        except KeyError:
            # for some bizarre reason, mnemosyne removes src elements
            # from missing media
            pass
            # strip all other attributes, including implicit max-width
        for attr, val in tag.attrs:
            if attr != "src":
                del tag[attr]
        # strip superfluous elements
    for elem in "html", "head", "body", "meta":
        for tag in doc(elem):
            tag.replaceWithChildren()
    html = unicode(doc)
    return html
