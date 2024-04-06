# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test.ui'
##
## Created by: Qt User Interface Compiler version 5.15.8
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *  # type: ignore
from PyQt5.QtGui import *  # type: ignore
from PyQt5.QtWidgets import *  # type: ignore


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName("Form")
        Form.resize(400, 321)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName("label")

        self.horizontalLayout.addWidget(self.label)

        self.lineEdit_objfile = QLineEdit(Form)
        self.lineEdit_objfile.setObjectName("lineEdit_objfile")

        self.horizontalLayout.addWidget(self.lineEdit_objfile)

        self.toolButton_objfile = QToolButton(Form)
        self.toolButton_objfile.setObjectName("toolButton_objfile")

        self.horizontalLayout.addWidget(self.toolButton_objfile)

        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName("label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.lineEdit_texturedir = QLineEdit(Form)
        self.lineEdit_texturedir.setObjectName("lineEdit_texturedir")

        self.horizontalLayout_2.addWidget(self.lineEdit_texturedir)

        self.toolButton_texturedir = QToolButton(Form)
        self.toolButton_texturedir.setObjectName("toolButton_texturedir")

        self.horizontalLayout_2.addWidget(self.toolButton_texturedir)

        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName("label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.lineEdit_output = QLineEdit(Form)
        self.lineEdit_output.setObjectName("lineEdit_output")

        self.horizontalLayout_3.addWidget(self.lineEdit_output)

        self.toolButton_output = QToolButton(Form)
        self.toolButton_output.setObjectName("toolButton_output")

        self.horizontalLayout_3.addWidget(self.toolButton_output)

        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", "Form", None))
        self.label.setText(QCoreApplication.translate("Form", "objfile", None))
        self.lineEdit_objfile.setText(QCoreApplication.translate("Form", "/home/rapa/myproject_MATE/test/obj/1.obj", None))
        self.toolButton_objfile.setText(QCoreApplication.translate("Form", "...", None))
        self.label_2.setText(QCoreApplication.translate("Form", "texture", None))
        self.lineEdit_texturedir.setText(
            QCoreApplication.translate("Form", "/home/rapa/myproject_MATE/test/texture/1", None)
        )
        self.toolButton_texturedir.setText(QCoreApplication.translate("Form", "...", None))
        self.label_3.setText(QCoreApplication.translate("Form", "output", None))
        self.lineEdit_output.setText(QCoreApplication.translate("Form", "/home/rapa/myproject_MATE/1", None))
        self.toolButton_output.setText(QCoreApplication.translate("Form", "...", None))

    # retranslateUi
