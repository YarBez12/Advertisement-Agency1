from PyQt5 import QtWidgets, uic
from typing import Tuple, Optional, List, Any
from PyQt5.QtCore import QDate, QTimer
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

import InitialData
from Controllers import AddAdvertisementWindowController, AddCampaignWindowController, AddClientWindowController, \
    TablesWindowController
from DatabaseController import DatabaseController
from InitialData import *
from Models import *


class AddAdvertisementWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("AddAdvertisementWindow.ui", self)
        self.sendDateEdit.setCalendarPopup(True)
        self.formatComboBox.addItems(ADVERTISEMENT_FORMATS)
        self.languageComboBox.addItems(LANGUAGES)
        self.addAtachmentButton.clicked.connect(self.choose_file)
        self.saveButton.clicked.connect(self.save)
        self.cancelButton.clicked.connect(self.reject)
        self.__controller = AddAdvertisementWindowController(self)
        self.resetButton.clicked.connect(self.reset_data)
        self.campaignComboBox.addItems([campaign.name for campaign in InitialData.Campaigns.get_items()])
        self.reset_data()

    def choose_file(self) -> None:
        options = QtWidgets.QFileDialog.DontUseNativeDialog
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Choose your file", "", "All Files (*.*)",
                                                             options=options)
        self.__controller.update_attachment_line_edit(file_path)

    def save(self) -> None:
        validation = self.__controller.validate_window()
        if not validation:
            QtWidgets.QMessageBox.warning(
                self,
                "Unfilled fields",
                "Please fill in all necessary fields"
            )
        else:
            self.accept()

    def get_data(self) -> Optional[Advertisement]:
        return self.__controller.get_data()

    def set_data(self, advertisement: Advertisement) -> None:
        self.__controller.set_data(advertisement)

    def reset_data(self):
        self.__controller.reset_data()

    def set_campaign_name(self, campaign_name: int):
        self.__controller.set_campaign_name(campaign_name)


class AddCampaignWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("AddCampaignWindow.ui", self)
        self.startDateEdit.setCalendarPopup(True)
        self.endDateEdit.setCalendarPopup(True)
        self.__controller = AddCampaignWindowController(self)
        self.companyComboBox.addItems([client.company_name for client in InitialData.Clients.get_items()])
        self.reset_data()
        self.saveButton.clicked.connect(self.save)
        self.cancelButton.clicked.connect(self.reject)
        self.resetButton.clicked.connect(self.reset_data)

    def save(self) -> None:
        validation = self.__controller.validate_window()
        if not validation:
            QtWidgets.QMessageBox.warning(
                self,
                "Unfilled fields",
                "Please fill in all necessary fields"
            )
        else:
            self.accept()

    def get_data(self):
        return self.__controller.get_data()

    def reset_data(self) -> None:
        self.__controller.reset_data()

    def set_data(self, campaign: Campaign) -> None:
        self.__controller.set_data(campaign)

class AddClientWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("AddClientWindow.ui", self)
        self.typeComboBox.addItems(["Individual", "Company"])
        self.areaComboBox.addItems(CLIENT_AREAS)
        self.__controller = AddClientWindowController(self)
        self.saveButton.clicked.connect(self.save)
        self.cancelButton.clicked.connect(self.reject)
        self.resetButton.clicked.connect(self.reset_data)

    def save(self) -> None:
        validation = self.__controller.validate_window()
        if not validation:
            QtWidgets.QMessageBox.warning(
                self,
                "Unfilled fields",
                "Please fill in all necessary fields"
            )
        else:
            self.accept()

    def get_data(self) -> Optional[Client]:
        return self.__controller.get_data()

    def reset_data(self) -> None:
        self.__controller.reset_data()

    def set_data(self, client) -> None:
        self.__controller.set_data(client)


class TablesWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        # super().__init__()
        # uic.loadUi("TablesWindow.ui", self)
        # self.addButton.clicked.connect(self.open_item_dialog)
        # self.editButton.clicked.connect(lambda : self.open_item_dialog(True)) #1
        # self.removeButton.clicked.connect(self.remove_item)
        # self.firstButton.clicked.connect(self.navigate_first)
        # self.previousButton.clicked.connect(self.navigate_previous)
        # self.nextButton.clicked.connect(self.navigate_next)
        # self.lastButton.clicked.connect(self.navigate_last)
        # self.actionGoClients.triggered.connect(lambda: self.update_table(InitialData.Clients))
        # self.actionGoCampaigns.triggered.connect(lambda: self.update_table(InitialData.Campaigns))
        # self.actionGoAdvertisements.triggered.connect(lambda: self.update_table(InitialData.Advertisements))
        # self.actionAdd.triggered.connect(self.open_item_dialog)
        # self.actionUpdate.triggered.connect(lambda : self.open_item_dialog(True)) #2
        # self.actionDelete.triggered.connect(self.remove_item)
        # self.current_data = InitialData.Clients
        # self.update_table(self.current_table)

        super().__init__()
        uic.loadUi("TablesWindow.ui", self)
        self.__controller = TablesWindowController(self)
        self.addButton.clicked.connect(self.open_item_dialog)
        self.editButton.clicked.connect(lambda: self.open_item_dialog(True))
        self.removeButton.clicked.connect(self.remove_item)
        self.firstButton.clicked.connect(self.__controller.navigate_first)
        self.previousButton.clicked.connect(self.__controller.navigate_previous)
        self.nextButton.clicked.connect(self.__controller.navigate_next)
        self.lastButton.clicked.connect(self.__controller.navigate_last)
        self.actionGoClients.triggered.connect(lambda: self.__controller.update_table(InitialData.Clients))
        self.actionGoCampaigns.triggered.connect(lambda: self. __controller.update_table(InitialData.Campaigns))
        self.actionGoAdvertisements.triggered.connect(lambda: self.__controller.update_table(InitialData.Advertisements))
        self.actionAdd.triggered.connect(self.open_item_dialog)
        self.actionUpdate.triggered.connect(lambda: self.open_item_dialog(True))
        self.actionDelete.triggered.connect(self.remove_item)
        self.__controller.update_table(self.__controller.current_data)

    def remove_item(self) -> None:
        selected_row = self.dataTableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "No data", "Please select a row to delete")
            return

        table_name = self.__controller.current_data.get_str_models_name()
        key_columns = {
            "Clients": "company_name",
            "Campaigns": "campaign_id",
            "Advertisements": "advertisement_id"
        }
        key_value = self.dataTableWidget.item(selected_row, 0).text()
        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirmation",
            f"Are you sure you want to delete item with {key_columns[table_name]} = {key_value}?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            deleted_key = self.__controller.remove_item(selected_row)
            if deleted_key:
                self.__controller.update_table(self.__controller.current_data)

    # def remove_item(self) -> None:
    #     table_name = self.current_data.get_str_models_name()
    #     key_columns = {
    #         "Clients" : "company_name",
    #         "Campaigns" : "campaign_id",
    #         "Advertisements" : "advertisement_id"
    #     }
    #     selected_row = self.dataTableWidget.currentRow()
    #     if selected_row != -1:
    #         key_value = self.dataTableWidget.item(selected_row, 0).text()
    #         reply = QtWidgets.QMessageBox.question(self,
    #             "Confirmation",
    #             f"Are you sure you want to delete item with {key_columns[table_name]} = {key_value}",
    #             QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
    #         )
    #         if reply == QtWidgets.QMessageBox.Yes:
    #             remove_item = next(
    #                 item for item in self.current_data.get_items() if str(item.GetData()[1][0]) == key_value)
    #             self.current_data.remove(remove_item)
    #             self.update_table(self.current_data)
    #         else:
    #             return

    # def open_item_dialog(self, edit : bool = False) -> None:
    #     dialogs = {
    #         "Clients" : AddClientWindow,
    #         "Campaigns" : AddCampaignWindow,
    #         "Advertisements" : AddAdvertisementWindow
    #     }
    #     table_name = self.current_data.get_str_models_name()
    #     dialog_class = dialogs.get(table_name)
    #     if not dialog_class:
    #         return
    #     if edit:
    #         selected_row = self.dataTableWidget.currentRow();
    #         if selected_row == -1:
    #             QtWidgets.QMessageBox.warning(self, "No data", "Please select a row to edit")
    #             return
    #         edit_item = self.current_data[selected_row]
    #         dialog = dialog_class(self)
    #         dialog.set_data(edit_item)
    #     else:
    #         dialog = dialog_class(self)
    #     if dialog.exec_() == QtWidgets.QDialog.Accepted:
    #         data = dialog.get_data()
    #         if data:
    #             if edit:
    #                 self.current_data.update(selected_row, data)
    #             else:
    #                 self.current_data.add(data)
    #             self.update_table(self.current_data)

    def open_item_dialog(self, edit: bool = False) -> None:
        dialogs = {
            "Clients": AddClientWindow,
            "Campaigns": AddCampaignWindow,
            "Advertisements": AddAdvertisementWindow
        }
        table_name = self.__controller.current_data.get_str_models_name()
        dialog_class = dialogs.get(table_name)
        if not dialog_class:
            return
        dialog = dialog_class(self)
        if edit:
            selected_row = self.dataTableWidget.currentRow()
            if selected_row == -1:
                QtWidgets.QMessageBox.warning(self, "No data", "Please select a row to edit")
                return
            edit_item = self.__controller.get_item_for_edit(selected_row)
            if not edit_item:
                QtWidgets.QMessageBox.warning(self, "Error", "Could not retrieve item for editing")
                return
            dialog.set_data(edit_item)

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            data = dialog.get_data()
            if data:
                self.__controller.save_item(data, edit, self.dataTableWidget.currentRow() if edit else None)
                self.__controller.update_table(self.__controller.current_data)
