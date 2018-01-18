#-*- coding:utf-8 -*-
#
# Copyright © 2016–2017 Liang Feng <finalion@gmail.com>
#
# Support: Report an issue at https://github.com/finalion/WordQuery/issues
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version; http://www.gnu.org/copyleft/gpl.html.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import re
import shutil
import sys
import time
from collections import defaultdict

from aqt import mw
from aqt.qt import QFileDialog, QObject, QThread, pyqtSignal, pyqtSlot
from aqt.utils import showInfo, showText, tooltip
from .constants import Endpoint, Template
from .context import config
from .lang import _, _sl
from .progress import ProgressManager
from .service import service_manager, QueryResult, copy_static_file
from .utils import Empty, MapDict, Queue, wrap_css


def inspect_note(note):
    '''
    inspect the note, and get necessary input parameters
    return word_ord: field index of the word in current note
    return word: the word
    return maps: dicts map of current note
    '''
    maps = config.get_maps(note.model()['id'])
    for i, m in enumerate(maps):
        if m.get('word_checked', False):
            word_ord = i
            break
    else:
        # if no field is checked to be the word field, default the
        # first one.
        word_ord = 0

    def purify_word(word):
        return word.strip() if word else ''

    word = purify_word(note.fields[word_ord])
    return word_ord, word, maps


def query_from_browser(browser):
    if not browser:
        return
    work_manager.reset_query_counts()
    notes = [browser.mw.col.getNote(note_id)
             for note_id in browser.selectedNotes()]
    if len(notes) == 0:
        return
    if len(notes) == 1:
        query_from_editor_all_fields(browser.editor)
    if len(notes) > 1:
        fields_number = 0
        progress.start(immediate=True)
        for i, note in enumerate(notes):
            # user cancels the progress
            if progress.abort():
                break
            try:
                results = query_all_flds(note)
                update_note_fields(note, results)
                fields_number += len(results)
                progress.update_labels(
                    MapDict(type='count', words_number=i + 1, fields_number=fields_number))
            except InvalidWordException:
                showInfo(_("NO_QUERY_WORD"))
        promot_choose_css()
        browser.model.reset()
        progress.finish()
        # browser.model.reset()
        # browser.endReset()
        tooltip(u'{0} {1} {2}, {3} {4}'.format(
            _('UPDATED'), i + 1, _('CARDS'), work_manager.completed_query_counts(), _('FIELDS')))


def query_from_editor_all_fields(editor):
    if not editor or not editor.note:
        return
    work_manager.reset_query_counts()
    time.sleep(0.1)
    progress.start(immediate=True)
    try:
        results = query_all_flds(editor.note)
        update_note_fields(editor.note, results)
    except InvalidWordException:
        showInfo(_("NO_QUERY_WORD"))
    progress.finish()
    promot_choose_css()
    editor.setNote(editor.note, focus=True)
    editor.saveNow()


def query_from_editor_current_field(editor):
    if not editor or not editor.note:
        return
    work_manager.reset_query_counts()
    progress.start(immediate=True)
    # if the focus falls into the word field, then query all note fields,
    # else only query the current focused field.
    fld_index = editor.currentField
    word_ord = inspect_note(editor.note)[0]
    try:
        if fld_index == word_ord:
            results = query_all_flds(editor.note)
        else:
            results = query_single_fld(editor.note, fld_index)
        update_note_fields(editor.note, results)
    except InvalidWordException:
        showInfo(_("NO_QUERY_WORD"))
    # editor.note.flush()
    # showText(str(editor.note.model()['tmpls']))
    progress.finish()
    promot_choose_css()
    editor.setNote(editor.note, focus=True)
    editor.saveNow()


def update_note_fields(note, results):
    for i, q in results.items():
        if isinstance(q, QueryResult) and i < len(note.fields):
            update_note_field(note, i, q)


def update_note_field(note, fld_index, fld_result):
    result, js, jsfile = fld_result.result, fld_result.js, fld_result.jsfile
    # js process: add to template of the note model
    add_to_tmpl(note, js=js, jsfile=jsfile)
    note.fields[fld_index] = result if result else ''
    note.flush()


def promot_choose_css():
    for local_service in service_manager.local_services:
        try:
            missed_css = local_service.missed_css.pop()
            showInfo(Template.miss_css.format(
                dict=local_service.title, css=missed_css))
            filepath = QFileDialog.getOpenFileName(
                caption=u'Choose css file', filter=u'CSS (*.css)')
            if filepath:
                shutil.copy(filepath, u'_' + missed_css)
                wrap_css(u'_' + missed_css)
                local_service.missed_css.clear()

        except KeyError as e:
            pass


