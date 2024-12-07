from datetime import datetime

from PyQt5 import QtWidgets, uic
from typing import Tuple, Optional, List, Any
from PyQt5.QtCore import QDate, QTimer
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QFileDialog
import xlsxwriter
from fpdf import FPDF
import pandas as pd

import InitialData
from Controllers import *
from DatabaseController import DatabaseController
from Models import *

class UserViewWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, user=None):
        super().__init__(parent)
        uic.loadUi("UserViewWindow.ui", self)
        self.user = user
        self.viewed_messages = set()
        self.platformsListWidget.itemDoubleClicked.connect(self.show_ad_for_platform)
        self.advertisementsListWidget.itemDoubleClicked.connect(self.show_ad_details)
        self.load_platforms()
        self.actionLogout.triggered.connect(self.go_back)

    def go_back(self):
        self.parent().show()
        self.close()

    def load_platforms(self):
        self.platformsListWidget.clear()
        if not self.user or not self.user.segment_id:
            QtWidgets.QMessageBox.warning(self, "Error", "User is not associated with any audience segment.")
            return
        segment_id = self.user.segment_id
        associated_platforms = [
            sp for sp in InitialData.SegmentPlatforms.get_items()
            if sp.segment_id == segment_id
        ]
        platform_ids = [sp.platform_id for sp in associated_platforms]
        platforms = [
            platform for platform in InitialData.MediaPlatforms.get_items()
            if platform.platform_id in platform_ids
        ]
        for platform in platforms:
            item = QtWidgets.QListWidgetItem(platform.platform_name)
            item.setData(Qt.UserRole, platform.platform_id)
            self.platformsListWidget.addItem(item)

    def show_ad_for_platform(self, item):
        self.advertisementsListWidget.clear()
        platform_id = item.data(Qt.UserRole)
        advertisements = [
            ad for ad in InitialData.Advertisements.get_items()
            if ad.platform_id == platform_id
        ]
        for ad in advertisements:
            if ad.advertisement_id not in self.viewed_messages:
                ad.views = (ad.views or 0) + 1
                self.viewed_messages.add(ad.advertisement_id)
        for ad in advertisements:
            ad_item = QtWidgets.QListWidgetItem(ad.topic)
            ad_item.setData(Qt.UserRole, ad.advertisement_id)
            self.advertisementsListWidget.addItem(ad_item)

    def show_ad_details(self, item):
        advertisement_id = item.data(Qt.UserRole)
        advertisement = next(
            (ad for ad in InitialData.Advertisements.get_items() if ad.advertisement_id == advertisement_id), None
        )
        if not advertisement:
            QtWidgets.QMessageBox.warning(self, "Error", "Could not find the selected advertisement.")
            return
        advertisement.clicks = (advertisement.clicks or 0) + 1
        dialog = QtWidgets.QMessageBox(self)
        dialog.setWindowTitle("Message Details")
        dialog.setText(f"Message Text: {advertisement.text}")
        dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
        dialog.exec_()


class AddAdvertisementWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("AddAdvertisementWindow.ui", self)
        self.sendDateEdit.setCalendarPopup(True)
        self.formatComboBox.addItems(InitialData.ADVERTISEMENT_FORMATS)
        self.languageComboBox.addItems(InitialData.LANGUAGES)
        self.addAtachmentButton.clicked.connect(self.choose_file)
        self.saveButton.clicked.connect(self.save)
        self.cancelButton.clicked.connect(self.reject)
        self.__controller = AddAdvertisementWindowController(self)
        self.reset_data()
        self.dateButton.clicked.connect(self.toggle_time)
        self.languageButton.clicked.connect(self.toggle_language)
        self.campaignButton.clicked.connect(self.toggle_campaign)
        self.platformButton.clicked.connect(self.toggle_platform)
        self.resetButton.clicked.connect(self.reset_data)
        self.campaignComboBox.addItems([campaign.campaign_name for campaign in InitialData.Campaigns.get_items() if campaign.campaign_name])
        self.platformComboBox.addItems([platform.platform_name for platform in InitialData.MediaPlatforms.get_items()])
        self.reset_data()

    def toggle_time(self) -> None:
        if self.sendDateEdit.isEnabled():
            self.sendDateEdit.setEnabled(False)
            self.dateButton.setText("Add time")
        else:
            self.sendDateEdit.setEnabled(True)
            self.dateButton.setText("Remove time")

    def toggle_language(self) -> None:
        if self.languageComboBox.isEnabled():
            self.languageComboBox.setEnabled(False)
            self.languageButton.setText("Add language")
        else:
            self.languageComboBox.setEnabled(True)
            self.languageButton.setText("Remove language")

    def toggle_campaign(self) -> None:
        if self.languageComboBox.isEnabled():
            self.campaignComboBox.setEnabled(False)
            self.campaignButton.setText("Add campaign")
        else:
            self.campaignComboBox.setEnabled(True)
            self.campaignButton.setText("Remove campaign")

    def toggle_platform(self) -> None:
        if self.platformComboBox.isEnabled():
            self.platformComboBox.setEnabled(False)
            self.platformButton.setText("Add platform")
        else:
            self.platformComboBox.setEnabled(True)
            self.platformButton.setText("Remove platform")


    def choose_file(self) -> None:
        options = QtWidgets.QFileDialog.DontUseNativeDialog
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Choose your file", "", "All Files (*.*)",
                                                             options=options)
        self.__controller.update_attachment_line_edit(file_path)

    def save(self) -> None:
        validation = self.__controller.validate_window()
        if validation:
            QtWidgets.QMessageBox.warning(
                self,
                "Invalid data",
                validation
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

    def set_platform_name(self, platform_name: int):
        self.__controller.set_platform_name(platform_name)


class AddPlatformWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("AddPlatformWindow.ui", self)
        self.formatComboBox.addItems(InitialData.ADVERTISEMENT_FORMATS)
        self.typeComboBox.addItems(InitialData.PLATFORM_TYPES)
        self.saveButton.clicked.connect(self.save)
        self.cancelButton.clicked.connect(self.reject)
        self.__controller = AddPlatformWindowController(self)
        self.typeButton.clicked.connect(self.toggle_type)
        self.formatButton.clicked.connect(self.toggle_format)
        self.sizeButton.clicked.connect(self.toggle_size)
        self.budgetAllocationButton.clicked.connect(self.toggle_budget_allocation)
        self.reset_data()
        self.resetButton.clicked.connect(self.reset_data)
        self.budgetAllocationLabel.hide()
        self.budgetAllocationSpinBox.hide()
        self.reset_data()

    def toggle_budget_allocation(self) -> None:
        if self.budgetAllocationSpinBox.isEnabled():
            self.budgetAllocationSpinBox.setEnabled(False)
            self.budgetAllocationButton.setText("Add budget")
        else:
            self.budgetAllocationSpinBox.setEnabled(True)
            self.budgetAllocationButton.setText("Remove budget")

    def toggle_type(self) -> None:
        if self.typeComboBox.isEnabled():
            self.typeComboBox.setEnabled(False)
            self.typeButton.setText("Add type")
        else:
            self.typeComboBox.setEnabled(True)
            self.typeButton.setText("Remove type")

    def toggle_format(self) -> None:
        if self.formatComboBox.isEnabled():
            self.formatComboBox.setEnabled(False)
            self.formatButton.setText("Add format")
        else:
            self.formatComboBox.setEnabled(True)
            self.formatButton.setText("Remove format")

    def toggle_size(self) -> None:
        if self.audienceSpinBox.isEnabled():
            self.audienceSpinBox.setEnabled(False)
            self.sizeButton.setText("Add size")
        else:
            self.audienceSpinBox.setEnabled(True)
            self.sizeButton.setText("Remove size")


    def save(self) -> None:
        validation = self.__controller.validate_window()
        if validation:
            QtWidgets.QMessageBox.warning(
                self,
                "Unfilled fields",
                validation
            )
        else:
            self.accept()

    def get_data(self) -> Optional[Advertisement]:
        return self.__controller.get_data()

    def set_data(self, platform) -> None:
        self.__controller.set_data(platform)

    def reset_data(self):
        self.__controller.reset_data()

    def show_budget_allocation(self):
        self.budgetAllocationLabel.show()
        self.budgetAllocationSpinBox.show()
        self.budgetAllocationButton.show()


    def set_budget_allocation(self, value):
        self.show_budget_allocation()
        if value is not None:
            self.budgetAllocationSpinBox.setValue(value)
            self.budgetAllocationSpinBox.setEnabled(True)
            self.budgetAllocationButton.setText("Remove budget")
        else:
            self.budgetAllocationSpinBox.setEnabled(False)
            self.budgetAllocationButton.setText("Add budget")

    def get_budget_allocation(self):
        return self.budgetAllocationSpinBox.value() if self.budgetAllocationSpinBox.isEnabled() else None

class AddSegmentWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("AddSegmentWindow.ui", self)
        self.genderComboBox.addItems(["Male", "Female", "Other"])
        self.locationComboBox.addItems(InitialData.LOCATIONS)
        self.languageComboBox.addItems(InitialData.LANGUAGES)
        self.deviceComboBox.addItems(InitialData.DEVICES)
        self.saveButton.clicked.connect(self.save)
        self.cancelButton.clicked.connect(self.reject)
        self.__controller = AddSegmentWindowController(self)
        self.reset_data()
        self.locationButton.clicked.connect(self.toggle_location)
        self.deviceButton.clicked.connect(self.toggle_device)
        self.resetButton.clicked.connect(self.reset_data)
        self.reset_data()

    def toggle_location(self) -> None:
        if self.locationComboBox.isEnabled():
            self.locationComboBox.setEnabled(False)
            self.locationButton.setText("Add location")
        else:
            self.locationComboBox.setEnabled(True)
            self.locationButton.setText("Remove location")

    def toggle_device(self) -> None:
        if self.deviceComboBox.isEnabled():
            self.deviceComboBox.setEnabled(False)
            self.deviceButton.setText("Add device")
        else:
            self.deviceComboBox.setEnabled(True)
            self.deviceButton.setText("Remove device")

    def save(self) -> None:
        validation = self.__controller.validate_window()
        if validation:
            QtWidgets.QMessageBox.warning(
                self,
                "Unfilled fields",
                validation
            )
        else:
            self.accept()

    def get_data(self) -> Optional[Advertisement]:
        return self.__controller.get_data()

    def set_data(self, segment) -> None:
        self.__controller.set_data(segment)

    def reset_data(self):
        self.__controller.reset_data()


class AddUserWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("AddUserWindow.ui", self)
        self.genderComboBox.addItems(["Male", "Female", "Other"])
        self.countryComboBox.addItems(InitialData.LOCATIONS)
        self.createdDateEdit.setCalendarPopup(True)
        self.lastPurchaseDateEdit.setCalendarPopup(True)
        self.segmentComboBox.addItems([segment.segment_name for segment in InitialData.AudienceSegments.get_items() if segment.segment_name])
        self.saveButton.clicked.connect(self.save)
        self.cancelButton.clicked.connect(self.reject)
        self.__controller = AddUserWindowController(self)
        self.reset_data()
        self.dateButton.clicked.connect(self.toggle_date)
        self.segmentButton.clicked.connect(self.toggle_segment)
        self.resetButton.clicked.connect(self.reset_data)
        self.reset_data()

    def toggle_date(self) -> None:
        if self.lastPurchaseDateEdit.isEnabled():
            self.lastPurchaseDateEdit.setEnabled(False)
            self.dateButton.setText("Add date")
        else:
            self.lastPurchaseDateEdit.setEnabled(True)
            self.dateButton.setText("Remove date")

    def toggle_segment(self) -> None:
        if self.segmentComboBox.isEnabled():
            self.segmentComboBox.setEnabled(False)
            self.segmentButton.setText("Add segment")
        else:
            self.segmentComboBox.setEnabled(True)
            self.segmentButton.setText("Remove segment")

    def save(self) -> None:
        validation = self.__controller.validate_window()
        if validation:
            QtWidgets.QMessageBox.warning(
                self,
                "Unfilled fields",
                validation
            )
        else:
            self.accept()

    def get_data(self) -> Optional[Advertisement]:
        return self.__controller.get_data()

    def set_data(self, user) -> None:
        self.__controller.set_data(user)

    def reset_data(self):
        self.__controller.reset_data()

    def set_segment_name(self, segment_name: int):
        self.__controller.set_segment_name(segment_name)



class AddCampaignWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("AddCampaignWindow.ui", self)
        self.startDateEdit.setCalendarPopup(True)
        self.endDateEdit.setCalendarPopup(True)
        self.startDateButton.clicked.connect(self.toggle_start_date)
        self.endDateButton.clicked.connect(self.toggle_end_date)
        self.budgetButton.clicked.connect(self.toggle_budget)
        self.budgetAllocationButton.clicked.connect(self.toggle_budget_allocation)
        self.budgetAllocationLabel.hide()
        self.budgetAllocationSpinBox.hide()
        self.budgetAllocationButton.hide()
        self.__controller = AddCampaignWindowController(self)
        self.companyComboBox.addItems([client.company_name for client in InitialData.Clients.get_items()])
        self.reset_data()
        self.saveButton.clicked.connect(self.save)
        self.cancelButton.clicked.connect(self.reject)
        self.resetButton.clicked.connect(self.reset_data)

    def save(self) -> None:
        validation = self.__controller.validate_window()
        if validation:
            QtWidgets.QMessageBox.warning(
                self,
                "Unfilled fields",
                validation
            )
        else:
            self.accept()

    def get_data(self):
        return self.__controller.get_data()

    def reset_data(self) -> None:
        self.__controller.reset_data()
        self.budgetSpinBox.setEnabled(False)
        self.startDateEdit.setEnabled(False)
        self.endDateEdit.setEnabled(False)
        self.budgetAllocationSpinBox.setEnabled(False)
        self.startDateButton.setText("Add Date")
        self.endDateButton.setText("Add Date")
        self.budgetButton.setText("Add budget")
        self.budgetAllocationButton.setText("Add budget")

    def set_data(self, campaign: Campaign) -> None:
        self.__controller.set_data(campaign)
        self.startDateButton.setText("Remove Date" if campaign.start_date else "Add Date")
        self.endDateButton.setText("Remove Date" if campaign.end_date else "Add Date")
        self.budgetButton.setText("Remove budget" if campaign.budget is not None else "Add budget")

    def toggle_start_date(self) -> None:
        if self.startDateEdit.isEnabled():
            self.startDateEdit.setEnabled(False)
            self.startDateButton.setText("Add Date")
        else:
            self.startDateEdit.setEnabled(True)
            self.startDateButton.setText("Remove Date")

    def toggle_end_date(self) -> None:
        if self.endDateEdit.isEnabled():
            self.endDateEdit.setEnabled(False)
            self.endDateButton.setText("Add Date")
        else:
            self.endDateEdit.setEnabled(True)
            self.endDateButton.setText("Remove Date")

    def toggle_budget(self) -> None:
        if self.budgetSpinBox.isEnabled():
            self.budgetSpinBox.setEnabled(False)
            self.budgetButton.setText("Add budget")
        else:
            self.budgetSpinBox.setEnabled(True)
            self.budgetButton.setText("Remove budget")

    def toggle_budget_allocation(self) -> None:
        if self.budgetAllocationSpinBox.isEnabled():
            self.budgetAllocationSpinBox.setEnabled(False)
            self.budgetAllocationButton.setText("Add budget")
        else:
            self.budgetAllocationSpinBox.setEnabled(True)
            self.budgetAllocationButton.setText("Remove budget")

    def set_client_name(self, client_name):
        self.companyComboBox.setCurrentText(str(client_name))
        self.companyComboBox.setEnabled(False)

    def show_budget_allocation(self):
        self.budgetAllocationLabel.show()
        self.budgetAllocationSpinBox.show()
        self.budgetAllocationButton.show()

    def set_budget_allocation(self, value):
        self.show_budget_allocation()
        if value is not None:
            self.budgetAllocationSpinBox.setValue(value)
            self.budgetAllocationSpinBox.setEnabled(True)
            self.budgetAllocationButton.setText("Remove budget")
        else:
            self.budgetAllocationSpinBox.setEnabled(False)
            self.budgetAllocationButton.setText("Add budget")

    def get_budget_allocation(self):
        return self.budgetAllocationSpinBox.value() if self.budgetAllocationSpinBox.isEnabled() else None


class AddClientWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("AddClientWindow.ui", self)
        self.typeComboBox.addItems(["Individual", "Company"])
        self.areaComboBox.addItems(InitialData.CLIENT_AREAS)
        self.__controller = AddClientWindowController(self)
        self.reset_data()
        self.saveButton.clicked.connect(self.save)
        self.cancelButton.clicked.connect(self.reject)
        self.resetButton.clicked.connect(self.reset_data)
        self.budgetButton.clicked.connect(self.toggle_budget)

    def toggle_budget(self) -> None:
        if self.budgetSpinBox.isEnabled():
            self.budgetSpinBox.setEnabled(False)
            self.budgetButton.setText("Add budget")
        else:
            self.budgetSpinBox.setEnabled(True)
            self.budgetButton.setText("Remove budget")

    def save(self) -> None:
        validation = self.__controller.validate_window()
        if validation:
            QtWidgets.QMessageBox.warning(
                self,
                "Unfilled fields",
                validation
            )
        else:
            self.accept()

    def get_data(self) -> Optional[Client]:
        return self.__controller.get_data()

    def reset_data(self) -> None:
        self.__controller.reset_data()

    def set_data(self, client) -> None:
        self.__controller.set_data(client)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("MainWindow.ui", self)
        self.clientRadioButton.setChecked(True)
        self.loginButton.clicked.connect(self.go_next)

    def go_next(self):
        entered_email = self.emailLineEdit.text().strip()
        entered_password = self.passwordLineEdit.text().strip()
        if self.clientRadioButton.isChecked():
            appropriate_client = None
            for client in InitialData.Clients.get_items():
                if entered_email == client.email and entered_password == client.password:
                    appropriate_client = client
                    break
            if appropriate_client:
                window = ClientViewWindow(self, appropriate_client)
                self.hide()
                window.show()
            else:
                QtWidgets.QMessageBox.warning(self, "Invalid data", "Email or password is incorrect")
        elif self.userRadioButton.isChecked():
            appropriate_user = None
            for user in InitialData.Users.get_items():
                if entered_email == user.email and entered_password == user.password:
                    appropriate_user = user
                    break
            if appropriate_user:
                pass
                window = UserViewWindow(self, user)
                self.hide()
                window.show()
            else:
                QtWidgets.QMessageBox.warning(self, "Invalid data", "Email or password is incorrect")
        else:
            if entered_email == "admin@gmail.com" and entered_password == "ADMIN":
                window = TablesWindow(self)
                self.hide()
                window.show()
            else:
                QtWidgets.QMessageBox.warning(self, "Invalid data", "Email or password is incorrect")



class TablesWindow(QtWidgets.QMainWindow):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        uic.loadUi("TablesWindow.ui", self)
        self.__controller = TablesWindowController(self)
        self.addButton.clicked.connect(self.open_item_dialog)
        self.editButton.clicked.connect(lambda: self.open_item_dialog(True))
        self.removeButton.clicked.connect(self.remove_item)
        self.infoButton.clicked.connect(self.open_info_window)
        self.firstButton.clicked.connect(self.__controller.navigate_first)
        self.previousButton.clicked.connect(self.__controller.navigate_previous)
        self.nextButton.clicked.connect(self.__controller.navigate_next)
        self.lastButton.clicked.connect(self.__controller.navigate_last)
        self.actionGoClients.triggered.connect(lambda: self.__controller.update_table(InitialData.Clients))
        self.actionGoCampaigns.triggered.connect(lambda: self. __controller.update_table(InitialData.Campaigns))
        self.actionGoPlatforms.triggered.connect(lambda: self.__controller.update_table(InitialData.MediaPlatforms))
        self.actionGoSegments.triggered.connect(lambda: self.__controller.update_table(InitialData.AudienceSegments))
        self.actionGoUsers.triggered.connect(lambda: self.__controller.update_table(InitialData.Users))
        self.actionGoAdvertisements.triggered.connect(lambda: self.__controller.update_table(InitialData.Advertisements))
        self.actionAdd.triggered.connect(self.open_item_dialog)
        self.actionUpdate.triggered.connect(lambda: self.open_item_dialog(True))
        self.actionDelete.triggered.connect(self.remove_item)
        self.actionLogout.triggered.connect(self.go_back)
        self.actionCampaignsPlatforms.triggered.connect(self.generate_platform_campaign_report)
        self.sortButton.clicked.connect(self.open_sort_dialog)
        self.findButton.clicked.connect(self.open_find_dialog)
        self.filterButton.clicked.connect(self.open_filter_dialog)
        self.resetButton.clicked.connect(self.reset_editing)
        # self.sortButton.setVisible(False)
        # self.findButton.setVisible(False)
        # self.filterButton.setVisible(False)
        self.__controller.update_table(self.__controller.current_data)

    def reset_editing(self):
        self.__controller.find_criteria = None
        self.__controller.sort_criteria = None
        self.__controller.filter_criteria = None
        self.__controller.display_data = self.__controller.current_data
        self.__controller.update_table(self.__controller.current_data)
    def open_sort_dialog(self):
        sort_dialogs = {
            "Campaigns" : CampaignSortWindow,
            "Clients": ClientSortWindow
        }
        dialog = sort_dialogs.get(self.__controller.current_data.get_str_models_name(), None)
        if dialog:
            sort_dialog = dialog(self, self.__controller.sort_criteria)
        else:
            QtWidgets.QMessageBox.warning(self, "Unavailable function", "This button is unavailable")
            return
        # sort_dialog = CampaignSortWindow(self, self.__controller.sort_criteria)
        if sort_dialog.exec_() == QtWidgets.QDialog.Accepted:
            selected_option = sort_dialog.get_selected_option()
            # print(selected_option)
            if selected_option:
                self.__controller.sort_table(selected_option)

    def open_find_dialog(self):
        find_dialogs = {
            "Campaigns" : CampaignFindWindow,
            "Clients": ClientFindWindow
        }
        dialog = find_dialogs.get(self.__controller.current_data.get_str_models_name(), None)
        if dialog:
            find_dialog = dialog(self, self.__controller.find_criteria)
        else:
            QtWidgets.QMessageBox.warning(self, "Unavailable function", "This button is unavailable")
            return
        if find_dialog.exec_() == QtWidgets.QDialog.Accepted:
            search_criteria = find_dialog.get_search_criteria()
            # print(*search_criteria)
            if search_criteria:
                try:
                    self.__controller.find_items(search_criteria)
                except ValueError as e:
                    QtWidgets.QMessageBox.warning(self, "No data", str(e))

    def open_filter_dialog(self):
        filter_dialogs = {
            "Advertisements": AdvertisementFilterWindow,
            "Audience Segments": SegmentFilterWindow
        }
        dialog = filter_dialogs.get(self.__controller.current_data.get_str_models_name(), None)
        if dialog:
            filter_dialog = dialog(self, self.__controller.filter_criteria)
        else:
            QtWidgets.QMessageBox.warning(self, "Unavailable function", "This button is unavailable")
            return
        if filter_dialog.exec_() == QtWidgets.QDialog.Accepted:
            filter_criteria = filter_dialog.get_filter_criteria()
            if filter_criteria:
                try:
                    self.__controller.filter_items(filter_criteria)
                except ValueError as e:
                    QtWidgets.QMessageBox.warning(self, "No data", str(e))

    def remove_item(self) -> None:
        selected_row = self.dataTableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "No data", "Please select a row to delete")
            return

        table_name = self.__controller.current_data.get_str_models_name()
        key_columns = {
            "Clients": "company_name",
            "Campaigns": "campaign_id",
            "Advertisements": "advertisement_id",
            "Media Platforms": "platform_id",
            "Audience Segments": "segment_id",
            "Users": "email"
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
            # if deleted_key:
                # self.__controller.update_table(self.__controller.current_data)

    def open_item_dialog(self, edit: bool = False) -> None:
        dialogs = {
            "Clients": AddClientWindow,
            "Campaigns": AddCampaignWindow,
            "Advertisements": AddAdvertisementWindow,
            "Media Platforms": AddPlatformWindow,
            "Audience Segments": AddSegmentWindow,
            "Users": AddUserWindow
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
                # self.__controller.update_table(self.__controller.current_data)


    def open_info_window(self) -> None:
        windows = {
            "Clients": ClientWindow,
            "Campaigns": CampaignWindow,
            "Advertisements": AdvertisementWindow,
            "Media Platforms": PlatformWindow,
            "Audience Segments": SegmentWindow,
            "Users": UserWindow
        }
        table_name = self.__controller.current_data.get_str_models_name()
        window_class = windows.get(table_name)

        if not window_class:
            QtWidgets.QMessageBox.warning(self, "Error", f"No info window available for {table_name}.")
            return
        selected_row = self.dataTableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select an item to view details.")
            return
        selected_item = self.__controller.get_item_for_edit(selected_row)

        def update_callback():
            self.__controller.update_table(self.__controller.current_data)
        info_window = window_class(self, selected_item, update_callback)
        self.hide()
        info_window.show()

    def generate_platform_campaign_report(self):
        platforms = InitialData.MediaPlatforms.get_items()
        if not platforms:
            QtWidgets.QMessageBox.warning(self, "No Platforms", "No platforms found in the system.")
            return
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save Platform Campaign Report", "", "PDF Files (*.pdf)"
        )
        if not file_path:
            return
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(0, 10, "Platform Campaign Report", ln=True, align="C")
        pdf.ln(10)
        for platform in platforms:
            platform_campaigns = [
                cp.campaign_id for cp in InitialData.CampaignPlatforms.get_items()
                if cp.platform_id == platform.platform_id
            ]
            if not platform_campaigns:
                continue
            campaigns = [
                campaign for campaign in InitialData.Campaigns.get_items()
                if campaign.campaign_id in platform_campaigns
            ]
            pdf.set_font("Arial", style="B", size=12)
            pdf.cell(0, 10, f"Platform: {platform.platform_name}", ln=True)
            pdf.ln(5)
            headers = ["Campaign Name", "Start Date", "End Date", "Budget"]
            column_widths = [60, 40, 40, 40]
            for header, width in zip(headers, column_widths):
                pdf.cell(width, 10, header, border=1, align="C")
            pdf.ln()
            for campaign in campaigns:
                pdf.cell(60, 10, campaign.campaign_name or "Unnamed Campaign", border=1)
                pdf.cell(40, 10, campaign.start_date.strftime('%Y-%m-%d') if campaign.start_date else "N/A", border=1)
                pdf.cell(40, 10, campaign.end_date.strftime('%Y-%m-%d') if campaign.end_date else "N/A", border=1)
                pdf.cell(40, 10, f"${campaign.budget:.2f}" if campaign.budget else "N/A", border=1)
                pdf.ln()
            pdf.ln(10)
        pdf.output(file_path)
        QtWidgets.QMessageBox.information(self, "Success", f"Platform Campaign Report saved: {file_path}")

    def go_back(self):
        self.parent().show()
        self.close()


class ClientViewWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, client: Client = None):
        super().__init__(parent)
        uic.loadUi("ClientViewWindow.ui", self)
        self.client = client
        self.display_info()
        self.actionLogout.triggered.connect(self.go_back)
        self.campaignsBudgetButton.clicked.connect(self.generate_budget_report)
        self.campaignsAudienceButton.clicked.connect(self.generate_audience_report)
        self.platformsEfficiencyButton.clicked.connect(self.generate_platform_efficiency_report)
        self.campaignsAdvertisementsButton.clicked.connect(self.generate_advertising_messages_report)
        self.addCampaignButton.clicked.connect(self.create_campaign_request_document)

    def display_info(self):
        self.nameLabel.setText(self.client.company_name)
        campaigns = InitialData.Campaigns.find(company_name=self.client.company_name)
        if campaigns:
            headers = campaigns[0].GetData()[0]
            updated_headers = [header for header in headers if header != "Company Name"]
            self.campaignsTableWidget.setRowCount(len(campaigns))
            self.campaignsTableWidget.setColumnCount(len(updated_headers))
            self.campaignsTableWidget.setHorizontalHeaderLabels(updated_headers)

            for row_ind, row_data in enumerate(campaigns):
                campaign_data = row_data.GetData()[1]
                adjusted_data = [value for index, value in enumerate(campaign_data) if headers[index] != "Company Name"]
                for col_ind, col_data in enumerate(adjusted_data):
                    item = QTableWidgetItem(str(col_data))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.campaignsTableWidget.setItem(row_ind, col_ind, item)

            campaign_ids = [campaign.campaign_id for campaign in campaigns]
            used_platform_ids = {
                cp.platform_id for cp in InitialData.CampaignPlatforms.get_items()
                if cp.campaign_id in campaign_ids
            }
            used_platforms = [
                platform for platform in InitialData.MediaPlatforms.get_items()
                if platform.platform_id in used_platform_ids
            ]
            headers = used_platforms[0].GetData()[0]
            self.platformsTableWidget.setRowCount(len(used_platforms))
            self.platformsTableWidget.setColumnCount(len(headers))
            self.platformsTableWidget.setHorizontalHeaderLabels(headers)

            for row_ind, platform in enumerate(used_platforms):
                platform_data = platform.GetData()[1]
                for col_ind, col_data in enumerate(platform_data):
                    item = QTableWidgetItem(str(col_data))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.platformsTableWidget.setItem(row_ind, col_ind, item)



    # def edit_client(self):
    #     dialog = AddClientWindow(self)
    #     current_client = self.clients[self.current_index]
    #     if not current_client:
    #         QtWidgets.QMessageBox.warning(self, "Error", "Could not retrieve item for editing")
    #         return
    #     # print(self.campaigns[self.current_index])
    #     dialog.set_data(current_client)
    #     if dialog.exec_() == QtWidgets.QDialog.Accepted:
    #         updated_client = dialog.get_data()
    #         if updated_client:
    #             company_name = current_client.company_name
    #             for i, client in enumerate(InitialData.Clients.get_items()):
    #                 if client.company_name == company_name:
    #                     InitialData.Clients.update(i, updated_client)
    #                     break
    #             self.update_info()

    def go_back(self):
        self.parent().show()
        self.close()

    def export_to_excel(self, file_path, report_data, headers):
        excel_data = []
        for report in report_data:
            max_len = max(
                len(report.get(key, []))
                for key in headers[1:]
            )
            columns = {
                key: (report.get(key, []) )
                     + [""] * (max_len - len(report.get(key, [])))
                for key in headers[1:]
            }
            for values in zip(*columns.values()):
                row = {headers[0]: report.get(headers[0], "Unnamed")}
                for col_name, value in zip(headers[1:], values):
                    row[col_name] = value
                excel_data.append(row)
        df = pd.DataFrame(excel_data)
        df.to_excel(file_path, index=False)
        QtWidgets.QMessageBox.information(self, "Success", f"Report saved as Excel: {file_path}")

    def export_to_pdf(self, file_path, report_data, headers):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for report in report_data:
            pdf.set_font("Arial", style="B", size=14)
            pdf.cell(0, 10, f"{headers[0]}: {report.get(headers[0], 'Unnamed')}", ln=True)
            for header in headers[1:]:
                pdf.set_font("Arial", style="B", size=12)
                pdf.cell(0, 10, f"{header}:", ln=True)
                pdf.set_font("Arial", size=10)
                for item in report.get(header, []):
                    pdf.cell(0, 10, f"  - {item}", ln=True)
                pdf.ln(5)
            pdf.ln(10)
        pdf.output(file_path)
        QtWidgets.QMessageBox.information(self, "Success", f"Report saved as PDF: {file_path}")

    def generate_budget_report(self):
        campaigns = InitialData.Campaigns.find(company_name=self.client.company_name)
        if not campaigns:
            QtWidgets.QMessageBox.warning(self, "No Campaigns", "No campaigns found for this client.")
            return
        report_data = []
        for campaign in campaigns:
            total_budget = campaign.budget
            clicks = sum(
                ad.clicks
                for ad in InitialData.Advertisements.get_items()
                if ad.campaign_id == campaign.campaign_id and ad.clicks is not None
            )
            cost_per_click = total_budget / clicks if clicks else 0
            roi = (clicks * 3 - total_budget) / total_budget if total_budget else 0
            report_data.append({
                "Campaign Name": campaign.campaign_name or "Unnamed Campaign",
                "Total Budget": [total_budget],
                "Clicks": [clicks],
                "Cost per Click": [round(cost_per_click, 2)],
                "ROI (%)": [round(roi * 100, 2)]
            })
        headers = ["Campaign Name", "Total Budget", "Clicks", "Cost per Click", "ROI (%)"]
        self.export_report(report_data, headers, "Budget Report")

    def generate_audience_report(self):
        campaigns = InitialData.Campaigns.find(company_name=self.client.company_name)
        if not campaigns:
            QtWidgets.QMessageBox.warning(self, "No Campaigns", "No campaigns found for this client.")
            return
        report_data = []
        for campaign in campaigns:
            campaign_id = campaign.campaign_id
            campaign_platforms = [
                cp.platform_id for cp in InitialData.CampaignPlatforms.get_items()
                if cp.campaign_id == campaign_id
            ]
            audience_segments = {
                segment for sp in InitialData.SegmentPlatforms.get_items()
                if sp.platform_id in campaign_platforms
                for segment in InitialData.AudienceSegments.get_items()
                if segment.segment_id == sp.segment_id
            }
            report = {
                "Campaign Name": campaign.campaign_name or "Unnamed Campaign",
                "Demographics": list(set(f"{seg.age_range} ({seg.gender})" for seg in audience_segments)),

                "Interests": list(set(seg.general_interest for seg in audience_segments)),
                "Geographic Coverage": list(set(seg.location for seg in audience_segments)),
            }
            report_data.append(report)
        headers = [
            "Campaign Name",
            "Demographics",
            "Interests",
            "Geographic Coverage",
        ]
        self.export_report(report_data, headers, "Audience Report")

    def generate_platform_efficiency_report(self):
        campaigns = InitialData.Campaigns.find(company_name=self.client.company_name)
        platform_data = {}
        for campaign in campaigns:
            campaign_ads = [
                ad for ad in InitialData.Advertisements.get_items()
                if ad.campaign_id == campaign.campaign_id
            ]
            for ad in campaign_ads:
                if ad.platform_id not in platform_data:
                    platform_data[ad.platform_id] = {"Impressions": 0, "Clicks": 0}

                platform_data[ad.platform_id]["Impressions"] += ad.views or 0
                platform_data[ad.platform_id]["Clicks"] += ad.clicks or 0
        report_data = []
        for platform_id, metrics in platform_data.items():
            platform = next(
                (p for p in InitialData.MediaPlatforms.get_items() if p.platform_id == platform_id), None
            )
            if platform:
                impressions = metrics["Impressions"]
                clicks = metrics["Clicks"]
                conversion_rate = (clicks / impressions * 100) if impressions else 0
                report_data.append({
                    "Platform Name": platform.platform_name,
                    "Impressions": [impressions],
                    "Clicks": [clicks],
                    "Conversion Rate (%)": [round(conversion_rate, 2)],
                })
        headers = ["Platform Name", "Impressions", "Clicks", "Conversion Rate (%)"]
        self.export_report(report_data, headers, "Platform Efficiency Report")

    def generate_advertising_messages_report(self):
        campaigns = InitialData.Campaigns.find(company_name=self.client.company_name)
        if not campaigns:
            QtWidgets.QMessageBox.warning(self, "No Campaigns", "No campaigns found for this client.")
            return
        report_data = []
        for campaign in campaigns:
            campaign_ads = [
                ad for ad in InitialData.Advertisements.get_items()
                if ad.campaign_id == campaign.campaign_id
            ]
            for ad in campaign_ads:
                clicks = ad.clicks or 0
                impressions = ad.views or 0
                ctr = (clicks / impressions * 100) if impressions else 0

                report_data.append({
                    "Campaign Name": campaign.campaign_name or "Unnamed Campaign",
                    "Advertisement Text": [ad.text or "No Text"],
                    "Topic": [ad.topic or "No Topic"],
                    "Format": [ad.format],
                    "Clicks": [clicks],
                    "Impressions": [impressions],
                    "CTR (%)": [round(ctr, 2)],
                })

        headers = [
            "Campaign Name",
            "Advertisement Text",
            "Topic",
            "Format",
            "Clicks",
            "Impressions",
            "CTR (%)",
        ]
        self.export_report(report_data, headers, "Advertising Messages Report")

    def export_report(self, report_data, headers, report_title):
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, f"Save {report_title}", "", "Excel Files (*.xlsx);;PDF Files (*.pdf)"
        )
        if not file_path:
            return

        if file_path.endswith(".xlsx"):
            self.export_to_excel(file_path, report_data, headers)
        elif file_path.endswith(".pdf"):
            self.export_to_pdf(file_path, report_data, headers)
        else:
            QtWidgets.QMessageBox.warning(self, "Invalid File Type", "Please select a valid file type (.xlsx or .pdf).")

    def create_campaign_request_document(self):
        dialog = AddCampaignWindow(self)
        dialog.set_client_name(self.client.company_name)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            campaign_data = dialog.get_data()
            if not campaign_data:
                QtWidgets.QMessageBox.warning(self, "Error", "Failed to retrieve campaign data.")
                return
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
                self,
                "Save Campaign Request Document",
                "",
                "PDF Files (*.pdf)"
            )
            if not file_path:
                return
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.set_font("Arial", style="B", size=16)
            pdf.cell(0, 10, "Official Campaign Request", ln=True, align='C')
            pdf.ln(10)
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, f"Date: {datetime.today().strftime('%Y-%m-%d')}", ln=True)
            pdf.ln(5)
            pdf.cell(0, 10, f"Campaign Name: {campaign_data.campaign_name or 'Unnamed Campaign'}", ln=True)
            pdf.cell(0, 10, f"Goal: {campaign_data.goal}", ln=True)
            pdf.cell(0, 10, f"Budget: {campaign_data.budget if campaign_data.budget else 'N/A'}", ln=True)
            pdf.cell(0, 10,
                     f"Start Date: {campaign_data.start_date.strftime('%Y-%m-%d') if campaign_data.start_date else 'N/A'}",
                     ln=True)
            pdf.cell(0, 10,
                     f"End Date: {campaign_data.end_date.strftime('%Y-%m-%d') if campaign_data.end_date else 'N/A'}",
                     ln=True)
            pdf.cell(0, 10, f"Company: {campaign_data.company_name}", ln=True)
            pdf.ln(10)
            pdf.cell(0, 10, "Signature: __________________________", ln=True)
            pdf.ln(10)
            pdf.cell(0, 10, "Approved By: _______________________", ln=True)
            pdf.output(file_path)
            QtWidgets.QMessageBox.information(self, "Success", f"Campaign request document saved to {file_path}.")


