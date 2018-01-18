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
import sys
from collections import namedtuple

import anki
import aqt
import aqt.models
from aqt import mw
from aqt.qt import *
from aqt.studydeck import StudyDeck
from aqt.utils import shortcut, showInfo
from .constants import VERSION, Endpoint, Template
from .context import app_icon, config
from .lang import _, _sl
from .service import service_manager
from .utils import MapDict, get_icon, get_model_byId, get_ord_from_fldname

DICT_COMBOS, DICT_FILED_COMBOS, ALL_COMBOS = [0, 1, 2]

widget_size = namedtuple('WidgetSize', ['dialog_width', 'dialog_height_margin', 'map_min_height',
                                        'map_max_height', 'map_fld_width', 'map_dictname_width',
                                        'map_dictfield_width'])(500, 200, 0, 30, 100, 130, 130)


class FoldersManageDialog(QDialog):

    def __init__(self, parent=0):
        QDialog.__init__(self, parent)
        self.parent = parent
        self.setWindowTitle(u"Set Dicts")
        self._dict_paths = []
        self.build()

    def build(self):
        layout = QVBoxLayout()
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("+")
        remove_btn = QPushButton("-")
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(remove_btn)
        add_btn.clicked.connect(self.add_folder)
        remove_btn.clicked.connect(self.remove_folder)
        self.folders_lst = QListWidget()
        self.folders_lst.addItems(config.dirs)
        self.chk_use_filename = QCheckBox(_('CHECK_FILENAME_LABEL'))
        self.chk_export_media = QCheckBox(_('EXPORT_MEDIA'))
        self.chk_use_filename.setChecked(config.use_filename)
        self.chk_export_media.setChecked(config.export_media)
        chk_layout = QHBoxLayout()
        chk_layout.addWidget(self.chk_use_filename)
        chk_layout.addWidget(self.chk_export_media)
        btnbox = QDialogButtonBox(QDialogButtonBox.Ok, Qt.Horizontal, self)
        btnbox.accepted.connect(self.accept)
        layout.addLayout(btn_layout)
        layout.addWidget(self.folders_lst)
        layout.addLayout(chk_layout)
        layout.addWidget(btnbox)
        self.setLayout(layout)

    def add_folder(self):
        dir_ = QFileDialog.getExistingDirectory(self,
                                                caption=u"Select Folder", directory="", options=QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if dir_:
            self.folders_lst.addItem(dir_)

    def remove_folder(self):
        item = self.folders_lst.takeItem(self.folders_lst.currentRow())
        del item

    def find_mdxes(self):
        for each in self.dirs:
            for dirpath, dirnames, filenames in os.walk(each):
                self._dict_paths.extend([os.path.join(dirpath, filename)
                                         for filename in filenames if filename.lower().endswith(u'.mdx')])
        return list(set(self._dict_paths))

    @property
    def dict_paths(self):
        return self.find_mdxes()

    @property
    def dirs(self):
        return [self.folders_lst.item(i).text()
                for i in range(self.folders_lst.count())]

    def save(self):
        data = {'dirs': self.dirs,
                'use_filename': self.chk_use_filename.isChecked(),
                'export_media': self.chk_export_media.isChecked()}
        config.update(data)


class OptionsDialog(QDialog):

    def __init__(self, parent=0):
        super(OptionsDialog, self).__init__()
        self.setWindowFlags(Qt.CustomizeWindowHint |
                            Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowMinMaxButtonsHint)
        self.parent = parent
        # from PyQt4 import QtCore, QtGui
        self.setWindowIcon(app_icon)
        self.setWindowTitle(u"Options")
        self.build()

    def build(self):
        self.main_layout = QVBoxLayout()
        models_layout = QHBoxLayout()
        # add buttons
        mdx_button = QPushButton(_('DICTS_FOLDERS'))
        mdx_button.clicked.connect(self.show_fm_dialog)
        self.models_button = QPushButton(_('CHOOSE_NOTE_TYPES'))
        self.models_button.clicked.connect(self.btn_models_pressed)
        models_layout.addWidget(mdx_button)
        models_layout.addWidget(self.models_button)
        self.main_layout.addLayout(models_layout)
        # add dicts mapping
        dicts_widget = QWidget()
        self.dicts_layout = QGridLayout()
        self.dicts_layout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        dicts_widget.setLayout(self.dicts_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(dicts_widget)
        #scroll_area.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding)

        self.main_layout.addWidget(scroll_area)
        # add description of radio buttons AND ok button
        bottom_layout = QHBoxLayout()
        about_btn = QPushButton(_('ABOUT'))
        about_btn.clicked.connect(self.show_about)
        chk_update_btn = QPushButton(_('UPDATE'))
        chk_update_btn.clicked.connect(self.check_updates)
        home_label = QLabel(
            '<a href="{url}">User Guide</a>'.format(url=Endpoint.user_guide))
        home_label.setOpenExternalLinks(True)
        shop_label = QLabel(
            '<a href="{url}">Service Shop</a>'.format(url=Endpoint.service_shop))
        shop_label.setOpenExternalLinks(True)
        btnbox = QDialogButtonBox(QDialogButtonBox.Ok, Qt.Horizontal, self)
        btnbox.accepted.connect(self.accept)
        bottom_layout.addWidget(about_btn)
        bottom_layout.addWidget(chk_update_btn)
        bottom_layout.addWidget(home_label)
        bottom_layout.addWidget(shop_label)
        bottom_layout.addWidget(btnbox)
        self.main_layout.addLayout(bottom_layout)
        self.setLayout(self.main_layout)
        # init from saved data
        self.current_model = None
        if config.last_model_id:
            self.current_model = get_model_byId(
                mw.col.models, config.last_model_id)
            if self.current_model:
                self.models_button.setText(
                    u'%s [%s]' % (_('CHOOSE_NOTE_TYPES'),  self.current_model['name']))
                # build fields -- dicts layout
                self.build_mappings_layout(self.current_model)

    def show_about(self):
        QMessageBox.about(self, _('ABOUT'), Template.tmpl_about)

    def show_fm_dialog(self):
        fm_dialog = FoldersManageDialog(self)
        fm_dialog.activateWindow()
        fm_dialog.raise_()
        if fm_dialog.exec_() == QDialog.Accepted:
            dict_paths = fm_dialog.dict_paths
            fm_dialog.save()
            # update local services
            service_manager.update_services()
            # update_dicts_combo
            dict_cbs = self._get_combos(DICT_COMBOS)
            for i, cb in enumerate(dict_cbs):
                current_text = cb.currentText()
                self.fill_dict_combo_options(cb, current_text)

    def accept(self):
        self.save()
        self.close()

    def btn_models_pressed(self):
        self.save()
        self.current_model = self.show_models()
        if self.current_model:
            self.build_mappings_layout(self.current_model)

    def build_mappings_layout(self, model):

        def clear_layout(layout):
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
                    else:
                        clear_layout(item.layout())

        clear_layout(self.dicts_layout)

        label1 = QLabel("")
        label1.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        label2 = QLabel(_("DICTS"))
        label2.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        label3 = QLabel(_("DICT_FIELDS"))
        label3.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.dicts_layout.addWidget(label1, 0, 0)
        self.dicts_layout.addWidget(label2, 0, 1)
        self.dicts_layout.addWidget(label3, 0, 2)

        maps = config.get_maps(model['id'])
        self.radio_group = QButtonGroup()
        for i, fld in enumerate(model['flds']):
            ord = fld['ord']
            name = fld['name']
            if maps:
                for j, each in enumerate(maps):
                    if each.get('fld_ord', -1) == ord:
                        self.add_dict_layout(j, fld_name=name, **each)
                        break
                else:
                    self.add_dict_layout(i, fld_name=name)
            else:
                self.add_dict_layout(i, fld_name=name)

        self.setLayout(self.main_layout)
        self.resize(widget_size.dialog_width, (i + 1) * widget_size.map_max_height + widget_size.dialog_height_margin)

    def show_models(self):
        edit = QPushButton(anki.lang._("Manage"),
                           clicked=lambda: aqt.models.Models(mw, self))
        ret = StudyDeck(mw, names=lambda: sorted(mw.col.models.allNames()),
                        accept=anki.lang._("Choose"), title=anki.lang._("Choose Note Type"),
                        help="_notes", parent=self, buttons=[edit],
                        cancel=True, geomKey="selectModel")
        if ret.name:
            model = mw.col.models.byName(ret.name)
            self.models_button.setText(
                u'%s [%s]' % (_('CHOOSE_NOTE_TYPES'), ret.name))
            return model

    def dict_combobox_index_changed(self, index):
        # showInfo("combo index changed")
        dict_combos, field_combos = self._get_combos(ALL_COMBOS)
        assert len(dict_combos) == len(field_combos)
        for i, dict_combo in enumerate(dict_combos):
            # in windows and linux: the combo has current focus,
            # in mac: the combo's listview has current focus, and the listview can
            # be got by view()
            # showInfo('to check focus')
            if dict_combo.hasFocus() or dict_combo.view().hasFocus():
                self.fill_field_combo_options(
                    field_combos[i], dict_combo.currentText(), dict_combo.itemData(index))
                break

    def fill_dict_combo_options(self, dict_combo, current_text):
        dict_combo.clear()
        dict_combo.addItem(_('NOT_DICT_FIELD'))
        dict_combo.insertSeparator(dict_combo.count())
        for service in service_manager.local_services:
            # combo_data.insert("data", each.label)
            dict_combo.addItem(
                service.title, userData=service.unique)
        dict_combo.insertSeparator(dict_combo.count())
        for service in service_manager.web_services:
            dict_combo.addItem(
                service.title, userData=service.unique)

        def set_dict_combo_index():
            dict_combo.setCurrentIndex(-1)
            for i in range(dict_combo.count()):
                if current_text in _sl('NOT_DICT_FIELD'):
                    dict_combo.setCurrentIndex(0)
                if dict_combo.itemText(i) == current_text:
                    dict_combo.setCurrentIndex(i)

        set_dict_combo_index()

    def fill_field_combo_options(self, field_combo, dict_combo_text, dict_combo_itemdata):
        field_combo.clear()
        field_combo.setEnabled(True)
        if dict_combo_text in _sl('NOT_DICT_FIELD'):
            field_combo.setEnabled(False)
        elif dict_combo_text in _sl('MDX_SERVER'):
            field_combo.setEditText('http://')
            field_combo.setFocus(Qt.MouseFocusReason)  # MouseFocusReason
        else:
            field_text = field_combo.currentText()
            service_unique = dict_combo_itemdata
            current_service = service_manager.get_service(service_unique)
            # problem
            if current_service and current_service.fields:
                for each in current_service.fields:
                    field_combo.addItem(each)
                    if each == field_text:
                        field_combo.setEditText(field_text)

    def radio_btn_checked(self):
        rbs = self.findChildren(QRadioButton)
        dict_cbs, fld_cbs = self._get_combos(ALL_COMBOS)
        for i, rb in enumerate(rbs):
            dict_cbs[i].setEnabled(not rb.isChecked())
            fld_cbs[i].setEnabled(
                (dict_cbs[i].currentText() != _('NOT_DICT_FIELD')) and (not rb.isChecked()))

    def add_dict_layout(self, i, **kwargs):
        """
        kwargs:
        word_checked  dict  fld_name dict_field
        """
        word_checked, dict_name, dict_unique, fld_name, dict_field = (
            kwargs.get('word_checked', False),
            kwargs.get('dict', _('NOT_DICT_FIELD')),
            kwargs.get('dict_unique', ''),
            kwargs.get('fld_name', ''),
            kwargs.get('dict_field', ''),)

        word_check_btn = QRadioButton(fld_name)
        word_check_btn.setMinimumSize(0, 0)
        word_check_btn.setMaximumSize(widget_size.map_fld_width+1000,
                                      widget_size.map_max_height)
        word_check_btn.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        word_check_btn.setCheckable(True)
        word_check_btn.clicked.connect(self.radio_btn_checked)
        if i == 0:
            word_checked = True
        word_check_btn.setChecked(word_checked)
        self.radio_group.addButton(word_check_btn)

        dict_combo = QComboBox()
        dict_combo.setMinimumSize(widget_size.map_dictname_width, 0)
        dict_combo.setFocusPolicy(
            Qt.TabFocus | Qt.ClickFocus | Qt.StrongFocus | Qt.WheelFocus)
        dict_combo.setEnabled(not word_checked)
        dict_combo.currentIndexChanged.connect(
            self.dict_combobox_index_changed)
        self.fill_dict_combo_options(dict_combo, dict_name)

        field_combo = QComboBox()
        field_combo.setMinimumSize(widget_size.map_dictfield_width, 0)
        # field_combo.setMaximumSize(130, 30)
        field_combo.setEnabled((not word_checked) and (
            dict_name != _('NOT_DICT_FIELD')))
        field_combo.setEditable(True)
        field_combo.setEditText(dict_field)
        self.fill_field_combo_options(field_combo, dict_name, dict_unique)

        self.dicts_layout.addWidget(word_check_btn, i + 1, 0)
        self.dicts_layout.addWidget(dict_combo, i + 1, 1)
        self.dicts_layout.addWidget(field_combo, i + 1, 2)

    def _get_combos(self, flag):
        # 0 : dict_combox, 1:field_combox
        dict_combos = self.findChildren(QComboBox)
        if flag in [DICT_COMBOS, DICT_FILED_COMBOS]:
            return dict_combos[flag::2]
        if flag == ALL_COMBOS:
            return dict_combos[::2], dict_combos[1::2]

    def save(self):
        if not self.current_model:
            return
        data = dict()
        labels = self.findChildren(QRadioButton)
        dict_cbs, field_cbs = self._get_combos(ALL_COMBOS)
        maps = [{"word_checked": label.isChecked(),
                 "dict": dict_cb.currentText().strip(),
                 "dict_unique": dict_cb.itemData(dict_cb.currentIndex()) if dict_cb.itemData(dict_cb.currentIndex()) else "",
                 "dict_field": field_cb.currentText().strip(),
                 "fld_ord": get_ord_from_fldname(self.current_model, label.text()
                                                 )}
                for (dict_cb, field_cb, label) in zip(dict_cbs, field_cbs, labels)]
        current_model_id = str(self.current_model['id'])
        data[current_model_id] = maps
        data['last_model'] = self.current_model['id']
        config.update(data)

    def check_updates(self):

        self.updater = Updater()
        self.updater.chk_finish_signal.connect(self._show_update_result)
        self.updater.start()

    @pyqtSlot(dict)
    def _show_update_result(self, data):
        if data['result'] == 'ok':
            version = data['version']
            if version > VERSION:
                showInfo(Template.new_version.format(version=version))
            elif version == VERSION:
                showInfo(Template.latest_version)
            else:
                showInfo(Template.abnormal_version)
        else:
            showInfo(Template.check_failure.format(msg=data['msg']))


class Updater(QThread):
    chk_finish_signal = pyqtSignal(dict)

    def __init__(self):
        super(QThread, self).__init__()

    def run(self):
        import urllib2
        try:
            req = urllib2.Request(Endpoint.check_version)
            req.add_header('Pragma', 'no-cache')
            resp = urllib2.urlopen(req, timeout=10)
            version = resp.read().strip()
            data = {'result': 'ok', 'version': version}
        except:
            info = _('CHECK_FAILURE')
            data = {'result': 'error', 'msg': info}

        self.chk_finish_signal.emit(data)


def show_options():
    config.read()
    opt_dialog = OptionsDialog(mw)
    opt_dialog.exec_()
    opt_dialog.activateWindow()
    opt_dialog.raise_()
    # service_manager.fetch_headers()