def add_to_tmpl(note, **kwargs):
    # templates
    '''
    [{u'name': u'Card 1', u'qfmt': u'{{Front}}\n\n', u'did': None, u'bafmt': u'',
        u'afmt': u'{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}\n\n{{12}}\n\n{{44}}\n\n', u'ord': 0, u'bqfmt': u''}]
    '''
    # showInfo(str(kwargs))
    afmt = note.model()['tmpls'][0]['afmt']
    if kwargs:
        jsfile, js = kwargs.get('jsfile', None), kwargs.get('js', None)
        if js and js.strip():
            addings = js.strip()
            if addings not in afmt:
                if not addings.startswith(u'<script') and not addings.endswith(u'/script>'):
                    addings = u'\r\n<script>{}</script>'.format(addings)
                afmt += addings
        if jsfile:
            new_jsfile = u'_' + \
                jsfile if not jsfile.startswith(u'_') else jsfile
            copy_static_file(jsfile, new_jsfile)
            addings = u'\r\n<script src="{}"></script>'.format(new_jsfile)
            afmt += addings
        note.model()['tmpls'][0]['afmt'] = afmt


class InvalidWordException(Exception):
    """Invalid word exception"""


def join_result(query_func):
    def wrap(*args, **kwargs):
        query_func(*args, **kwargs)
        for name, worker in work_manager.workers.items():
            while not worker.isFinished():
                mw.app.processEvents()
                worker.wait(100)
        return handle_results('__query_over__')
    return wrap


@join_result
def query_all_flds(note):
    handle_results.total = defaultdict(QueryResult)
    word_ord, word, maps = inspect_note(note)
    if not word:
        raise InvalidWordException
    progress.update_title(u'Querying [[ %s ]]' % word)
    for i, each in enumerate(maps):
        if i == word_ord:
            continue
        if i == len(note.fields):
            break
        dict_name = each.get('dict', '').strip()
        dict_field = each.get('dict_field', '').strip()
        dict_unique = each.get('dict_unique', '').strip()
        if dict_name and dict_name not in _sl('NOT_DICT_FIELD') and dict_field:
            worker = work_manager.get_worker(dict_unique)
            worker.target(i, dict_field, word)
    work_manager.start_all_workers()


@join_result
def query_single_fld(note, fld_index):
    handle_results.total = defaultdict(QueryResult)
    word_ord, word, maps = inspect_note(note)
    if not word:
        raise InvalidWordException
    progress.update_title(u'Querying [[ %s ]]' % word)
    # assert fld_index > 0
    if fld_index >= len(maps):
        return QueryResult()
    dict_name = maps[fld_index].get('dict', '').strip()
    dict_field = maps[fld_index].get('dict_field', '').strip()
    dict_unique = maps[fld_index].get('dict_unique', '').strip()
    if dict_name and dict_name not in _sl('NOT_DICT_FIELD') and dict_field:
        worker = work_manager.get_worker(dict_unique)
        worker.target(fld_index, dict_field, word)
    work_manager.start_all_workers()


@pyqtSlot(dict)
def handle_results(result):
    # showInfo('slot: ' + str(result))
    if result != '__query_over__':
        # progress.
        handle_results.total.update(result)
    return handle_results.total


class QueryWorkerManager(object):

    def __init__(self):
        self.workers = defaultdict(QueryWorker)

    def get_worker(self, service_unique):
        if service_unique not in self.workers:
            worker = QueryWorker(service_unique)
            # check whether the service is available
            if worker.service:
                self.workers[service_unique] = worker
        else:
            worker = self.workers[service_unique]
        return worker

    def start_worker(self, worker):
        worker.start()

    def start_all_workers(self):
        progress.update_rows(len(self.workers))
        for i, worker in enumerate(self.workers.values()):
            worker.index = i
            worker.start()

    def reset_query_counts(self):
        for worker in self.workers.values():
            worker.completed_counts = 0

    def completed_query_counts(self):
        return sum([worker.completed_counts for worker in self.workers.values()])


class QueryWorker(QThread):

    result_ready = pyqtSignal(dict)
    progress_update = pyqtSignal(dict)

    def __init__(self, service_unique):
        super(QueryWorker, self).__init__()
        self.service_unique = service_unique
        self.index = 0
        self.service = service_manager.get_service(service_unique)
        self.completed_counts = 0
        self.queue = Queue()
        self.result_ready.connect(handle_results)
        self.progress_update.connect(progress.update_labels)

    def target(self, index, service_field, word):
        self.queue.put((index, service_field, word))

    def run(self):
        # self.completed_counts = 0
        while True:
            if progress.abort():
                break
            try:
                index, service_field, word = self.queue.get(timeout=0.1)
                # self.progress_update.emit({
                #     'service_name': self.service.title,
                #     'word': word,
                #     'field_name': service_field
                # })
                result = self.query(service_field, word)
                self.result_ready.emit({index: result})
                self.completed_counts += 1
                # rest a moment
                self.rest()
            except Empty:
                break

    def rest(self):
        time.sleep(self.service.query_interval)

    def query(self, service_field, word):
        self.service.set_notifier(self.progress_update, self.index)
        return self.service.active(service_field, word)


progress = ProgressManager(mw)

work_manager = QueryWorkerManager()
