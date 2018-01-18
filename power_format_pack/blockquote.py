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


class Blockquote(object):

    def __init__(self, other, selected_html):
        self.editor_instance    = other
        self.selected_html      = selected_html
        if not self.selected_html:
            return
        self.insert_blockquote()

    def insert_blockquote(self):
        author = None
        start_delim = "[["
        end_delim = "]]"
        len_delim = len(start_delim)
        start = self.selected_html.find(start_delim)
        end = self.selected_html.find(end_delim, start + 1)
        if start > -1 and end > -1:
            author = self.selected_html[(start+len_delim):end]
            self.editor_instance.web.eval("""
                document.execCommand('formatBlock', false, 'blockquote');
                var bq = window.getSelection().focusNode.parentNode;
                if (bq.toString() !== "[object HTMLQuoteElement]"
                    && bq.toString() !== "[object HTMLBlockquoteElement]") {
                    bq = bq.parentNode;
                }
                bq.setAttribute("cite", "%s");
                bq.innerText = bq.innerText.replace(/ ?\[\[.+?\]\]/g, "");
                var authorParagraph = document.createElement("p");
                authorParagraph.style.fontStyle = "italic";
                authorParagraph.innerHTML = "%s"
                bq.appendChild(authorParagraph);
            """ % (author, author))
        else:
            self.editor_instance.web.eval("setFormat('formatBlock', 'blockquote');")

