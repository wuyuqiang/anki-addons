from collections import OrderedDict

from PyQt4 import QtCore, QtGui

import gutil


class SourceWidget(QtGui.QWidget):

    REMOVE_APPEND_MODE = 1
    ONLY_APPEND_MODE = 2
    OVERWRITE_MODE = 3

    def __init__(self, addon, alerts, fields, config=None):
        super(SourceWidget, self).__init__()
        self._src_combo_box = None
        self._dest_field_dict = OrderedDict()
        self._split_check = None

        self._config = config
        self._addon = addon
        self._alerts = alerts
        self._fields = fields

        self._ui()
        self._preset_config()

    def _preset_config(self):
        if not self._config:
            return
        for dest_layout, _ in self._dest_field_dict.items():
            gutil.delete_items_from_layout(dest_layout)
        self._dest_field_dict.clear()

        gutil.set_idx_combo_box(self._src_combo_box, self._config["src"])
        self._split_check.setChecked(self._config["split"])

        write_mode = self._config.get("write_mode", self.REMOVE_APPEND_MODE)
        if write_mode == self.REMOVE_APPEND_MODE:
            self._remove_append_btn.setChecked(True)
        elif write_mode == self.ONLY_APPEND_MODE:
            self._only_append_btn.setChecked(True)
        elif write_mode == self.OVERWRITE_MODE:
            self._overwrite_btn.setChecked(True)

        dest_list = self._config["dest_list"]
        for value_dict in dest_list:
            dest_layout = self._add_dest_field()

            dest_combo_box = self._dest_field_dict[dest_layout]["dest_combo_box"]
            dest_combo_box.setCurrentData(value_dict["dest"])
            # gutil.set_idx_combo_box(dest_combo_box, value_dict["dest"])

            service_combo_box = self._dest_field_dict[dest_layout]["service_combo_box"]
            srv_id = value_dict["service"]
            service_combo_box.setCurrentData(srv_id)
            # gutil.set_idx_combo_box(service_combo_box, srv_id)

            voice_combo_box = self._dest_field_dict[dest_layout]["voice_combo_box"]
            self._set_voice_value(voice_combo_box, srv_id)
            voice_combo_box.setCurrentData(value_dict["voice"])
            # gutil.set_idx_combo_box(voice_combo_box, value_dict["voice"])

    def _ui(self):
        vlayout = QtGui.QVBoxLayout()
        vlayout.findChildren(QtGui.QHBoxLayout)
        vlayout.addLayout(self._ui_src_field())
        vlayout.addLayout(self._ui_dest_field())
        self.setLayout(vlayout)
        # self.setStyleSheet("border:1px solid black;border-radius:5px")

    def _add_dest_field(self):
        dest_layout = self._ui_dest_field()
        self.layout().addLayout(dest_layout)
        return dest_layout

    def _ui_src_field(self):
        src_label = QtGui.QLabel("Source Field:", self)

        self._src_combo_box = gutil.ComboBox(self)
        for field_name in self._get_fields():
            self._src_combo_box.addItem(field_name, field_name)

        dest_button = QtGui.QPushButton('add destination', self)
        dest_button.clicked.connect(self._add_dest_field)

        self._split_check = QtGui.QCheckBox("split")
        self._remove_append_btn = QtGui.QRadioButton("remove append")
        self._remove_append_btn.setChecked(True)
        self._only_append_btn = QtGui.QRadioButton("only append")
        self._overwrite_btn = QtGui.QRadioButton("overwrite")

        self._write_mode = QtGui.QButtonGroup(self)
        self._write_mode.addButton(self._remove_append_btn, self.REMOVE_APPEND_MODE)
        self._write_mode.addButton(self._only_append_btn, self.ONLY_APPEND_MODE)
        self._write_mode.addButton(self._overwrite_btn, self.OVERWRITE_MODE)

        src_field_layout = QtGui.QHBoxLayout()
        src_field_layout.addWidget(src_label)
        src_field_layout.addWidget(self._src_combo_box)
        src_field_layout.addWidget(self._split_check)
        src_field_layout.addStretch()

        src_field_layout.addWidget(self._remove_append_btn)
        src_field_layout.addWidget(self._only_append_btn)
        src_field_layout.addWidget(self._overwrite_btn)

        src_field_layout.addStretch()
        src_field_layout.addWidget(dest_button)

        return src_field_layout

    def _ui_dest_field(self):
        dest_field_layout = QtGui.QHBoxLayout()

        del_button = QtGui.QPushButton('-')
        del_button.setFixedSize(15, 15)

        def remove_layout():
            self.layout().removeItem(dest_field_layout)
            gutil.delete_items_from_layout(dest_field_layout)
            self._dest_field_dict.pop(dest_field_layout)
            return

        del_button.clicked.connect(remove_layout)

        dest_label = QtGui.QLabel("Dest Field:")
        dest_combo_box = gutil.ComboBox()
        for field_name in self._get_fields():
            dest_combo_box.addItem(field_name, field_name)

        preset_combo_box = gutil.ComboBox()
        preset_combo_box.addItem("Load preset..")
        preset_combo_box.insertSeparator(1)
        presets = self._addon.config['presets']
        preset_combo_box.addItems(sorted(presets.keys(), key=lambda key: key.lower()))

        service_combo_box = gutil.ComboBox()
        for srv_id, text in self._get_service():
            service_combo_box.addItem(text, srv_id)

        voice_combo_box = gutil.ComboBox()

        def _on_service_activated():
            srv_id = service_combo_box.getCurrentData()
            self._set_voice_value(voice_combo_box, srv_id)

        service_combo_box.activated.connect(_on_service_activated)

        def _on_preset_activated_inner(idx):
            if idx == 0:
                return
            name = preset_combo_box.currentText()
            try:
                preset = self._addon.config['presets'][name]
                svc_id = preset['service']
            except KeyError:
                self._alerts("%s preset is invalid." % name, self)
                return

            idx = service_combo_box.findData(svc_id)
            if idx < 0:
                self._alerts(self._addon.router.get_unavailable_msg(svc_id),
                             self)
                return
            service_combo_box.setCurrentIndex(idx)
            _on_service_activated()
            voice_combo_box.setCurrentData(preset['voice'])

        preset_combo_box.activated.connect(_on_preset_activated_inner)
        dest_field_layout.addWidget(del_button)
        dest_field_layout.addWidget(dest_label)
        dest_field_layout.addWidget(dest_combo_box)
        dest_field_layout.addWidget(preset_combo_box)
        dest_field_layout.addWidget(service_combo_box)
        dest_field_layout.addWidget(voice_combo_box)

        self._dest_field_dict[dest_field_layout] = {
            "dest_combo_box": dest_combo_box,
            "service_combo_box": service_combo_box,
            "voice_combo_box": voice_combo_box,
        }

        _on_service_activated()
        return dest_field_layout

    def _set_voice_value(self, voice_combo_box, srv_id):
        voice_combo_box.clear()
        for key, text in self._get_voice_option(srv_id):
            voice_combo_box.addItem(text, key)

    @staticmethod
    def _get_combobox_strdata(combo_box):
        index = combo_box.currentIndex()
        data = combo_box.itemData(index)
        # data = str(data)
        return data

    def get_widget_values(self):
        values = {
            "src": self._get_combobox_strdata(self._src_combo_box),
            "split": self._split_check.isChecked(),
            "write_mode": self._write_mode.checkedId(),
            "dest_list": [],
        }

        dest = values["dest_list"]
        for _, boxes in self._dest_field_dict.items():
            dest_name = self._get_combobox_strdata(boxes["dest_combo_box"])
            service = self._get_combobox_strdata(boxes["service_combo_box"])
            voice = self._get_combobox_strdata(boxes["voice_combo_box"])
            dest.append({
                "dest": dest_name,
                "service": service,
                "voice": voice,
            })
        return values

    def _get_fields(self):
        return self._fields

    def _get_service(self):
        return self._addon.router.get_services()

    def _get_voice_option(self, srv_id):
        options = self._addon.router.get_options(srv_id)
        return options[0]["values"]
