import os
import sys
import json
from collections import OrderedDict

from PyQt4 import QtCore, QtGui

from re import compile as re

import Log

from .common import Label, Note, ICON
from .base import Dialog, ServiceDialog
from ..paths import CUSTOME_CONFIG

from .wcustom import *


LOG = Log.getLogger(__name__)

__all__ = ['CustomGenerator']


class Config:

    CONFIG_PATH = CUSTOME_CONFIG

    MAIN_SECTION = "main_section"
    LAST_SECTION = "last_section"

    def __init__(self):
        self._config = OrderedDict()
        self._config[self.MAIN_SECTION] = None
        self._config[self.LAST_SECTION] = None
        self._load()

    def _load(self):
        if not os.path.exists(self.CONFIG_PATH):
            return False
        fp = open(self.CONFIG_PATH)
        self._config = json.load(fp, object_pairs_hook=OrderedDict)
        fp.close()
        return True

    def save(self):
        fp = open(self.CONFIG_PATH, "w")
        json.dump(self._config, fp)
        fp.close()

    def _get_section(self, sec_name):
        section = self._config[sec_name]
        if section is None:
            self._config[sec_name] = OrderedDict()
            section = self._config[sec_name]
        return section

    def set_src_list_conf(self, conf_name, src_list):
        main_sec = self._get_section(self.MAIN_SECTION)
        main_sec[conf_name] = src_list
        self.save()

    def src_list_conf(self, conf_name):
        main_sec = self._get_section(self.MAIN_SECTION)
        return main_sec[conf_name]

    def src_list_conf_keys(self):
        main_sec = self._get_section(self.MAIN_SECTION)
        return main_sec.keys()

    def set_last_conf_name(self, conf_name):
        last_sec = self._get_section(self.LAST_SECTION)
        last_sec["conf_name"] = conf_name
        self.save()

    def last_conf_name(self):
        last_sec = self._get_section(self.LAST_SECTION)
        return last_sec.get("conf_name", None)

    def set_last_src_list(self, src_list):
        last_sec = self._get_section(self.LAST_SECTION)
        last_sec["src_list"] = src_list
        self.save()

    def last_src_list(self):
        last_sec = self._get_section(self.LAST_SECTION)
        return last_sec.get("src_list", [])


