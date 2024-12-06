
from PyQt5 import QtWidgets, uic
from typing import Tuple, Optional, List, Any
from PyQt5.QtCore import QDate, QTimer
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

import InitialData
from Controllers import *
from DatabaseController import DatabaseController
from Models import *


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
        self.resetButton.clicked.connect(self.reset_data)
        self.campaignComboBox.addItems([campaign.campaign_name for campaign in InitialData.Campaigns.get_items()])
        self.platformComboBox.addItems([platform.platform_name for platform in InitialData.MediaPlatforms.get_items()])
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
        self.resetButton.clicked.connect(self.reset_data)
        self.budgetAllocationLabel.hide()
        self.budgetAllocationSpinBox.hide()
        self.reset_data()

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

    def set_data(self, platform) -> None:
        self.__controller.set_data(platform)

    def reset_data(self):
        self.__controller.reset_data()

    def show_budget_allocation(self):
        self.budgetAllocationLabel.show()
        self.budgetAllocationSpinBox.show()

    def set_budget_allocation(self, value):
        self.show_budget_allocation()
        self.budgetAllocationSpinBox.setValue(value)

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
        self.resetButton.clicked.connect(self.reset_data)
        self.reset_data()

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
        self.segmentComboBox.addItems([segment.segment_name for segment in InitialData.AudienceSegments.get_items()])
        self.saveButton.clicked.connect(self.save)
        self.cancelButton.clicked.connect(self.reject)
        self.__controller = AddUserWindowController(self)
        self.resetButton.clicked.connect(self.reset_data)
        self.reset_data()

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
        self.budgetAllocationLabel.hide()
        self.budgetAllocationSpinBox.hide()
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
        self.budgetSpinBox.setEnabled(False)
        self.startDateEdit.setEnabled(False)
        self.endDateEdit.setEnabled(False)
        self.startDateButton.setText("Add Date")
        self.endDateButton.setText("Add Date")
        self.budgetButton.setText("Add budget")

    def set_data(self, campaign: Campaign) -> None:
        self.__controller.set_data(campaign)
        self.startDateButton.setText("Remove Date" if campaign.start_date else "Add Date")
        self.endDateButton.setText("Remove Date" if campaign.end_date else "Add Date")
        self.budgetButton.setText("Remove budget" if campaign.budget is not None else "Add budget")

    def toggle_start_date(self) -> None:
        if self.startDateEdit.isEnabled():
            self.startDateEdit.setEnabled(False)
            self.startDateEdit.setStyleSheet("background-color: lightgray;")
            self.startDateButton.setText("Add Date")
        else:
            self.startDateEdit.setEnabled(True)
            self.startDateEdit.setStyleSheet("")
            self.startDateButton.setText("Remove Date")

    def toggle_end_date(self) -> None:
        if self.endDateEdit.isEnabled():
            self.endDateEdit.setEnabled(False)
            self.endDateEdit.setStyleSheet("background-color: lightgray;")
            self.endDateButton.setText("Add Date")
        else:
            self.endDateEdit.setEnabled(True)
            self.endDateEdit.setStyleSheet("")
            self.endDateButton.setText("Remove Date")

    def toggle_budget(self) -> None:
        if self.budgetSpinBox.isEnabled():
            self.budgetSpinBox.setEnabled(False)
            self.budgetSpinBox.setStyleSheet("background-color: lightgray;")
            self.budgetButton.setText("Add budget")
        else:
            self.budgetSpinBox.setEnabled(True)
            self.budgetSpinBox.setStyleSheet("")
            self.budgetButton.setText("Remove budget")

    def set_client_name(self, client_name):
        self.companyComboBox.setCurrentText(str(client_name))
        self.companyComboBox.setEnabled(False)

    def show_budget_allocation(self):
        self.budgetAllocationLabel.show()
        self.budgetAllocationSpinBox.show()

    def set_budget_allocation(self, value):
        self.show_budget_allocation()
        self.budgetAllocationSpinBox.setValue(value)

class AddClientWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("AddClientWindow.ui", self)
        self.typeComboBox.addItems(["Individual", "Company"])
        self.areaComboBox.addItems(InitialData.CLIENT_AREAS)
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
        super().__init__()
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

    def add_platform(self):
        dialog = AddPlatformWindow(self)
        dialog.show_budget_allocation()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            new_platform = dialog.get_data()
            if new_platform:
                InitialData.MediaPlatforms.add(new_platform)
                current_campaign_id = self.campaigns[self.current_index].campaign_id
                platform_id = new_platform.platform_id
                budget_allocation = dialog.budgetAllocationSpinBox.value()
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
            updated_budget_allocation = dialog.budgetAllocationSpinBox.value()
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

    def add_campaign(self):
        dialog = AddCampaignWindow(self)
        dialog.show_budget_allocation()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            new_campaign = dialog.get_data()
            if new_campaign:
                InitialData.Campaigns.add(new_campaign)
                current_platform_id = self.platforms[self.current_index].platform_id
                campaign_id = new_campaign.campaign_id
                budget_allocation = dialog.budgetAllocationSpinBox.value()
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
            updated_budget_allocation = dialog.budgetAllocationSpinBox.value()
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
