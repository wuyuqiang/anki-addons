import copy
import warnings

from PyQt4 import QtGui, QtCore

from power_format_pack import preferences
from power_format_pack import utility
from power_format_pack.prefhelper import PrefHelper
from power_format_pack.qt.views.keysequencedialog import Ui_KeySequenceDialog
from power_format_pack.qt.views.table_keybindings import Ui_TableKeyBindings


class ClickEvent(QtCore.QObject):
    def __init__(self, parent):
        super(ClickEvent, self).__init__(parent)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            dialog = KeySequenceDialog()
            key_sequence = dialog.key_sequence
            if key_sequence:
                pretty = utility.key_to_text(key_sequence)
                source.setText(pretty)
            return True
        return False


class FormKeyBindings(QtGui.QDialog):
    def __init__(self, parent, keybindings):
        super(FormKeyBindings, self).__init__(parent)
        self.keybindings = keybindings
        self.new_keybindings = copy.deepcopy(self.keybindings)

        self.ui = Ui_TableKeyBindings()
        self.ui.setupUi(self)
        self.table = self.ui.tableWidget
        self.ui.tableWidget.cellDoubleClicked[int, int].connect(self.on_double_click)
        button_box = self.ui.buttonBox
        restore_defaults_button = button_box.button(QtGui.QDialogButtonBox.RestoreDefaults)
        restore_defaults_button.clicked.connect(self.on_reset_defaults)
        reset_button = button_box.button(QtGui.QDialogButtonBox.Reset)
        reset_button.clicked.connect(self.on_reset)

        self._fill_table(keybindings)

        self.exec_()

    def _fill_table(self, keybindings):
        num_iterator = utility.create_counter()
        self.table.setRowCount(len(keybindings))
        # create all cells
        for action, keybinding in sorted(keybindings.iteritems()):
            pretty_action = utility.prettify_option_name(action)
            current_row = num_iterator.next()
            action_cell = QtGui.QTableWidgetItem(pretty_action)
            # action cells should be non-modifiable
            action_cell.setFlags(action_cell.flags() & ~QtCore.Qt.ItemIsEditable)
            self.table.setItem(current_row, 0, action_cell)
            keybinding_cell = QtGui.QTableWidgetItem(utility.key_to_text(keybinding))
            # keybinding cells should be non-modifiable
            keybinding_cell.setFlags(action_cell.flags() & ~QtCore.Qt.ItemIsEditable)
            self.table.setItem(current_row, 1, keybinding_cell)
        self.table.resizeColumnsToContents()

    def refill_table(self, keybindings):
        num_iterator = utility.create_counter()
        for _ in xrange(self.table.rowCount()):
            current_row = num_iterator.next()
            action_cell = self.table.item(current_row, 0)
            keybinding_cell = self.table.item(current_row, 1)
            ugly_action = utility.deprettify_option_name(action_cell.text())
            keybinding_cell.setText(utility.key_to_text(keybindings.get(ugly_action)))

    def on_double_click(self, row, column):
        # ignore double clicks on action cells
        if column == 0:
            return
        action_cell = self.table.item(row, column - 1)
        keybinding_cell = self.table.item(row, column)
        if action_cell and keybinding_cell:
            dialog = KeySequenceDialog(self, action_cell.text())
            key_sequence = dialog.key_sequence
            if key_sequence:
                self.new_keybindings[utility.deprettify_option_name(action_cell.text())] = key_sequence
                keybinding_cell.setText(utility.key_to_text(key_sequence))

    def on_reset_defaults(self):
        default_keybindings = PrefHelper.get_default_keybindings()
        self.new_keybindings = default_keybindings
        self.refill_table(default_keybindings)

    def on_reset(self):
        self.new_keybindings = copy.deepcopy(self.keybindings)
        self.refill_table(self.new_keybindings)

    def accept(self):
        if PrefHelper.are_dicts_different(self.keybindings, self.new_keybindings):
            PrefHelper.save_keybindings(self.new_keybindings)
            preferences.KEYS = self.new_keybindings
        self.close()

    @staticmethod
    def create_num_iterator():
        num = 0
        while True:
            yield num
            num += 1


class KeySequenceDialog(QtGui.QDialog):

    def __init__(self, parent, action):
        super(KeySequenceDialog, self).__init__(parent)
        self.key_sequence = None
        self.ui = Ui_KeySequenceDialog()
        self.ui.setupUi(self)
        self.ui.label.setText("<p align=\"center\">" +
                              "Press the key combination you want to associate<br/>" +
                              "with the '{}' button.</p>".format(action))
        self.exec_()

    def keyPressEvent(self, event):
        key = event.key()

        if key == QtCore.Qt.Key_unknown:
            warnings.warn("Unknown key from a macro probably")
            return

        # the user have clicked just and only the special keys Ctrl, Shift, Alt, Meta.
        if key in (QtCore.Qt.Key_Control, QtCore.Qt.Key_Shift, QtCore.Qt.Key_Alt, QtCore.Qt.Key_Meta):
            return

        # check for a combination of user clicks
        modifiers = event.modifiers()

        if modifiers & QtCore.Qt.ShiftModifier:
            key += QtCore.Qt.SHIFT
        if modifiers & QtCore.Qt.ControlModifier:
            key += QtCore.Qt.CTRL
        if modifiers & QtCore.Qt.AltModifier:
            key += QtCore.Qt.ALT
        if modifiers & QtCore.Qt.MetaModifier:
            key += QtCore.Qt.META

        self.key_sequence = QtGui.QKeySequence(key)
        self.close()