class CustomGenerator(Dialog):

    HELP_USAGE_DESC = "Adding audio to multiple notes"

    HELP_USAGE_SLUG = 'browser'

    _RE_WHITESPACE = re(r'\s+')

    def __init__(self, browser, alerts, *args, **kwargs):
        self._browser = browser
        self._alerts = alerts

        self._src_field_dict = OrderedDict()
        self._config = Config()
        super(CustomGenerator, self).__init__(title="Custom Generator", *args, **kwargs)

    def _ui(self):
        super_layout = super(CustomGenerator, self)._ui()

        area_widget = QtGui.QWidget()
        self._scroll_area_layout = QtGui.QVBoxLayout(area_widget)
        main_area = QtGui.QScrollArea()
        main_area.setWidget(area_widget)
        main_area.setWidgetResizable(True)

        main_vbox = QtGui.QVBoxLayout()
        main_vbox.addLayout(self._ui_top())
        main_vbox.addWidget(main_area)
        main_vbox.addWidget(self._ui_buttons())

        super_layout.addLayout(main_vbox)
        return super_layout

    def _ui_buttons(self):
        """
        Adjust title of the OK button.
        """

        buttons = super(CustomGenerator, self)._ui_buttons()
        buttons.findChild(QtGui.QAbstractButton, 'okay').setText("&Generate")

        return buttons

    def _reset_config_combo_box(self, current_config=None):
        self._config_combo_box.clear()
        self._config_combo_box.addItem("load config ...", "load")
        self._config_combo_box.insertSeparator(1)
        if not self._config:
            return
        for config_name in self._config.src_list_conf_keys():
            self._config_combo_box.addItem(config_name, config_name)

        if current_config:
            gutil.set_idx_combo_box(self._config_combo_box, current_config)

    def _ui_top(self):
        self._add_src_button = QtGui.QPushButton('add source')
        self._add_src_button.clicked.connect(self._ui_add_src_field)

        self._config_combo_box = gutil.ComboBox()
        self._reset_config_combo_box()
        self._config_combo_box.activated.connect(self._full_config_to_widgets)

        self._save_button = QtGui.QPushButton('save')
        self._save_button.clicked.connect(self._save_config)

        add_src_hbox = QtGui.QHBoxLayout()
        add_src_hbox.addWidget(self._add_src_button)
        add_src_hbox.addStretch(1)
        add_src_hbox.addWidget(self._config_combo_box)
        add_src_hbox.addWidget(self._save_button)

        return add_src_hbox

    def _full_config_to_widgets(self, idx):
        if idx == 0:
            print "nothing"
            return
        config_name = self._config_combo_box.currentText()
        # config_name = str(config_name)
        # gutil.delete_items_from_layout(self._scroll_area_layout)
        # self._src_field_dict.clear()

        src_config_list = self._config.src_list_conf(config_name)
        self._reset_config_to_widgets(src_config_list)
        # for src_config in src_config_list:
        #     self._ui_add_src_field(src_config)

    def _reset_config_to_widgets(self, src_config_list):
        gutil.delete_items_from_layout(self._scroll_area_layout)
        self._src_field_dict.clear()

        for src_config in src_config_list:
            self._ui_add_src_field(src_config)

    def _save_config(self):
        idx = self._config_combo_box.currentIndex()
        default_conf = ""
        if idx > 0:
            default_conf = self._config_combo_box.getCurrentData()
        config_name, ok = QtGui.QInputDialog.getText(self, 'save config', 'please enter config name:', text=default_conf)
        if not ok:
            return
        # config_name = str(config_name)
        values = self.get_widget_values()
        self._config.set_src_list_conf(config_name, values)
        self._config.set_last_conf_name(config_name)
        self._config.set_last_src_list(values)
        self._reset_config_combo_box(config_name)
        print "config save ok."

    def _ui_add_src_field(self, src_config=None):
        del_button = QtGui.QPushButton('-')
        del_button.setFixedSize(15, 15)
        src_widget = SourceWidget(self._addon, self._alerts, self._fields, src_config)

        src_hbox = QtGui.QHBoxLayout()
        src_hbox.addWidget(del_button)
        src_hbox.addWidget(src_widget)

        self._scroll_area_layout.addLayout(src_hbox)

        self._src_field_dict[src_hbox] = src_widget
        self._resize()

        def del_src_field():
            self._scroll_area_layout.removeItem(src_hbox)
            gutil.delete_items_from_layout(src_hbox)
            self._src_field_dict.pop(src_hbox)
            self._resize()
            return

        del_button.clicked.connect(del_src_field)
        return src_hbox

    def _resize(self):
        size = QtCore.QSize()
        i = 1
        for layout, widget in self._src_field_dict.items():
            size = size.expandedTo(widget.sizeHint())
            i += 1
        self.resize(size.width() + 150, size.height() * i + 150)

    def get_widget_values(self):
        values = []
        for _, widget in self._src_field_dict.items():
            v = widget.get_widget_values()
            values.append(v)
        return values

    def show(self):
        self._notes = [
            self._browser.mw.col.getNote(note_id)
            for note_id in self._browser.selectedNotes()
        ]

        # self.findChild(Note, 'intro').setText(
        #     '%d note%s selected. Click "Help" for usage hints.' %
        #     (len(self._notes), "s" if len(self._notes) != 1 else "")
        # )

        self._fields = sorted({
            field
            for note in self._notes
            for field in note.keys()
        })

        last_conf_name = self._config.last_conf_name()
        self._config_combo_box.setCurrentData(last_conf_name)
        # self._reset_config_combo_box(last_conf_name)
        # self._full_config_to_widgets(self._config_combo_box.currentIndex())

        last_src_list = self._config.last_src_list()
        self._reset_config_to_widgets(last_src_list)

        super(CustomGenerator, self).show()

    def accept(self):

        # eligible_notes = [
        #     note
        #     for note in self._notes
        #     if source in note.keys() and dest in note.keys()
        # ]
        #
        # if not eligible_notes:
        #     self._alerts(
        #         "Of the %d notes selected in the browser, none have both "
        #         "'%s' and '%s' fields." % (len(self._notes), source, dest)
        #         if len(self._notes) > 1
        #         else "The selected note does not have both '%s' and '%s'"
        #              "fields." % (source, dest),
        #         self,
        #     )
        #     return
        eligible_notes = self._notes

        self._process = {
            'all': None,
            'aborted': False,
            'progress': _Progress(
                maximum=len(eligible_notes),
                on_cancel=self._accept_abort,
                title="Generating MP3s",
                addon=self._addon,
                parent=self,
            ),
            'query_iter': QueryIterator(eligible_notes, self.get_widget_values()),
            'handling': {
                'append': True,
                'behavior': True,
            },
            'queue': eligible_notes,
            'counts': {
                'total': len(self._notes),
                'elig': len(eligible_notes),
                'skip': len(self._notes) - len(eligible_notes),
                'done': 0,  # all notes processed
                'okay': 0,  # calls which resulted in a successful MP3
                'fail': 0,  # calls which resulted in an exception
            },
            'exceptions': {},
            'throttling': {
                'calls': {},  # unthrottled download calls made per service
                'sleep': self._addon.config['throttle_sleep'],
                'threshold': self._addon.config['throttle_threshold'],
            },
        }

        self._browser.mw.checkpoint("AwesomeTTS Batch Update")
        self._process['progress'].show()
        self._browser.model.beginReset()

        self._accept_next()

    def _accept_abort(self):
        """
        Flags that the user has requested that processing stops.
        """

        self._process['aborted'] = True

    def _accept_next(self):
        """
        Pop the next note off the queue, if not throttled, and process.
        """

        self._accept_update()

        proc = self._process
        throttling = proc['throttling']

        query_iter = proc['query_iter']
        if proc['aborted'] or query_iter.is_finished():
            self._accept_done()
            return

        if throttling['calls'] and \
           max(throttling['calls'].values()) >= throttling['threshold']:
            # at least one service needs a break

            timer = QtCore.QTimer()
            throttling['timer'] = timer
            throttling['countdown'] = throttling['sleep']

            timer.timeout.connect(self._accept_throttled)
            timer.setInterval(1000)
            timer.start()
            return

        # note = proc['queue'].pop(0)
        # phrase = note[proc['fields']['source']]
        item = query_iter.next_item()
        note = item["note"]
        write_mode = item["write_mode"]
        phrase = self._addon.strip.from_note(item['phrase'])
        self._accept_update(phrase)

        def done():
            """Count the processed note."""

            proc['counts']['done'] += 1

        def okay(path):
            """Count the success and update the note."""

            filename = self._browser.mw.col.media.addFile(path)
            dest = item['dest']
            note[dest] = self._accept_next_output(note[dest], filename, write_mode)
            note.flush()

            proc['counts']['okay'] += 1

        def fail(exception):
            """Count the failure and the unique message."""
            error_filename = "_w_custom_error.mp3"
            dest = item['dest']
            note[dest] = self._accept_next_output(note[dest], error_filename, write_mode)
            note.flush()

            proc['counts']['fail'] += 1

            message = exception.message
            if isinstance(message, basestring):
                message = self._RE_WHITESPACE.sub(' ', message).strip()

            try:
                proc['exceptions'][message] += 1
            except KeyError:
                proc['exceptions'][message] = 1

        def miss(svc_id, count):
            """Count the cache miss."""

            try:
                throttling['calls'][svc_id] += count
            except KeyError:
                throttling['calls'][svc_id] = count

        callbacks = dict(
            done=done, okay=okay, fail=fail, miss=miss,

            # The call to _accept_next() is done via a single-shot QTimer for
            # a few reasons: keep the UI responsive, avoid a "maximum
            # recursion depth exceeded" exception if we hit a string of cached
            # files, and allow time to respond to a "cancel".
            then=lambda: QtCore.QTimer.singleShot(0, self._accept_next),
        )

        svc_id = item['svc_id']
        want_human = (self._addon.config['filenames_human'] or u'{{text}}' if
                      self._addon.config['filenames'] == 'human' else False)

        if svc_id.startswith('group:'):
            config = self._addon.config
            self._addon.router.group(text=phrase,
                                     group=config['groups'][svc_id[6:]],
                                     presets=config['presets'],
                                     callbacks=callbacks,
                                     want_human=want_human,
                                     note=note)
        else:
            self._addon.router(svc_id=svc_id,
                               text=phrase,
                               options=item['options'],
                               callbacks=callbacks,
                               want_human=want_human,
                               note=note)

    def _accept_next_output(self, old_value, filename, write_mode):
        """
        Given a note's old value and our current handling options,
        returns a new note value using the passed filename.
        """

        if write_mode == SourceWidget.REMOVE_APPEND_MODE:
            return self._addon.strip.sounds.univ(old_value).strip() + \
                   ' [sound:%s]' % filename
        elif write_mode == SourceWidget.ONLY_APPEND_MODE:
            return old_value + ' [sound:%s]' % filename
        elif write_mode == SourceWidget.OVERWRITE_MODE:
            return '[sound:%s]' % filename

        # proc = self._process

        # if proc['handling']['append']:
        #     if proc['handling']['behavior']:
        #         return self._addon.strip.sounds.univ(old_value).strip() + \
        #             ' [sound:%s]' % filename
        #     elif filename in old_value:
        #         return old_value
        #     else:
        #         return old_value + ' [sound:%s]' % filename
        #
        # else:
        #     if proc['handling']['behavior']:
        #         return '[sound:%s]' % filename
        #     else:
        #         return filename

    def _accept_throttled(self):
        """
        Called for every "timeout" of the timer during a throttling.
        """

        proc = self._process

        if proc['aborted']:
            proc['throttling']['timer'].stop()
            self._accept_done()
            return

        proc['throttling']['countdown'] -= 1
        self._accept_update()

        if proc['throttling']['countdown'] <= 0:
            proc['throttling']['timer'].stop()
            del proc['throttling']['countdown']
            del proc['throttling']['timer']
            proc['throttling']['calls'] = {}
            self._accept_next()

    def _accept_update(self, detail=None):
        """
        Update the progress bar and message.
        """

        proc = self._process

        proc['progress'].update(
            label="finished %d of %d%s\n"
                  "%d successful, %d failed\n"
                  "\n"
                  "%s" % (
                      proc['counts']['done'],
                      proc['counts']['elig'],

                      " (%d skipped)" % proc['counts']['skip']
                      if proc['counts']['skip']
                      else "",

                      proc['counts']['okay'],
                      proc['counts']['fail'],

                      "sleeping for %d second%s" % (
                          proc['throttling']['countdown'],
                          "s"
                          if proc['throttling']['countdown'] != 1
                          else ""
                      )
                      if (
                          proc['throttling'] and
                          'countdown' in proc['throttling']
                      )
                      else " "
                  ),
            value=proc['counts']['done'],
            detail=detail,
        )

    def _accept_done(self):
        """
        Display statistics and close out the dialog.
        """

        self._browser.model.endReset()

        proc = self._process
        proc['progress'].accept()

        messages = [
            "The %d note%s you selected %s been processed. " % (
                proc['counts']['total'],
                "s" if proc['counts']['total'] != 1 else "",
                "have" if proc['counts']['total'] != 1 else "has",
            )
            if proc['counts']['done'] == proc['counts']['total']
            else "%d of the %d note%s you selected %s processed. " % (
                proc['counts']['done'],
                proc['counts']['total'],
                "s" if proc['counts']['total'] != 1 else "",
                "were" if proc['counts']['done'] != 1 else "was",
            ),

            "%d note%s skipped for not having both the source and "
            "destination fields. Of those remaining, " % (
                proc['counts']['skip'],
                "s were" if proc['counts']['skip'] != 1
                else " was",
            )
            if proc['counts']['skip']
            else "During processing, "
        ]

        if proc['counts']['fail']:
            if proc['counts']['okay']:
                messages.append(
                    "%d note%s successfully updated, but "
                    "%d note%s failed while processing." % (
                        proc['counts']['okay'],
                        "s were" if proc['counts']['okay'] != 1
                        else " was",
                        proc['counts']['fail'],
                        "s" if proc['counts']['fail'] != 1
                        else "",
                    )
                )
            else:
                messages.append("no notes were successfully updated.")

            messages.append("\n\n")

            if len(proc['exceptions']) == 1:
                messages.append("The following problem was encountered:")
                messages += [
                    "\n%s (%d time%s)" %
                    (message, count, "s" if count != 1 else "")
                    for message, count
                    in proc['exceptions'].items()
                ]
            else:
                messages.append("The following problems were encountered:")
                messages += [
                    "\n- %s (%d time%s)" %
                    (message, count, "s" if count != 1 else "")
                    for message, count
                    in proc['exceptions'].items()
                ]

        else:
            messages.append("there were no errors.")

        if proc['aborted']:
            messages.append("\n\n")
            messages.append(
                "You aborted processing. If you want to rollback the changes "
                "to the notes that were already processed, use the Undo "
                "AwesomeTTS Batch Update option from the Edit menu."
            )

        # self._addon.config.update(proc['all'])
        # self._disable_inputs(False)
        self._config.set_last_conf_name(self._config_combo_box.getCurrentData())
        self._config.set_last_src_list(self.get_widget_values())
        self._notes = None
        self._process = None

        super(CustomGenerator, self).accept()

        # this alert is done by way of a singleShot() callback to avoid random
        # crashes on Mac OS X, which happen <5% of the time if called directly
        QtCore.QTimer.singleShot(
            0,
            lambda: self._alerts("".join(messages), self._browser),
        )