class SegmentFilterWindow(QtWidgets.QDialog):
    def __init__(self, parent = None, criteria = None):
        super().__init__(parent)
        uic.loadUi("SegmentFilterWindow.ui", self)
        self.findButton.clicked.connect(self.accept)
        self.genderListWidget.addItems(["Male", "Female", "Other"])
        self.genderListWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.locationListWidget.addItems(InitialData.LOCATIONS)
        self.locationListWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.deviceListWidget.addItems(InitialData.DEVICES)
        self.deviceListWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        if criteria:
            for index in range(self.genderListWidget.count()):
                item = self.genderListWidget.item(index)
                if item.text() in criteria["Genders"]:
                    item.setSelected(True)
            for index in range(self.locationListWidget.count()):
                item = self.locationListWidget.item(index)
                if item.text() in criteria["Locations"]:
                    item.setSelected(True)
            for index in range(self.deviceListWidget.count()):
                item = self.deviceListWidget.item(index)
                if item.text() in criteria["Devices"]:
                    item.setSelected(True)
            self.minAgeSpinBox.setValue(criteria["Minimum age"])
            self.maxAgeSpinBox.setValue(criteria["Maximum age"])

    def get_filter_criteria(self):
        selected_genders = [item.text() for item in self.genderListWidget.selectedItems()]
        selected_locations = [item.text() for item in self.locationListWidget.selectedItems()]
        selected_devices = [item.text() for item in self.deviceListWidget.selectedItems()]
        minimum_age = self.minAgeSpinBox.value()
        maximum_age = self.maxAgeSpinBox.value()
        return [selected_genders, selected_locations, selected_devices, minimum_age, maximum_age]
