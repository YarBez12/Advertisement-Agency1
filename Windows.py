
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


class AddCampaignWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("AddCampaignWindow.ui", self)
        self.startDateEdit.setCalendarPopup(True)
        self.endDateEdit.setCalendarPopup(True)
        self.startDateButton.clicked.connect(self.toggle_start_date)
        self.endDateButton.clicked.connect(self.toggle_end_date)
        self.budgetButton.clicked.connect(self.toggle_budget)
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
            if deleted_key:
                self.__controller.update_table(self.__controller.current_data)

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
                self.__controller.update_table(self.__controller.current_data)


    def open_info_window(self) -> None:
        windows = {
            # "Clients": ClientWindow,
            "Campaigns": CampaignWindow,
            # "Advertisements": AdvertisementWindow,
            # "Media Platforms": PlatformWindow,
            # "Audience Segments": SegmentWindow,
            # "Users": UserWindow
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
        print(self.campaigns[self.current_index])
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



