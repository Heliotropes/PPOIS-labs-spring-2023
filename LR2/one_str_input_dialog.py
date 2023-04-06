# -*- coding: utf-8 -*-
from typing import NoReturn

# Author: Vodohleb04
# Form implementation generated from reading ui file 'oneStrInputDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

from library import SearchRemoveBy
from mode import Mode


class Ui_oneStrParameterDialog(object):

    def setupUi(self, ui_dialog, oneStrParameterDialog, data_controller, icon_file, parameter_name: str, mode: Mode,
                buffer=None):
        self._multyparam = True if isinstance(buffer, dict) else False
        self._mode = mode
        oneStrParameterDialog.setObjectName("oneStrParameterDialog")
        oneStrParameterDialog.resize(373, 92)
        oneStrParameterDialog.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(icon_file), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        oneStrParameterDialog.setWindowIcon(icon)
        oneStrParameterDialog.setStyleSheet("background-color: rgb(255, 225, 230);")
        self.dialogButtonBox = QtWidgets.QDialogButtonBox(oneStrParameterDialog)
        self.dialogButtonBox.setGeometry(QtCore.QRect(200, 50, 171, 32))
        self.dialogButtonBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.dialogButtonBox.setStyleSheet("background-color: rgb(199, 214, 255);")
        self.dialogButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.dialogButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.dialogButtonBox.setObjectName("dialogButtonBox")
        self.inputLine = QtWidgets.QLineEdit(oneStrParameterDialog)
        self.inputLine.setGeometry(QtCore.QRect(0, 0, 371, 41))
        self.inputLine.setStyleSheet("background-color: rgb(199, 214, 255);")
        self.inputLine.setInputMask("")
        self.inputLine.setText("")
        self.inputLine.setClearButtonEnabled(False)
        self.inputLine.setObjectName("inputLine")
        self.retranslateUi(oneStrParameterDialog, parameter_name)
        self.dialogButtonBox.accepted.connect(oneStrParameterDialog.accept)
        self.dialogButtonBox.rejected.connect(oneStrParameterDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(oneStrParameterDialog)
        if self._multyparam:
            self.connect_multyparam_accepted(ui_dialog, oneStrParameterDialog, data_controller, buffer)
        else:
            self.connect_accepted(ui_dialog, oneStrParameterDialog, data_controller)

    def retranslateUi(self, oneStrParameterDialog, parameter_name: str):
        _translate = QtCore.QCoreApplication.translate
        oneStrParameterDialog.setWindowTitle(_translate("oneStrParameterDialog", f"Ввод параметра \""
                                                                                 f"{parameter_name}\""))
        self.inputLine.setPlaceholderText(_translate("oneStrParameterDialog", f"Введите значение для параметра \""
                                                                              f"{parameter_name}\""))

    def connect_accepted(self, ui_dialog, oneStrParameterDialog, data_controller) -> NoReturn:
        if self._mode == Mode.SEARCH_MODE:
            oneStrParameterDialog.accepted.connect(lambda: self._connect_accepted_search(
                ui_search_dialog=ui_dialog,
                data_controller=data_controller))
        elif self._mode == Mode.REMOVE_MODE:
            oneStrParameterDialog.accepted.connect(
                lambda: self._remove_agreement(ui_dialog, oneStrParameterDialog, data_controller))

    def _remove_agreement(self, ui_dialog, oneStrParameterDialog, data_controller) -> NoReturn:
        result = QtWidgets.QMessageBox.question(
            oneStrParameterDialog,
            "Подтвердите удаление",
            "Вы действительно хотите удалить данные из таблицы?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No)
        if result == QtWidgets.QMessageBox.Yes:
            data_controller.one_str_param_complete_remove(ui_dialog, param_to_remove=self.inputLine.text())

    def connect_multyparam_accepted(self, ui_dialog, oneStrParameterDialog, data_controller, buffer) -> NoReturn:
        oneStrParameterDialog.accepted.connect(lambda: self._multyparam_accepted(
            ui_dialog=ui_dialog,
            oneStrParameterDialog=oneStrParameterDialog,
            data_controller=data_controller,
            buffer=buffer))

    def _connect_accepted_search(self, ui_search_dialog, data_controller) -> NoReturn:
        ui_search_dialog.dialogButtonBox.button(ui_search_dialog.dialogButtonBox.Ok).setEnabled(False)
        data_controller.one_str_param_complete_search(
            ui_search_dialog=ui_search_dialog,
            param_to_search=self.inputLine.text())

    def _multyparam_accepted(self, ui_dialog, oneStrParameterDialog, data_controller, buffer) -> NoReturn:
        if self.inputLine.text() == "":
            data_controller.dialog_input_error("Ничего не было подано на ввод")
            oneStrParameterDialog.reject()
        else:
            buffer["publishing_house"] = self.inputLine.text()
            buffer["required_amount"] -= 1
            if buffer["required_amount"] == 0:
                if self._mode == Mode.SEARCH_MODE:
                    self._multyparam_accepted_search(ui_dialog, data_controller, buffer)
                elif self._mode == Mode.REMOVE_MODE:
                    result = QtWidgets.QMessageBox.question(
                        oneStrParameterDialog,
                        "Подтвердите удаление",
                        "Вы действительно хотите удалить данные из таблицы?",
                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                        QtWidgets.QMessageBox.No)
                    if result == QtWidgets.QMessageBox.Yes:
                        self._multyparam_accepted_remove(ui_dialog, data_controller, buffer)

    @staticmethod
    def _multyparam_accepted_search(ui_search_dialog, data_controller, buffer) -> NoReturn:
        ui_search_dialog.found_books = data_controller.lib.search_for_books(SearchRemoveBy.PUBLISHING_HOUSE_AND_AUTHORS,
                                                                            publishing_house=buffer["publishing_house"],
                                                                            authors=buffer["authors"])
        data_controller.one_str_param_complete_search(ui_search_dialog,
                                                      buffer,
                                                      multyparam=True)
        ui_search_dialog.dialogButtonBox.button(ui_search_dialog.dialogButtonBox.Ok).setEnabled(False)

    @staticmethod
    def _multyparam_accepted_remove(ui_main_window, data_controller, buffer) -> NoReturn:
        data_controller.one_str_param_complete_remove(ui_main_window, buffer, multyparam=True)