class AdvertisementFilterWindow(QtWidgets.QDialog):
    def __init__(self, parent = None, criteria = None):
        super().__init__(parent)
        uic.loadUi("AdvertisementsFilterWindow.ui", self)
        self.findButton.clicked.connect(self.accept)
        self.formatListWidget.addItems(InitialData.ADVERTISEMENT_FORMATS)
        self.formatListWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.languageListWidget.addItems(InitialData.LANGUAGES)
        self.languageListWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.dateBeforeCheckbox.setChecked(True)
        self.dateAfterCheckbox.setChecked(True)
        self.beforeDateEdit.setCalendarPopup(True)
        self.afterDateEdit.setCalendarPopup(True)
        if criteria:
            for index in range(self.formatListWidget.count()):
                item = self.formatListWidget.item(index)
                if item.text() in criteria["Formats"]:
                    item.setSelected(True)
            for index in range(self.languageListWidget.count()):
                item = self.languageListWidget.item(index)
                if item.text() in criteria["Languages"]:
                    item.setSelected(True)
            if criteria["Before date"]:
                self.beforeDateEdit.setDate(criteria["Before date"])
            else:
                self.dateBeforeCheckbox.setChecked(False)
            if criteria["After date"]:
                self.afterDateEdit.setDate(criteria["After date"])
            else:
                self.dateAfterCheckbox.setChecked(False)
            self.clicksSpinBox.setValue(criteria["Minimum clicks"])

    def get_filter_criteria(self):
        selected_formats = [item.text() for item in self.formatListWidget.selectedItems()]
        selected_languages = [item.text() for item in self.languageListWidget.selectedItems()]
        before_date = datetime.combine(self.beforeDateEdit.date().toPyDate(),
                      datetime.min.time()) if self.dateBeforeCheckbox.isChecked() else None
        after_date = datetime.combine(self.afterDateEdit.date().toPyDate(),
                                       datetime.min.time()) if self.dateAfterCheckbox.isChecked() else None
        minimum_clicks = self.clicksSpinBox.value()
        return [selected_formats, selected_languages, before_date, after_date, minimum_clicks]


class CampaignFindWindow(QtWidgets.QDialog):
    def __init__(self, parent=None, criteria = None):
        super().__init__(parent)
        uic.loadUi("CampaignFindWindow.ui", self)
        self.findButton.clicked.connect(self.accept)
        if criteria:
            self.nameLineEdit.setText(criteria["Name"])
            self.goalLineEdit.setText(criteria["Goal"])

    def get_search_criteria(self):
        # print(1)
        # print(self.nameLineEdit.text().strip(), self.goalLineEdit.text().strip())
        return [self.nameLineEdit.text().strip(), self.goalLineEdit.text().strip()]

class ClientFindWindow(QtWidgets.QDialog):
    def __init__(self, parent=None, criteria = None):
        super().__init__(parent)
        uic.loadUi("ClientFindWindow.ui", self)
        self.findButton.clicked.connect(self.accept)
        if criteria:
            self.nameLineEdit.setText(criteria["Name"])
            self.emailLineEdit.setText(criteria["Email"])
            self.phoneLineEdit.setText(criteria["Phone"])
            self.areaLineEdit.setText(criteria["Area"])

    def get_search_criteria(self):
        # print(1)
        # print(self.nameLineEdit.text().strip(), self.goalLineEdit.text().strip())
        return [self.nameLineEdit.text().strip(), self.emailLineEdit.text().strip(),
                self.phoneLineEdit.text().strip(), self.areaLineEdit.text().strip()]


class CampaignSortWindow(QtWidgets.QDialog):
    def __init__(self, parent=None, criteria = None):
        super().__init__(parent)
        uic.loadUi("CampaignSortWindow.ui", self)
        self.sortButton.clicked.connect(self.accept)
        if (criteria == "By start date"):
            self.startDateRadioButton.setChecked(True)
        elif (criteria == "By budget"):
            self.budgetRadioButton.setChecked(True)
        elif (criteria == "By name"):
            self.nameRadioButton.setChecked(True)

    def get_selected_option(self):
        if self.startDateRadioButton.isChecked():
            return "By start date"
        elif self.budgetRadioButton.isChecked():
            return "By budget"
        elif self.nameRadioButton.isChecked():
            return "By name"
        return None


class ClientSortWindow(QtWidgets.QDialog):
    def __init__(self, parent=None, criteria = None):
        super().__init__(parent)
        uic.loadUi("ClientSortWindow.ui", self)
        self.sortButton.clicked.connect(self.accept)
        if (criteria == "By company name"):
            self.nameRadioButton.setChecked(True)
        elif (criteria == "By type"):
            self.typeRadioButton.setChecked(True)
        elif (criteria == "By available budget"):
            self.budgetRadioButton.setChecked(True)

    def get_selected_option(self):
        if self.nameRadioButton.isChecked():
            return "By company name"
        elif self.typeRadioButton.isChecked():
            return "By type"
        elif self.budgetRadioButton.isChecked():
            return "By available budget"
        return None

# class SelectPlatformDialog(QtWidgets.QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         uic.loadUi("SelectExistingItemWindow.ui", self)
#         self.platforms = []
#         self.selected_platform = None
#         self.budget_allocation = None
#         self.addButton.clicked.connect(self.add_platform)
#         self.budgetButton.clicked.connect(self.toggle_budget)
#         self.budgetButton.setText("Add budget")
#         self.budgetSpinBox.setEnabled(False)
#
#     def toggle_budget(self) -> None:
#         if self.budgetSpinBox.isEnabled():
#             self.budgetSpinBox.setEnabled(False)
#             self.budgetButton.setText("Add budget")
#         else:
#             self.budgetSpinBox.setEnabled(True)
#             self.budgetButton.setText("Remove budget")
#
#     def set_platforms(self, platforms):
#         self.platforms = platforms
#         self.platformComboBox.clear()
#         for platform in platforms:
#             self.platformComboBox.addItem(platform.platform_name)
#
#     def add_platform(self):
#         selected_index = self.platformComboBox.currentIndex()
#         if selected_index == -1:
#             QtWidgets.QMessageBox.warning(self, "Error", "Please select a platform.")
#             return
#         self.selected_platform = self.platforms[selected_index]
#         self.budget_allocation = int(self.budgetSpinBox.value())
#         self.accept()
#
#     def get_selected_platform(self):
#         return self.selected_platform
#
#     def get_budget_allocation(self):
#         if self.budgetSpinBox.isEnabled():
#             print(self.budget_allocation)
#             return self.budget_allocation
#         else:
#             return None

class SelectExistingItemDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("SelectExistingItemWindow.ui", self)
        self.items = []
        self.selected_item = None
        self.budget_allocation = None
        self.addButton.clicked.connect(self.add_item)
        self.budgetButton.clicked.connect(self.toggle_budget)
        self.budgetButton.setText("Add budget")
        self.budgetSpinBox.setEnabled(False)
        self.budgetButton.setVisible(False)
        self.budgetSpinBox.setVisible(False)
        self.budgetLabel.setVisible(False)

    def configure_dialog(self, items, show_budget=False, label_text = "Items"):
        self.items = items
        self.itemComboBox.clear()
        for item in items:
            self.itemComboBox.addItem(item.platform_name if hasattr(item, "platform_name")
                                      else item.campaign_name if hasattr(item, "campaign_name")
            else item.segment_name if hasattr(item, "segment_name")
            else str(item))
        self.budgetButton.setVisible(show_budget)
        self.budgetSpinBox.setVisible(show_budget)
        self.budgetLabel.setVisible(show_budget)
        self.itemLabel.setText(label_text)

    def toggle_budget(self) -> None:
        if self.budgetSpinBox.isEnabled():
            self.budgetSpinBox.setEnabled(False)
            self.budgetButton.setText("Add budget")
        else:
            self.budgetSpinBox.setEnabled(True)
            self.budgetButton.setText("Remove budget")

    def add_item(self):
        selected_index = self.itemComboBox.currentIndex()
        if selected_index == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select an item.")
            return
        self.selected_item = self.items[selected_index]
        self.budget_allocation = int(self.budgetSpinBox.value()) if self.budgetSpinBox.isEnabled() else None
        self.accept()

    def get_selected_item(self):
        return self.selected_item

    def get_budget_allocation(self):
        return self.budget_allocation if self.budgetSpinBox.isEnabled() else None


class SelectExistingSingleItemDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("SelectExistingSingleItemWindow.ui", self)
        self.items = []
        self.selected_item = None
        self.addButton.clicked.connect(self.add_item)

    def configure_dialog(self, items, label_text="Items"):
        self.items = items
        self.itemComboBox.clear()
        for item in items:
            self.itemComboBox.addItem(
                item.topic if hasattr(item, "topic") else
                item.email if hasattr(item, "email") else
                str(item)
            )
        self.itemLabel.setText(label_text)

    def add_item(self):
        selected_index = self.itemComboBox.currentIndex()
        if selected_index == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select an item.")
            return
        self.selected_item = self.items[selected_index]
        self.accept()

    def get_selected_item(self):
        return self.selected_item


class CampaignWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, campaign: Campaign = None, update_callback = None):
        super().__init__(parent)
        uic.loadUi("CampaignWindow.ui", self)

        self.campaigns = InitialData.Campaigns.get_items()
        self.current_index = self.campaigns.index(campaign) if campaign else 0
        self.update_callback = update_callback
        self.update_info()
        self.nextButton.clicked.connect(self.navigate_next)
        self.previousButton.clicked.connect(self.navigate_previous)
        self.editButton.clicked.connect(self.edit_campaign)
        self.backButton.clicked.connect(self.go_back)
        self.addPlatformButton.clicked.connect(self.add_platform)
        self.editPlatformButton.clicked.connect(self.edit_platform)
        self.removePlatformButton.clicked.connect(self.remove_platform)
        self.addAdvertisementButton.clicked.connect(self.add_advertisement)
        self.editAdvertisementButton.clicked.connect(self.edit_advertisement)
        self.removeAdvertisementButton.clicked.connect(self.remove_advertisement)
        self.addExistingAdvertisementButton.clicked.connect(self.add_existing_advertisement)
        self.addExistingPlatformButton.clicked.connect(self.add_existing_platform)
        self.removePlatformFromCampaignButton.clicked.connect(self.remove_platform_from_campaign)
        self.removeAdvertisementFromCampaignButton.clicked.connect(self.remove_advertisement_from_campaign)

    def remove_platform_from_campaign(self):
        selected_row = self.platformsTableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a platform to remove from the campaign.")
            return
        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure you want to remove the selected platform from this campaign?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            platform_id = int(
                self.platformsTableWidget.item(selected_row, 0).text()
            )
            current_campaign_id = self.campaigns[self.current_index].campaign_id
            campaign_platform = next(
                (cp for cp in InitialData.CampaignPlatforms.get_items()
                 if cp.campaign_id == current_campaign_id and cp.platform_id == platform_id),
                None
            )
            if campaign_platform:
                InitialData.CampaignPlatforms.remove(campaign_platform)
            self.update_info()

    def remove_advertisement_from_campaign(self):
        selected_row = self.advertisementsTableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select an advertisement to remove from the campaign.")
            return
        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure you want to remove the selected advertisement from this campaign?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            advertisement_id = int(
                self.advertisementsTableWidget.item(selected_row, 0).text()
            )
            advertisement = next(
                (ad for ad in InitialData.Advertisements.get_items() if ad.advertisement_id == advertisement_id),
                None
            )
            if advertisement:
                advertisement.campaign_id = None
                advertisement_index = InitialData.Advertisements.get_items().index(advertisement)
                InitialData.Advertisements.update(advertisement_index, advertisement)
            self.update_info()

    def add_existing_platform(self):
        dialog = SelectExistingItemDialog(self)
        current_campaign_id = self.campaigns[self.current_index].campaign_id
        used_platform_ids = [
            cp.platform_id for cp in InitialData.CampaignPlatforms.get_items() if cp.campaign_id == current_campaign_id
        ]
        available_platforms = [
            platform for platform in InitialData.MediaPlatforms.get_items() if
            platform.platform_id not in used_platform_ids
        ]
        dialog.configure_dialog(
            items=available_platforms,
            show_budget=True,
            label_text="Platforms"
        )
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            selected_platform = dialog.get_selected_item()
            allocated_budget = dialog.get_budget_allocation()
            if selected_platform:
                platform_id = selected_platform.platform_id
                campaign_platform = CampaignPlatform(
                    campaign_id=current_campaign_id,
                    platform_id=platform_id,
                    budget_allocation=allocated_budget
                )
                InitialData.CampaignPlatforms.add(campaign_platform)
                self.update_info()

    def add_existing_advertisement(self):
        dialog = SelectExistingSingleItemDialog(self)
        available_ads = [ad for ad in InitialData.Advertisements.get_items() if ad.campaign_id is None]
        dialog.configure_dialog(available_ads, "Advertisement topics")
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            selected_advertisement = dialog.get_selected_item()
            if selected_advertisement:
                current_campaign_id = self.campaigns[self.current_index].campaign_id
                selected_advertisement.campaign_id = current_campaign_id
                advertisement_index = InitialData.Advertisements.get_items().index(selected_advertisement)
                InitialData.Advertisements.update(advertisement_index, selected_advertisement)
                self.update_info()

    def add_platform(self):
        dialog = AddPlatformWindow(self)
        dialog.show_budget_allocation()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            new_platform = dialog.get_data()
            if new_platform:
                InitialData.MediaPlatforms.add(new_platform)
                current_campaign_id = self.campaigns[self.current_index].campaign_id
                platform_id = new_platform.platform_id
                budget_allocation = dialog.get_budget_allocation()
                campaign_platform = CampaignPlatform(
                    campaign_id=current_campaign_id,
                    platform_id=platform_id,
                    budget_allocation=budget_allocation
                )
                InitialData.CampaignPlatforms.add(campaign_platform)
                self.update_info()

    def edit_platform(self):
        selected_row = self.platformsTableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a platform to edit.")
            return

        platform_id = int(
            self.platformsTableWidget.item(selected_row, 0).text())
        selected_platform = next(
            (p for p in InitialData.MediaPlatforms.get_items() if p.platform_id == platform_id),
            None)
        current_campaign_id = self.campaigns[self.current_index].campaign_id
        campaign_platform = next(
            (cp for cp in InitialData.CampaignPlatforms.get_items()
             if cp.campaign_id == current_campaign_id and cp.platform_id == platform_id),
            None
        )
        dialog = AddPlatformWindow(self)
        dialog.set_data(selected_platform)
        dialog.set_budget_allocation(campaign_platform.budget_allocation)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            updated_platform = dialog.get_data()
            updated_budget_allocation = dialog.get_budget_allocation()
            if updated_platform:
                for i, platform in enumerate(InitialData.MediaPlatforms.get_items()):
                    if platform.platform_id == platform_id:
                        InitialData.MediaPlatforms.update(i, updated_platform)
                        break
                for i, cp in enumerate(InitialData.CampaignPlatforms.get_items()):
                    if cp.campaign_id == current_campaign_id and cp.platform_id == platform_id:
                        cp.budget_allocation = updated_budget_allocation
                        InitialData.CampaignPlatforms.update(i, cp)
                        break
                self.update_info()

    def remove_platform(self):
        selected_row = self.platformsTableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a platform to remove.")
            return

        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure you want to delete the selected platform?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            platform_id = int(
                self.platformsTableWidget.item(selected_row, 0).text())

            for cp in InitialData.CampaignPlatforms.get_items():
                if cp.platform_id == platform_id:
                    InitialData.CampaignPlatforms.remove(cp)

            remove_item = next(
                (p for p in InitialData.MediaPlatforms.get_items() if p.platform_id == platform_id),
                None
            )
            if remove_item:
                InitialData.MediaPlatforms.remove(remove_item)
            self.update_info()

    def add_advertisement(self):
        dialog = AddAdvertisementWindow(self)
        dialog.set_campaign_name(self.campaigns[self.current_index].campaign_name)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            new_advertisement = dialog.get_data()
            if new_advertisement:
                InitialData.Advertisements.add(new_advertisement)
                self.update_info()

    def edit_advertisement(self):
        selected_row = self.advertisementsTableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select an advertisement to edit.")
            return
        key_value = self.advertisementsTableWidget.item(selected_row, 0).text()
        selected_advertisement = next(
            (ad for ad in InitialData.Advertisements.get_items() if str(ad.GetData()[1][0]) == key_value),
            None
        )
        dialog = AddAdvertisementWindow(self)
        dialog.set_data(selected_advertisement)
        dialog.set_campaign_name(self.campaigns[self.current_index].campaign_name)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            updated_advertisement = dialog.get_data()
            if updated_advertisement:
                advertisement_index = InitialData.Advertisements.get_items().index(selected_advertisement)
                InitialData.Advertisements.update(advertisement_index, updated_advertisement)
                self.update_info()


    def remove_advertisement(self):
        selected_row = self.advertisementsTableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select an advertisement to remove.")
            return

        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure you want to delete the selected advertisement?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            key_value = self.advertisementsTableWidget.item(selected_row, 0).text()
            remove_item = next(
                (ad for ad in InitialData.Advertisements.get_items() if str(ad.GetData()[1][0]) == key_value),
                None
            )
            if remove_item:
                InitialData.Advertisements.remove(remove_item)
            self.update_info()

    def update_info(self):
        if not self.campaigns:
            QtWidgets.QMessageBox.warning(self, "Error", "No campaigns available.")
            self.close()
            return

        campaign = self.campaigns[self.current_index]
        start_date = campaign.start_date if isinstance(campaign.start_date, datetime) else None
        end_date = campaign.end_date if isinstance(campaign.end_date, datetime) else None
        self.idLabel.setText(f"ID: {campaign.campaign_id}")
        self.nameLabel.setText(f"Name: {campaign.campaign_name or 'N/A'}")
        self.startLabel.setText(
            f"Start Date: {start_date.strftime('%Y-%m-%d') if campaign.start_date else 'N/A'}")
        self.endLabel.setText(f"End Date: {end_date.strftime('%Y-%m-%d') if campaign.end_date else 'N/A'}")
        self.goalLabel.setText(f"Goal: {campaign.goal or 'N/A'}")
        self.budgetLabel.setText(f"Budget: {campaign.budget if campaign.budget else 'N/A'}")
        self.companyLabel.setText(f"Company: {campaign.company_name or 'N/A'}")
        advertisements = InitialData.Advertisements.find(campaign_id=campaign.campaign_id)
        campaign_platforms = InitialData.CampaignPlatforms.find(campaign_id=campaign.campaign_id)
        if campaign_platforms:
            platform_ids = [cp.platform_id for cp in campaign_platforms]
            related_platforms = [p for p in InitialData.MediaPlatforms.get_items() if p.platform_id in platform_ids]
            if related_platforms:
                headers = related_platforms[0].GetData()[0]
                headers.append("Budget Allocation")
                budget_map = {cp.platform_id: cp.budget_allocation for cp in campaign_platforms}
                self.platformsTableWidget.setRowCount(len(related_platforms))
                self.platformsTableWidget.setColumnCount(len(headers))
                self.platformsTableWidget.setHorizontalHeaderLabels(headers)
                for row_ind, platform in enumerate(related_platforms):
                    for col_ind, col_data in enumerate(platform.GetData()[1]):
                        item = QTableWidgetItem(str(col_data))
                        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        self.platformsTableWidget.setItem(row_ind, col_ind, item)
                    allocation = budget_map.get(platform.platform_id, "")
                    allocation_item = QTableWidgetItem(str(allocation))
                    allocation_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.platformsTableWidget.setItem(row_ind, len(headers) - 1, allocation_item)
        if advertisements:
            headers = advertisements[0].GetData()[0]
            updated_headers = []
            for header in headers:
                if header == "Campaign ID":
                    continue
                elif header == "Platform ID":
                    updated_headers.append("Platform Name")
                else:
                    updated_headers.append(header)
            platform_map = {platform.platform_id: platform.platform_name for platform in
                            InitialData.MediaPlatforms.get_items()}
            campaign_id_index = advertisements[0].GetData()[0].index("Campaign ID")
            platform_id_index = advertisements[0].GetData()[0].index("Platform ID")
            self.advertisementsTableWidget.setRowCount(len(advertisements))
            self.advertisementsTableWidget.setColumnCount(len(updated_headers))
            self.advertisementsTableWidget.setHorizontalHeaderLabels(updated_headers)
            for row_ind, row_data in enumerate(advertisements):
                for col_ind, col_data in enumerate(row_data.GetData()[1]):
                    if col_ind == campaign_id_index:
                        continue
                    elif col_ind == platform_id_index:
                        platform_name = platform_map.get(col_data, "")
                        item = QTableWidgetItem(platform_name)
                    else:
                        item = QTableWidgetItem(str(col_data))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    adjusted_col_ind = col_ind if col_ind < campaign_id_index else col_ind - 1
                    self.advertisementsTableWidget.setItem(row_ind, adjusted_col_ind, item)

    def navigate_next(self):
        if self.current_index < len(self.campaigns) - 1:
            self.current_index += 1
            self.update_info()
        else:
            QtWidgets.QMessageBox.information(self, "Info", "This is the last campaign.")

    def navigate_previous(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_info()
        else:
            QtWidgets.QMessageBox.information(self, "Info", "This is the first campaign.")

    def edit_campaign(self):
        dialog = AddCampaignWindow(self)
        current_campaign = self.campaigns[self.current_index]
        if not self.campaigns[self.current_index]:
            QtWidgets.QMessageBox.warning(self, "Error", "Could not retrieve item for editing")
            return
        # print(self.campaigns[self.current_index])
        dialog.set_data(self.campaigns[self.current_index])
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            updated_campaign = dialog.get_data()
            if updated_campaign:
                campaign_id = current_campaign.campaign_id
                for i, campaign in enumerate(InitialData.Campaigns.get_items()):
                    if campaign.campaign_id == campaign_id:
                        InitialData.Campaigns.update(i, updated_campaign)
                        break
                self.update_info()

    def go_back(self):
        if self.update_callback:
            self.update_callback()
        self.parent().show()
        self.close()


class ClientWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, client: Client = None, update_callback = None):
        super().__init__(parent)
        uic.loadUi("ClientWindow.ui", self)

        self.clients = InitialData.Clients.get_items()
        self.current_index = self.clients.index(client) if client else 0
        self.update_callback = update_callback
        self.update_info()
        self.nextButton.clicked.connect(self.navigate_next)
        self.previousButton.clicked.connect(self.navigate_previous)
        self.editButton.clicked.connect(self.edit_client)
        self.backButton.clicked.connect(self.go_back)
        self.addCampaignButton.clicked.connect(self.add_campaign)
        self.editCampaignButton.clicked.connect(self.edit_campaign)
        self.removeCampaignButton.clicked.connect(self.remove_campaign)

    def add_campaign(self):
        dialog = AddCampaignWindow(self)
        dialog.set_client_name(self.clients[self.current_index].company_name)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            new_campaign = dialog.get_data()
            if new_campaign:
                InitialData.Campaigns.add(new_campaign)
                self.update_info()

    def edit_campaign(self):
        selected_row = self.campaignsTableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select an campaign to edit.")
            return
        key_value = self.campaignsTableWidget.item(selected_row, 0).text()
        selected_campaign = next(
            (c for c in InitialData.Campaigns.get_items() if str(c.GetData()[1][0]) == key_value),
            None
        )
        dialog = AddCampaignWindow(self)
        dialog.set_data(selected_campaign)
        dialog.set_client_name(self.clients[self.current_index].company_name)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            updated_campaign = dialog.get_data()
            if updated_campaign:
                campaign_index = InitialData.Campaigns.get_items().index(selected_campaign)
                InitialData.Campaigns.update(campaign_index, updated_campaign)
                self.update_info()

    def remove_campaign(self):
        selected_row = self.campaignsTableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select an campaign to remove.")
            return

        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure you want to delete the selected campaign?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            key_value = self.campaignsTableWidget.item(selected_row, 0).text()
            remove_item = next(
                (c for c in InitialData.Campaigns.get_items() if str(c.GetData()[1][0]) == key_value),
                None
            )
            if remove_item:
                InitialData.Campaigns.remove(remove_item)
            self.update_info()

    def update_info(self):
        if not self.clients:
            QtWidgets.QMessageBox.warning(self, "Error", "No clients available.")
            self.close()
            return

        client = self.clients[self.current_index]
        self.nameLabel.setText(f"Name: {client.company_name}")
        self.phoneLabel.setText(f"Phone: {client.phone}")
        self.emailLabel.setText(f"Email: {client.email}")
        self.passwordLabel.setText(f"Password: {client.password}")
        self.addressLabel.setText(f"Address: {client.address}")
        self.typeLabel.setText(f"Type: {client.type}")
        self.areaLabel.setText(f"Business area: {client.business_area}")
        self.budgetLabel.setText(f"Available budget: {client.available_budget}")
        campaigns = InitialData.Campaigns.find(company_name=client.company_name)

        if campaigns:
            headers = campaigns[0].GetData()[0]
            updated_headers = [header for header in headers if header != "Company Name"]
            self.campaignsTableWidget.setRowCount(len(campaigns))
            self.campaignsTableWidget.setColumnCount(len(updated_headers))
            self.campaignsTableWidget.setHorizontalHeaderLabels(updated_headers)

            for row_ind, row_data in enumerate(campaigns):
                campaign_data = row_data.GetData()[1]
                adjusted_data = [value for index, value in enumerate(campaign_data) if headers[index] != "Company Name"]
                for col_ind, col_data in enumerate(adjusted_data):
                    item = QTableWidgetItem(str(col_data))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.campaignsTableWidget.setItem(row_ind, col_ind, item)
        else:
            self.campaignsTableWidget.clear()

    def navigate_next(self):
        if self.current_index < len(self.clients) - 1:
            self.current_index += 1
            self.update_info()
        else:
            QtWidgets.QMessageBox.information(self, "Info", "This is the last client.")

    def navigate_previous(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_info()
        else:
            QtWidgets.QMessageBox.information(self, "Info", "This is the first client.")

    def edit_client(self):
        dialog = AddClientWindow(self)
        current_client = self.clients[self.current_index]
        if not current_client:
            QtWidgets.QMessageBox.warning(self, "Error", "Could not retrieve item for editing")
            return
        # print(self.campaigns[self.current_index])
        dialog.set_data(current_client)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            updated_client = dialog.get_data()
            if updated_client:
                company_name = current_client.company_name
                for i, client in enumerate(InitialData.Clients.get_items()):
                    if client.company_name == company_name:
                        InitialData.Clients.update(i, updated_client)
                        break
                self.update_info()

    def go_back(self):
        if self.update_callback:
            self.update_callback()
        self.parent().show()
        self.close()








class PlatformWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, platform: MediaPlatform = None, update_callback = None):
        super().__init__(parent)
        uic.loadUi("PlatformWindow.ui", self)

        self.platforms = InitialData.MediaPlatforms.get_items()
        self.current_index = self.platforms.index(platform) if platform else 0
        self.update_callback = update_callback
        self.update_info()
        self.nextButton.clicked.connect(self.navigate_next)
        self.previousButton.clicked.connect(self.navigate_previous)
        self.editButton.clicked.connect(self.edit_platform)
        self.backButton.clicked.connect(self.go_back)
        self.addCampaignButton.clicked.connect(self.add_campaign)
        self.editCampaignButton.clicked.connect(self.edit_campaign)
        self.removeCampaignButton.clicked.connect(self.remove_campaign)
        self.addSegmentButton.clicked.connect(self.add_segment)
        self.editSegmentButton.clicked.connect(self.edit_segment)
        self.removeSegmentButton.clicked.connect(self.remove_segment)
        self.addAdvertisementButton.clicked.connect(self.add_advertisement)
        self.editAdvertisementButton.clicked.connect(self.edit_advertisement)
        self.removeAdvertisementButton.clicked.connect(self.remove_advertisement)
        self.addExistingAdvertisementButton.clicked.connect(self.add_existing_advertisement)
        self.addExistingCampaignButton.clicked.connect(self.add_existing_campaign)
        self.addExistingSegmentButton.clicked.connect(self.add_existing_segment)
        self.removeCampaignFromPlatformButton.clicked.connect(self.remove_campaign_from_platform)
        self.removeAdvertisementFromPlatformButton.clicked.connect(self.remove_advertisement_from_platform)
        self.removeSegmentFromPlatformButton.clicked.connect(self.remove_segment_from_platform)

    def remove_campaign_from_platform(self):
        selected_row = self.campaignsTableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a campaign to remove from the platform.")
            return
        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure you want to remove the selected campaign from this platform?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            campaign_id = int(
                self.campaignsTableWidget.item(selected_row, 0).text()
            )
            current_platform_id = self.platforms[self.current_index].platform_id
            campaign_platform = next(
                (cp for cp in InitialData.CampaignPlatforms.get_items()
                 if cp.campaign_id == campaign_id and cp.platform_id == current_platform_id),
                None
            )
            if campaign_platform:
                InitialData.CampaignPlatforms.remove(campaign_platform)
            self.update_info()

    def remove_segment_from_platform(self):
        selected_row = self.segmentsTableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a segment to remove from the platform.")
            return
        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure you want to remove the selected segment from this platform?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            segment_id = int(
                self.segmentsTableWidget.item(selected_row, 0).text()
            )
            current_platform_id = self.platforms[self.current_index].platform_id
            segment_platform = next(
                (sp for sp in InitialData.SegmentPlatforms.get_items()
                 if sp.segment_id == segment_id and sp.platform_id == current_platform_id),
                None
            )
            if segment_platform:
                InitialData.SegmentPlatforms.remove(segment_platform)
            self.update_info()

    def remove_advertisement_from_platform(self):
        selected_row = self.advertisementsTableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select an advertisement to remove from the platform.")
            return
        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure you want to remove the selected advertisement from this platform?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            advertisement_id = int(
                self.advertisementsTableWidget.item(selected_row, 0).text()
            )
            advertisement = next(
                (ad for ad in InitialData.Advertisements.get_items() if ad.advertisement_id == advertisement_id),
                None
            )
            if advertisement:
                advertisement.platform_id = None
                advertisement_index = InitialData.Advertisements.get_items().index(advertisement)
                InitialData.Advertisements.update(advertisement_index, advertisement)
            self.update_info()

    def add_existing_campaign(self):
        dialog = SelectExistingItemDialog(self)
        current_platform_id = self.platforms[self.current_index].platform_id
        used_campaigns_ids = [
            cp.campaign_id for cp in InitialData.CampaignPlatforms.get_items() if cp.platform_id == current_platform_id
        ]
        available_campaigns = [
            campaign for campaign in InitialData.Campaigns.get_items() if
            campaign.campaign_id not in used_campaigns_ids and campaign.campaign_name
        ]
        dialog.configure_dialog(
            items=available_campaigns,
            show_budget=True,
            label_text="Campaigns"
        )
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            selected_campaign = dialog.get_selected_item()
            allocated_budget = dialog.get_budget_allocation()
            if selected_campaign:
                campaign_id = selected_campaign.campaign_id
                campaign_platform = CampaignPlatform(
                    campaign_id=campaign_id,
                    platform_id=current_platform_id,
                    budget_allocation=allocated_budget
                )
                InitialData.CampaignPlatforms.add(campaign_platform)
                self.update_info()

    def add_existing_segment(self):
        dialog = SelectExistingItemDialog(self)
        current_platform_id = self.platforms[self.current_index].platform_id
        used_segments_ids = [
            sp.segment_id for sp in InitialData.SegmentPlatforms.get_items() if sp.platform_id == current_platform_id
        ]
        available_segments = [
            segment for segment in InitialData.AudienceSegments.get_items() if
            segment.segment_id not in used_segments_ids and segment.segment_name
        ]
        dialog.configure_dialog(
            items=available_segments,
            show_budget=False,
            label_text="Segments"
        )
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            selected_segment = dialog.get_selected_item()
            if selected_segment:
                segment_id = selected_segment.segment_id
                segment_platform = SegmentPlatform(
                    segment_id=segment_id,
                    platform_id=current_platform_id
                )
                InitialData.SegmentPlatforms.add(segment_platform)
                self.update_info()

    def add_existing_advertisement(self):
        dialog = SelectExistingSingleItemDialog(self)
        available_ads = [ad for ad in InitialData.Advertisements.get_items() if ad.platform_id is None]
        dialog.configure_dialog(available_ads, "Advertisement topics")
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            selected_advertisement = dialog.get_selected_item()
            if selected_advertisement:
                current_platform_id = self.platforms[self.current_index].platform_id
                selected_advertisement.platform_id = current_platform_id
                advertisement_index = InitialData.Advertisements.get_items().index(selected_advertisement)
                InitialData.Advertisements.update(advertisement_index, selected_advertisement)
                self.update_info()

    def add_campaign(self):
        dialog = AddCampaignWindow(self)
        dialog.show_budget_allocation()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            new_campaign = dialog.get_data()
            if new_campaign:
                InitialData.Campaigns.add(new_campaign)
                current_platform_id = self.platforms[self.current_index].platform_id
                campaign_id = new_campaign.campaign_id
                budget_allocation = dialog.get_budget_allocation()
                campaign_platform = CampaignPlatform(
                    campaign_id=campaign_id,
                    platform_id=current_platform_id,
                    budget_allocation=budget_allocation
                )
                InitialData.CampaignPlatforms.add(campaign_platform)
                self.update_info()

    def edit_campaign(self):
        selected_row = self.campaignsTableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a campaign to edit.")
            return

        campaign_id = int(
            self.campaignsTableWidget.item(selected_row, 0).text())
        selected_campaign = next(
            (c for c in InitialData.Campaigns.get_items() if c.campaign_id == campaign_id),
            None)
        current_platform_id = self.platforms[self.current_index].platform_id
        campaign_platform = next(
            (cp for cp in InitialData.CampaignPlatforms.get_items()
             if cp.campaign_id == campaign_id and cp.platform_id == current_platform_id),
            None
        )
        dialog = AddCampaignWindow(self)
        dialog.set_data(selected_campaign)
        dialog.set_budget_allocation(campaign_platform.budget_allocation)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            updated_campaign = dialog.get_data()
            updated_budget_allocation = dialog.get_budget_allocation()
            if updated_campaign:
                for i, campaign in enumerate(InitialData.Campaigns.get_items()):
                    if campaign.campaign_id == campaign_id:
                        InitialData.Campaigns.update(i, updated_campaign)
                        break
                for i, cp in enumerate(InitialData.CampaignPlatforms.get_items()):
                    if cp.campaign_id == campaign_id and cp.platform_id == current_platform_id:
                        cp.budget_allocation = updated_budget_allocation
                        InitialData.CampaignPlatforms.update(i, cp)
                        break
                self.update_info()

    def remove_campaign(self):
        selected_row = self.campaignsTableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a campaign to remove.")
            return

        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure you want to delete the selected campaign?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            campaign_id = int(
                self.campaignsTableWidget.item(selected_row, 0).text())

            for cp in InitialData.CampaignPlatforms.get_items():
                if cp.campaign_id == campaign_id:
                    InitialData.CampaignPlatforms.remove(cp)

            remove_item = next(
                (c for c in InitialData.Campaigns.get_items() if c.campaign_id == campaign_id),
                None
            )
            if remove_item:
                InitialData.Campaigns.remove(remove_item)
            self.update_info()

    def add_segment(self):
        dialog = AddSegmentWindow(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            new_segment = dialog.get_data()
            if new_segment:
                InitialData.AudienceSegments.add(new_segment)
                current_platform_id = self.platforms[self.current_index].platform_id
                segment_id = new_segment.segment_id
                segment_platform = SegmentPlatform(
                    segment_id = segment_id,
                    platform_id=current_platform_id
                )
                InitialData.SegmentPlatforms.add(segment_platform)
                self.update_info()

    def edit_segment(self):
        selected_row = self.segmentsTableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a segment to edit.")
            return

        segment_id = int(
            self.segmentsTableWidget.item(selected_row, 0).text())
        selected_segment = next(
            (s for s in InitialData.AudienceSegments.get_items() if s.segment_id == segment_id),
            None)
        current_platform_id = self.platforms[self.current_index].platform_id
        segment_platform = next(
            (sp for sp in InitialData.SegmentPlatforms.get_items()
             if sp.segment_id == segment_id and sp.platform_id == current_platform_id),
            None
        )
        dialog = AddSegmentWindow(self)
        dialog.set_data(selected_segment)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            updated_segment = dialog.get_data()
            if updated_segment:
                for i, segment in enumerate(InitialData.AudienceSegments.get_items()):
                    if segment.segment_id == segment_id:
                        InitialData.AudienceSegments.update(i, updated_segment)
                        break
                # for i, sp in enumerate(InitialData.SegmentPlatforms.get_items()):
                #     if sp.segment_id == segment_id and sp.platform_id == current_platform_id:
                #         InitialData.CampaignPlatforms.update(i, cp)
                #         break
                self.update_info()

    def remove_segment(self):
        selected_row = self.segmentsTableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a segment to remove.")
            return

        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure you want to delete the selected segment?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            segment_id = int(
                self.segmentsTableWidget.item(selected_row, 0).text())

            for sp in InitialData.SegmentPlatforms.get_items():
                if sp.segment_id == segment_id:
                    InitialData.SegmentPlatforms.remove(sp)

            remove_item = next(
                (s for s in InitialData.AudienceSegments.get_items() if s.segment_id == segment_id),
                None
            )
            if remove_item:
                InitialData.AudienceSegments.remove(remove_item)
            self.update_info()

    def add_advertisement(self):
        dialog = AddAdvertisementWindow(self)
        dialog.set_platform_name(self.platforms[self.current_index].platform_name)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            new_advertisement = dialog.get_data()
            if new_advertisement:
                InitialData.Advertisements.add(new_advertisement)
                self.update_info()

    def edit_advertisement(self):
        selected_row = self.advertisementsTableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select an advertisement to edit.")
            return
        key_value = self.advertisementsTableWidget.item(selected_row, 0).text()
        selected_advertisement = next(
            (ad for ad in InitialData.Advertisements.get_items() if str(ad.GetData()[1][0]) == key_value),
            None
        )
        dialog = AddAdvertisementWindow(self)
        dialog.set_data(selected_advertisement)
        dialog.set_platform_name(self.platforms[self.current_index].platform_name)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            updated_advertisement = dialog.get_data()
            if updated_advertisement:
                advertisement_index = InitialData.Advertisements.get_items().index(selected_advertisement)
                InitialData.Advertisements.update(advertisement_index, updated_advertisement)
                self.update_info()

    def remove_advertisement(self):
        selected_row = self.advertisementsTableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select an advertisement to remove.")
            return

        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure you want to delete the selected advertisement?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            key_value = self.advertisementsTableWidget.item(selected_row, 0).text()
            remove_item = next(
                (ad for ad in InitialData.Advertisements.get_items() if str(ad.GetData()[1][0]) == key_value),
                None
            )
            if remove_item:
                InitialData.Advertisements.remove(remove_item)
            self.update_info()

    def update_info(self):
        if not self.platforms:
            QtWidgets.QMessageBox.warning(self, "Error", "No platforms available.")
            self.close()
            return

        platform = self.platforms[self.current_index]
        self.idLabel.setText(f"ID: {platform.platform_id}")
        self.nameLabel.setText(f"Name: {platform.platform_name or 'N/A'}")
        self.typeLabel.setText(f"Name: {platform.platform_type or 'N/A'}")
        self.formatLabel.setText(f"Name: {platform.main_ad_format or 'N/A'}")
        self.sizeLabel.setText(f"Name: {platform.audience_size or 'N/A'}")
        advertisements = InitialData.Advertisements.find(platform_id=platform.platform_id)
        campaign_platforms = InitialData.CampaignPlatforms.find(platform_id=platform.platform_id)
        segment_platforms = InitialData.SegmentPlatforms.find(platform_id = platform.platform_id)
        if campaign_platforms:
            campaign_ids = [cp.campaign_id for cp in campaign_platforms]
            related_campaigns = [c for c in InitialData.Campaigns.get_items() if c.campaign_id in campaign_ids]
            if related_campaigns:
                headers = related_campaigns[0].GetData()[0]
                headers.append("Budget Allocation")
                budget_map = {cp.campaign_id: cp.budget_allocation for cp in campaign_platforms}
                self.campaignsTableWidget.setRowCount(len(related_campaigns))
                self.campaignsTableWidget.setColumnCount(len(headers))
                self.campaignsTableWidget.setHorizontalHeaderLabels(headers)
                for row_ind, campaign in enumerate(related_campaigns):
                    for col_ind, col_data in enumerate(campaign.GetData()[1]):
                        item = QTableWidgetItem(str(col_data))
                        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        self.campaignsTableWidget.setItem(row_ind, col_ind, item)
                    allocation = budget_map.get(campaign.campaign_id, "")
                    allocation_item = QTableWidgetItem(str(allocation))
                    allocation_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.campaignsTableWidget.setItem(row_ind, len(headers) - 1, allocation_item)
        else:
            self.campaignsTableWidget.clear()
        if segment_platforms:
            segment_ids = [sp.segment_id for sp in segment_platforms]
            related_segments = [s for s in InitialData.AudienceSegments.get_items() if s.segment_id in segment_ids]
            if related_segments:
                headers = related_segments[0].GetData()[0]
                # budget_map = {cp.campaign_id: cp.budget_allocation for cp in campaign_platforms}
                self.segmentsTableWidget.setRowCount(len(related_segments))
                self.segmentsTableWidget.setColumnCount(len(headers))
                self.segmentsTableWidget.setHorizontalHeaderLabels(headers)
                for row_ind, segment in enumerate(related_segments):
                    for col_ind, col_data in enumerate(segment.GetData()[1]):
                        item = QTableWidgetItem(str(col_data))
                        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        self.segmentsTableWidget.setItem(row_ind, col_ind, item)
        else:
            self.segmentsTableWidget.clear()

        if advertisements:
            headers = advertisements[0].GetData()[0]
            updated_headers = []
            for header in headers:
                if header == "Campaign ID":
                    updated_headers.append("Campaign Name")
                elif header == "Platform ID":
                    continue
                else:
                    updated_headers.append(header)
            campaign_map = {campaign.campaign_id: campaign.campaign_name for campaign in
                            InitialData.Campaigns.get_items()}
            campaign_id_index = advertisements[0].GetData()[0].index("Campaign ID")
            platform_id_index = advertisements[0].GetData()[0].index("Platform ID")
            self.advertisementsTableWidget.setRowCount(len(advertisements))
            self.advertisementsTableWidget.setColumnCount(len(updated_headers))
            self.advertisementsTableWidget.setHorizontalHeaderLabels(updated_headers)
            for row_ind, row_data in enumerate(advertisements):
                for col_ind, col_data in enumerate(row_data.GetData()[1]):
                    if col_ind == platform_id_index:
                        continue
                    elif col_ind == campaign_id_index:
                        campaign_name = campaign_map.get(col_data, "")
                        item = QTableWidgetItem(campaign_name)
                    else:
                        item = QTableWidgetItem(str(col_data))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    adjusted_col_ind = col_ind if col_ind < platform_id_index else col_ind - 1
                    self.advertisementsTableWidget.setItem(row_ind, adjusted_col_ind, item)
        else:
            self.advertisementsTableWidget.clear()

    def navigate_next(self):
        if self.current_index < len(self.platforms) - 1:
            self.current_index += 1
            self.update_info()
        else:
            QtWidgets.QMessageBox.information(self, "Info", "This is the last platform.")

    def navigate_previous(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_info()
        else:
            QtWidgets.QMessageBox.information(self, "Info", "This is the first platform.")

    def edit_platform(self):
        dialog = AddPlatformWindow(self)
        current_platform = self.platforms[self.current_index]
        if not current_platform:
            QtWidgets.QMessageBox.warning(self, "Error", "Could not retrieve item for editing")
            return
        # print(self.campaigns[self.current_index])
        dialog.set_data(current_platform)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            updated_platform = dialog.get_data()
            if updated_platform:
                platform_id = current_platform.platform_id
                for i, platform in enumerate(InitialData.MediaPlatforms.get_items()):
                    if platform.platform_id == platform_id:
                        InitialData.MediaPlatforms.update(i, updated_platform)
                        break
                self.update_info()

    def go_back(self):
        if self.update_callback:
            self.update_callback()
        self.parent().show()
        self.close()


class SegmentWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, segment: AudienceSegment = None, update_callback = None):
        super().__init__(parent)
        uic.loadUi("SegmentWindow.ui", self)

        self.segments = InitialData.AudienceSegments.get_items()
        self.current_index = self.segments.index(segment) if segment else 0
        self.update_callback = update_callback
        self.update_info()
        self.nextButton.clicked.connect(self.navigate_next)
        self.previousButton.clicked.connect(self.navigate_previous)
        self.editButton.clicked.connect(self.edit_segment)
        self.backButton.clicked.connect(self.go_back)
        self.addPlatformButton.clicked.connect(self.add_platform)
        self.editPlatformButton.clicked.connect(self.edit_platform)
        self.removePlatformButton.clicked.connect(self.remove_platform)
        self.addUserButton.clicked.connect(self.add_user)
        self.editUserButton.clicked.connect(self.edit_user)
        self.removeUserButton.clicked.connect(self.remove_user)
        self.addExistingPlatformButton.clicked.connect(self.add_existing_platform)
        self.addExistingUserButton.clicked.connect(self.add_existing_user)
        self.removePlatformFromSegmentButton.clicked.connect(self.remove_platform_from_segment)
        self.removeUserFromSegmentButton.clicked.connect(self.remove_user_from_segment)

    def remove_platform_from_segment(self):
        selected_row = self.platformsTableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a platform to remove from the segment.")
            return
        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure you want to remove the selected platform from this segment?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            platform_id = int(
                self.platformsTableWidget.item(selected_row, 0).text()
            )
            current_segment_id = self.segments[self.current_index].segment_id
            segment_platform = next(
                (sp for sp in InitialData.SegmentPlatforms.get_items()
                 if sp.segment_id == current_segment_id and sp.platform_id == platform_id),
                None
            )
            if segment_platform:
                InitialData.SegmentPlatforms.remove(segment_platform)
            self.update_info()

    def remove_user_from_segment(self):
        selected_row = self.usersTableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a user to remove from the segment.")
            return
        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure you want to remove the selected user from this segment?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            user_email = self.usersTableWidget.item(selected_row, 0).text()
            user = next(
                (user for user in InitialData.Users.get_items() if user.email == user_email),
                None
            )
            if user:
                user.segment_id = None
                user_index = InitialData.Users.get_items().index(user)
                InitialData.Advertisements.update(user_index, user)
            self.update_info()

    def add_existing_platform(self):
        dialog = SelectExistingItemDialog(self)
        current_segment_id = self.segments[self.current_index].segment_id
        used_platform_ids = [
            sp.platform_id for sp in InitialData.SegmentPlatforms.get_items() if sp.segment_id == current_segment_id
        ]
        available_platforms = [
            platform for platform in InitialData.MediaPlatforms.get_items() if
            platform.platform_id not in used_platform_ids
        ]
        dialog.configure_dialog(
            items=available_platforms,
            label_text="Platforms"
        )
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            selected_platform = dialog.get_selected_item()
            if selected_platform:
                platform_id = selected_platform.platform_id
                segmend_platform = SegmentPlatform(
                    segment_id=current_segment_id,
                    platform_id=platform_id
                )
                InitialData.SegmentPlatforms.add(segmend_platform)
                self.update_info()

    def add_existing_user(self):
        dialog = SelectExistingSingleItemDialog(self)
        available_users = [user for user in InitialData.Users.get_items() if user.segment_id is None]
        dialog.configure_dialog(available_users, "User emails")
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            selected_user = dialog.get_selected_item()
            if selected_user:
                current_segment_id = self.segments[self.current_index].segment_id
                selected_user.segment_id = current_segment_id
                user_index = InitialData.Users.get_items().index(selected_user)
                InitialData.Users.update(user_index, selected_user)
                self.update_info()

    def add_platform(self):
        dialog = AddPlatformWindow(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            new_platform = dialog.get_data()
            if new_platform:
                InitialData.MediaPlatforms.add(new_platform)
                current_segment_id = self.segments[self.current_index].segment_id
                platform_id = new_platform.platform_id
                segment_platform = SegmentPlatform(
                    segment_id=current_segment_id,
                    platform_id=platform_id
                )
                InitialData.SegmentPlatforms.add(segment_platform)
                self.update_info()

    def edit_platform(self):
        selected_row = self.platformsTableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a platform to edit.")
            return

        platform_id = int(
            self.platformsTableWidget.item(selected_row, 0).text())
        selected_platform = next(
            (p for p in InitialData.MediaPlatforms.get_items() if p.platform_id == platform_id),
            None)
        current_segment_id = self.segments[self.current_index].segment_id
        segment_platform = next(
            (sp for sp in InitialData.SegmentPlatforms.get_items()
             if sp.segment_id == current_segment_id and sp.platform_id == platform_id),
            None
        )
        dialog = AddPlatformWindow(self)
        dialog.set_data(selected_platform)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            updated_platform = dialog.get_data()
            if updated_platform:
                for i, platform in enumerate(InitialData.MediaPlatforms.get_items()):
                    if platform.platform_id == platform_id:
                        InitialData.MediaPlatforms.update(i, updated_platform)
                        break
                # for i, sp in enumerate(InitialData.SegmentPlatforms.get_items()):
                #     if sp.segment_id == current_segment_id and sp.platform_id == platform_id:
                #         InitialData.SegmentPlatforms.update(i, sp)
                #         break
                self.update_info()

    def remove_platform(self):
        selected_row = self.platformsTableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a platform to remove.")
            return

        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure you want to delete the selected platform?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            platform_id = int(
                self.platformsTableWidget.item(selected_row, 0).text())

            for sp in InitialData.SegmentPlatforms.get_items():
                if sp.platform_id == platform_id:
                    InitialData.SegmentPlatforms.remove(sp)

            remove_item = next(
                (p for p in InitialData.MediaPlatforms.get_items() if p.platform_id == platform_id),
                None
            )
            if remove_item:
                InitialData.MediaPlatforms.remove(remove_item)
            self.update_info()

    def add_user(self):
        dialog = AddUserWindow(self)
        dialog.set_segment_name(self.segments[self.current_index].segment_name)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            new_user = dialog.get_data()
            if new_user:
                InitialData.Users.add(new_user)
                self.update_info()

    def edit_user(self):
        selected_row = self.usersTableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a user to edit.")
            return
        key_value = self.usersTableWidget.item(selected_row, 0).text()
        selected_user = next(
            (u for u in InitialData.Users.get_items() if str(u.GetData()[1][0]) == key_value),
            None
        )
        dialog = AddUserWindow(self)
        dialog.set_data(selected_user)
        dialog.set_segment_name(self.segments[self.current_index].segment_name)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            updated_user = dialog.get_data()
            if updated_user:
                user_index = InitialData.Users.get_items().index(selected_user)
                InitialData.Users.update(user_index, updated_user)
                self.update_info()


    def remove_user(self):
        selected_row = self.usersTableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a user to remove.")
            return

        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure you want to delete the selected user?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            key_value = self.usersTableWidget.item(selected_row, 0).text()
            remove_item = next(
                (u for u in InitialData.Users.get_items() if str(u.GetData()[1][0]) == key_value),
                None
            )
            if remove_item:
                InitialData.Users.remove(remove_item)
            self.update_info()

    def update_info(self):
        if not self.segments:
            QtWidgets.QMessageBox.warning(self, "Error", "No segments available.")
            self.close()
            return

        segment = self.segments[self.current_index]
        self.idLabel.setText(f"ID: {segment.segment_id}")
        self.nameLabel.setText(f"Name: {segment.segment_name}")
        self.ageRangeLabel.setText(f"Age range: {segment.age_range}")
        self.genderLabel.setText(f"Gender: {segment.gender}")
        self.locationLabel.setText(f"Location: {segment.location}")
        self.interestLabel.setText(f"General interest: {segment.general_interest}")
        self.statusLabel.setText(f"Socioeconomic status: {segment.socioeconomic_status}")
        self.languageLabel.setText(f"Language: {segment.language}")
        self.characteristicsLabel.setText(f"Behavioral characteristics: {segment.behavioral_characteristics}")
        self.deviceLabel.setText(f"Used device: {segment.device_used}")
        users = InitialData.Users.find(segment_id =segment.segment_id)
        segment_platforms = InitialData.SegmentPlatforms.find(segment_id=segment.segment_id)
        if segment_platforms:
            platform_ids = [sp.platform_id for sp in segment_platforms]
            related_platforms = [p for p in InitialData.MediaPlatforms.get_items() if p.platform_id in platform_ids]
            if related_platforms:
                headers = related_platforms[0].GetData()[0]
                self.platformsTableWidget.setRowCount(len(related_platforms))
                self.platformsTableWidget.setColumnCount(len(headers))
                self.platformsTableWidget.setHorizontalHeaderLabels(headers)
                for row_ind, platform in enumerate(related_platforms):
                    for col_ind, col_data in enumerate(platform.GetData()[1]):
                        item = QTableWidgetItem(str(col_data))
                        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        self.platformsTableWidget.setItem(row_ind, col_ind, item)
        else:
            self.platformsTableWidget.clear()
        if users:
            headers = users[0].GetData()[0]
            updated_headers = []
            for header in headers:
                if header == "Segment ID":
                    continue
                else:
                    updated_headers.append(header)
            # platform_map = {platform.platform_id: platform.platform_name for platform in
            #                 InitialData.MediaPlatforms.get_items()}
            user_id_index = users[0].GetData()[0].index("Segment ID")
            self.usersTableWidget.setRowCount(len(users))
            self.usersTableWidget.setColumnCount(len(updated_headers))
            self.usersTableWidget.setHorizontalHeaderLabels(updated_headers)
            for row_ind, row_data in enumerate(users):
                for col_ind, col_data in enumerate(row_data.GetData()[1]):
                    if col_ind == user_id_index:
                        continue
                    else:
                        item = QTableWidgetItem(str(col_data))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    adjusted_col_ind = col_ind if col_ind < user_id_index else col_ind - 1
                    self.usersTableWidget.setItem(row_ind, adjusted_col_ind, item)
        else:
            self.usersTableWidget.clear()

    def navigate_next(self):
        if self.current_index < len(self.segments) - 1:
            self.current_index += 1
            self.update_info()
        else:
            QtWidgets.QMessageBox.information(self, "Info", "This is the last segment.")

    def navigate_previous(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_info()
        else:
            QtWidgets.QMessageBox.information(self, "Info", "This is the first segment.")

    def edit_segment(self):
        dialog = AddSegmentWindow(self)
        current_segment = self.segments[self.current_index]
        if not current_segment:
            QtWidgets.QMessageBox.warning(self, "Error", "Could not retrieve item for editing")
            return
        # print(self.campaigns[self.current_index])
        dialog.set_data(current_segment)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            updated_segment = dialog.get_data()
            if updated_segment:
                segment_id = current_segment.segment_id
                for i, segment in enumerate(InitialData.AudienceSegments.get_items()):
                    if segment.segment_id == segment_id:
                        InitialData.AudienceSegments.update(i, updated_segment)
                        break
                self.update_info()

    def go_back(self):
        if self.update_callback:
            self.update_callback()
        self.parent().show()
        self.close()


class AdvertisementWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, advertisement: Advertisement = None, update_callback = None):
        super().__init__(parent)
        uic.loadUi("AdvertisementWindow.ui", self)

        self.advertisements = InitialData.Advertisements.get_items()
        self.current_index = self.advertisements.index(advertisement) if advertisement else 0
        self.update_callback = update_callback
        self.update_info()
        self.nextButton.clicked.connect(self.navigate_next)
        self.previousButton.clicked.connect(self.navigate_previous)
        self.editButton.clicked.connect(self.edit_advertisement)
        self.backButton.clicked.connect(self.go_back)


    def update_info(self):
        if not self.advertisements:
            QtWidgets.QMessageBox.warning(self, "Error", "No advertisements available.")
            self.close()
            return

        advertisement : Advertisement = self.advertisements[self.current_index]
        self.idLabel.setText(f"ID: {advertisement.advertisement_id}")
        self.textLabel.setText(f"Text: {advertisement.text}")
        self.formatLabel.setText(f"Format: {advertisement.format}")
        self.sendTimeLabel.setText(f"Send Time: {advertisement.send_time}")
        self.topicLabel.setText(f"Topic: {advertisement.topic}")
        self.languageLabel.setText(f"Language: {advertisement.language}")
        self.attachmentLabel.setText(f"Attachment: {advertisement.attachment}")
        self.clicksLabel.setText(f"Clicks: {advertisement.clicks}")
        self.viewsLabel.setText(f"Views: {advertisement.views}")
        campaign_name = next(
            (campaign.campaign_name for campaign in InitialData.Campaigns.get_items()
             if campaign.campaign_id == advertisement.campaign_id),
            "Unknown Campaign"
        )
        self.campaignLabel.setText(f"Campaign: {campaign_name}")
        platform_name = next(
            (platform.platform_name for platform in InitialData.MediaPlatforms.get_items()
             if platform.platform_id == advertisement.platform_id),
            "Unknown Platform"
        )
        self.platformLabel.setText(f"Platform: {platform_name}")


    def navigate_next(self):
        if self.current_index < len(self.advertisements) - 1:
            self.current_index += 1
            self.update_info()
        else:
            QtWidgets.QMessageBox.information(self, "Info", "This is the last advertisement.")

    def navigate_previous(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_info()
        else:
            QtWidgets.QMessageBox.information(self, "Info", "This is the first advertisement.")

    def edit_advertisement(self):
        dialog = AddAdvertisementWindow(self)
        current_advertisement = self.advertisements[self.current_index]
        if not current_advertisement:
            QtWidgets.QMessageBox.warning(self, "Error", "Could not retrieve item for editing")
            return
        # print(self.campaigns[self.current_index])
        dialog.set_data(current_advertisement)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            updated_advertisement = dialog.get_data()
            if updated_advertisement:
                advertisement_id = current_advertisement.advertisement_id
                for i, advertisement in enumerate(InitialData.Advertisements.get_items()):
                    if advertisement.advertisement_id == advertisement_id:
                        InitialData.Advertisements.update(i, updated_advertisement)
                        break
                self.update_info()

    def go_back(self):
        if self.update_callback:
            self.update_callback()
        self.parent().show()
        self.close()


class UserWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, user: User = None, update_callback=None):
        super().__init__(parent)
        uic.loadUi("UserWindow.ui", self)
        self.users = InitialData.Users.get_items()
        self.current_index = self.users.index(user) if user else 0
        self.update_callback = update_callback
        self.update_info()
        self.nextButton.clicked.connect(self.navigate_next)
        self.previousButton.clicked.connect(self.navigate_previous)
        self.editButton.clicked.connect(self.edit_user)
        self.backButton.clicked.connect(self.go_back)

    def update_info(self):
        if not self.users:
            QtWidgets.QMessageBox.warning(self, "Error", "No users available.")
            self.close()
            return
        user: User = self.users[self.current_index]
        self.emailLabel.setText(f"Email: {user.email}")
        self.passwordLabel.setText(f"Password: {user.password}")
        self.ageLabel.setText(f"Age: {user.age}")
        self.genderLabel.setText(f"Gender: {user.gender}")
        self.countryLabel.setText(f"Country: {user.country}")
        self.accountCreationDateLabel.setText(f"Account creation date: {user.account_creation_date}")
        self.lastPurchaseDateLabel.setText(f"Last purchase date: {user.last_purchase_date}")
        segment_name = next(
            (segment.segment_name for segment in InitialData.AudienceSegments.get_items()
             if segment.segment_id == user.segment_id),
            "Unknown Segment"
        )
        self.segmentLabel.setText(f"Audience Segment: {segment_name}")

    def navigate_next(self):
        if self.current_index < len(self.users) - 1:
            self.current_index += 1
            self.update_info()
        else:
            QtWidgets.QMessageBox.information(self, "Info", "This is the last user.")

    def navigate_previous(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_info()
        else:
            QtWidgets.QMessageBox.information(self, "Info", "This is the first user.")

    def edit_user(self):
        dialog = AddUserWindow(self)
        current_user = self.users[self.current_index]
        if not current_user:
            QtWidgets.QMessageBox.warning(self, "Error", "Could not retrieve user for editing")
            return

        dialog.set_data(current_user)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            updated_user = dialog.get_data()
            if updated_user:
                user_email = current_user.email
                for i, user in enumerate(InitialData.Users.get_items()):
                    if user.email == user_email:
                        InitialData.Users.update(i, updated_user)
                        break
                self.update_info()

    def go_back(self):
        if self.update_callback:
            self.update_callback()
        self.parent().show()
        self.close()