class _Progress(Dialog):
    """
    Provides a dialog that can be displayed while processing.
    """

    __slots__ = [
        '_maximum'  # the value we are counting up to
        '_on_cancel'  # callable to invoke if the user hits cancel
    ]

    def __init__(self, maximum, on_cancel, *args, **kwargs):
        """
        Configures our bar's maximum and registers a cancel callback.
          """

        self._maximum = maximum
        self._on_cancel = on_cancel
        super(_Progress, self).__init__(*args, **kwargs)

    # UI Construction ########################################################

    def _ui(self):
        """
        Builds the interface with a status label and progress bar.
        """

        self.setMinimumWidth(500)

        status = Note("Please wait...")
        status.setAlignment(QtCore.Qt.AlignCenter)
        status.setObjectName('status')

        progress_bar = QtGui.QProgressBar()
        progress_bar.setMaximum(self._maximum)
        progress_bar.setObjectName('bar')

        detail = Note("")
        detail.setAlignment(QtCore.Qt.AlignCenter)
        detail.setFixedHeight(100)
        detail.setFont(self._FONT_INFO)
        detail.setObjectName('detail')
        detail.setScaledContents(True)

        layout = super(_Progress, self)._ui()
        layout.addStretch()
        layout.addWidget(status)
        layout.addStretch()
        layout.addWidget(progress_bar)
        layout.addStretch()
        layout.addWidget(detail)
        layout.addStretch()
        layout.addWidget(self._ui_buttons())

        return layout

    def _ui_buttons(self):
        """
        Overrides the default behavior to only have a cancel button.
        """

        buttons = QtGui.QDialogButtonBox()
        buttons.setObjectName('buttons')
        buttons.rejected.connect(self.reject)
        buttons.setStandardButtons(QtGui.QDialogButtonBox.Cancel)
        buttons.button(QtGui.QDialogButtonBox.Cancel).setAutoDefault(False)

        return buttons

    # Events #################################################################

    def reject(self):
        """
        On cancel, disable the button and call our registered callback.
        """

        self.findChild(QtGui.QDialogButtonBox, 'buttons').setDisabled(True)
        self._on_cancel()

    def update(self, label, value, detail=None):
        """
        Update the status text and bar.
        """

        self.findChild(Note, 'status').setText(label)
        self.findChild(QtGui.QProgressBar, 'bar').setValue(value)
        if detail:
            self.findChild(Note, 'detail').setText(detail)

