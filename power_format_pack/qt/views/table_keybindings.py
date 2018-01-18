# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'table_keybindings.ui'
#
# Created by: PyQt4 UI code generator 4.12
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_TableKeyBindings(object):
    def setupUi(self, TableKeyBindings):
        TableKeyBindings.setObjectName(_fromUtf8("TableKeyBindings"))
        TableKeyBindings.setWindowModality(QtCore.Qt.ApplicationModal)
        TableKeyBindings.resize(450, 400)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TableKeyBindings.sizePolicy().hasHeightForWidth())
        TableKeyBindings.setSizePolicy(sizePolicy)
        TableKeyBindings.setMinimumSize(QtCore.QSize(450, 400))
        TableKeyBindings.setMaximumSize(QtCore.QSize(450, 400))
        TableKeyBindings.setSizeGripEnabled(False)
        TableKeyBindings.setModal(True)
        self.buttonBox = QtGui.QDialogButtonBox(TableKeyBindings)
        self.buttonBox.setGeometry(QtCore.QRect(10, 360, 431, 32))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setMinimumSize(QtCore.QSize(431, 32))
        self.buttonBox.setMaximumSize(QtCore.QSize(431, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Reset|QtGui.QDialogButtonBox.RestoreDefaults|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.tableWidget = QtGui.QTableWidget(TableKeyBindings)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 430, 341))
        self.tableWidget.setMinimumSize(QtCore.QSize(430, 341))
        self.tableWidget.setMaximumSize(QtCore.QSize(430, 341))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(246, 254, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(246, 254, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(246, 254, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.tableWidget.setPalette(palette)
        self.tableWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.tableWidget.setStyleSheet(_fromUtf8("QHeaderView::section {\n"
"    background-color: rgb(255, 255, 245);\n"
"    border-style: none;\n"
"    border-bottom: 1px solid rgb(217, 217, 217);\n"
"    border-right: 1px solid rgb(217, 217, 217);\n"
"    padding: 4px;\n"
"    font-size: 1em;\n"
"    font-weight: bold;\n"
"    color: black;\n"
"}"))
        self.tableWidget.setFrameShadow(QtGui.QFrame.Plain)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked)
        self.tableWidget.setProperty("showDropIndicator", False)
        self.tableWidget.setDragDropOverwriteMode(False)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(QtCore.Qt.DotLine)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(2)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        item.setFont(font)
        item.setBackground(QtGui.QColor(255, 255, 255))
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(0, 1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(1, 0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(1, 1, item)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)

        self.retranslateUi(TableKeyBindings)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TableKeyBindings.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TableKeyBindings.reject)
        QtCore.QMetaObject.connectSlotsByName(TableKeyBindings)

    def retranslateUi(self, TableKeyBindings):
        TableKeyBindings.setWindowTitle(_translate("TableKeyBindings", "Change keybindings", None))
        TableKeyBindings.setWhatsThis(_translate("TableKeyBindings", "Here you can change the keybindings of the various functions provided by Power Format Pack.", None))
        self.tableWidget.setSortingEnabled(True)
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("TableKeyBindings", "New Row", None))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("TableKeyBindings", "New Row", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("TableKeyBindings", "Action", None))
        item.setToolTip(_translate("TableKeyBindings", "The name of the action offered by Power Format Pack.", None))
        item.setWhatsThis(_translate("TableKeyBindings", "The name of the function offered by Power Format Pack.", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("TableKeyBindings", "Keybinding", None))
        item.setToolTip(_translate("TableKeyBindings", "The keybinding associated with the action.", None))
        item.setWhatsThis(_translate("TableKeyBindings", "The keybinding associated with the action.", None))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("TableKeyBindings", "00", None))
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("TableKeyBindings", "10", None))
        item = self.tableWidget.item(1, 0)
        item.setText(_translate("TableKeyBindings", "01", None))
        item = self.tableWidget.item(1, 1)
        item.setText(_translate("TableKeyBindings", "11", None))
        self.tableWidget.setSortingEnabled(__sortingEnabled)

