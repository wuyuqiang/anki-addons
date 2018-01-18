from PyQt4 import QtCore, QtGui


def delete_items_from_layout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                delete_items_from_layout(item.layout())


def set_idx_combo_box(combo_box, value):
    idx = max(combo_box.findData(value), 0)
    combo_box.setCurrentIndex(idx)


class ComboBox(QtGui.QComboBox):

    def wheelEvent(self, e):
        # self.parentWidget().wheelEvent(e)
        e.ignore()

    def getCurrentData(self):
        index = self.currentIndex()
        data = self.itemData(index)
        return data

    def setCurrentData(self, data):
        idx = max(self.findData(data), 0)
        self.setCurrentIndex(idx)