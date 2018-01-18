# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'keysequencedialog.ui'
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

class Ui_KeySequenceDialog(object):
    def setupUi(self, KeySequenceDialog):
        KeySequenceDialog.setObjectName(_fromUtf8("KeySequenceDialog"))
        KeySequenceDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        KeySequenceDialog.resize(350, 150)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(KeySequenceDialog.sizePolicy().hasHeightForWidth())
        KeySequenceDialog.setSizePolicy(sizePolicy)
        KeySequenceDialog.setMinimumSize(QtCore.QSize(350, 150))
        KeySequenceDialog.setMaximumSize(QtCore.QSize(350, 150))
        KeySequenceDialog.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        KeySequenceDialog.setWindowTitle(_fromUtf8("Change key combination"))
        KeySequenceDialog.setModal(True)
        self.label = QtGui.QLabel(KeySequenceDialog)
        self.label.setGeometry(QtCore.QRect(10, 20, 331, 101))
        self.label.setMinimumSize(QtCore.QSize(331, 101))
        self.label.setMaximumSize(QtCore.QSize(331, 101))
        self.label.setText(_fromUtf8("<html><head/><body><p align=\"center\">Press the key combination you want<br/>to associate with this action.</p></body></html>"))
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(KeySequenceDialog)
        QtCore.QMetaObject.connectSlotsByName(KeySequenceDialog)

    def retranslateUi(self, KeySequenceDialog):
        pass

