
from PyQt5.QtCore import Qt

from Windows import *
from Models import Campaign, Advertisement, Client
import InitialData


class AddAdvertisementWindowController:
    def __init__(self, window):
        self.__window = window

    def update_attachment_line_edit(self, file_path):
        if file_path:
            self.__window.attachmentLineEdit.setText(file_path)

    def select_max_id_from_table(self) -> int:

        if not InitialData.Advertisements.get_items():
            return -1
        try:
            max_id = max(ad.advertisement_id for ad in InitialData.Advertisements.get_items())
            return max_id
        except ValueError:
            return -1


    def validate_window(self) -> bool:
        advertisement_topic = self.__window.topicLineEdit.text().strip()
        if not advertisement_topic:
            return False
        return True

    def get_data(self) -> Optional[Advertisement]:
        campaign_name = self.__window.campaignComboBox.currentText().strip()
        campaign = next((c for c in InitialData.Campaigns.get_items() if c.name == campaign_name), None)
        return Advertisement(
            advertisement_id=int(self.__window.idLineEdit.text().strip()),
            text=self.__window.textLineEdit.text().strip(),
            format=self.__window.formatComboBox.currentText(),
            send_time=self.__window.sendDateEdit.date().toString("yyyy-MM-dd"),
            topic=self.__window.topicLineEdit.text().strip(),
            language=self.__window.languageComboBox.currentText(),
            attachment=self.__window.attachmentLineEdit.text().strip(),
            clicks=int(
                self.__window.clicksLineEdit.text().strip()) if self.__window.clicksLineEdit.text().strip() else None,
            views=int(
                self.__window.viewsLineEdit.text().strip()) if self.__window.viewsLineEdit.text().strip() else None,
            campaign_id=campaign.campaign_id
        )

    def reset_data(self):
        max_id = self.select_max_id_from_table()
        self.__window.idLineEdit.setText(str(max_id + 1))
        self.__window.textLineEdit.clear()
        self.__window.formatComboBox.setCurrentIndex(0)
        self.__window.sendDateEdit.setDate(QDate.currentDate().addMonths(1))
        self.__window.topicLineEdit.clear()
        self.__window.languageComboBox.setCurrentIndex(0)
        self.__window.attachmentLineEdit.clear()
        self.__window.clicksLineEdit.clear()
        self.__window.viewsLineEdit.clear()
        self.__window.campaignComboBox.setCurrentIndex(0)

    def set_data(self, advertisement: Advertisement) -> None:
        self.__window.idLineEdit.setText(str(advertisement.advertisement_id))
        self.__window.textLineEdit.setText(advertisement.text or "")
        self.__window.formatComboBox.setCurrentText(advertisement.format or "")
        self.__window.sendDateEdit.setDate(
            QDate.fromString(advertisement.send_time, "yyyy-MM-dd") if advertisement.send_time else QDate.currentDate())
        self.__window.topicLineEdit.setText(advertisement.topic or "")
        self.__window.languageComboBox.setCurrentText(advertisement.language or "")
        self.__window.attachmentLineEdit.setText(advertisement.attachment or "")
        self.__window.clicksLineEdit.setText(str(advertisement.clicks) if advertisement.clicks is not None else "")
        self.__window.viewsLineEdit.setText(str(advertisement.views) if advertisement.views is not None else "")
        campaign = next((c for c in InitialData.Campaigns.get_items() if c.campaign_id == advertisement.campaign_id), None)
        if campaign:
            self.__window.campaignComboBox.setCurrentText(campaign.name)
        else:
            self.__window.campaignComboBox.setCurrentText("")

    def set_campaign_name(self, campaign_name: int):
        self.__window.campaignComboBox.setCurrentText(str(campaign_name))
        self.__window.campaignComboBox.setEnabled(False)


class AddCampaignWindowController:
    def __init__(self, window):
        self.__window = window

    def select_max_id_from_table(self) -> int:
        if not InitialData.Campaigns.get_items():
            return -1
        try:
            max_id = max(c.campaign_id for c in InitialData.Campaigns.get_items())
            return max_id
        except ValueError:
            return -1

    def validate_window(self) -> bool:
        campaign_goal = self.__window.goalLineEdit.text().strip()
        if not campaign_goal:
            return False
        return True

    def get_data(self) -> Optional[Campaign]:
        return Campaign(
            campaign_id=int(self.__window.idLineEdit.text().strip()),
            name=self.__window.nameLineEdit.text().strip(),
            start_date=self.__window.startDateEdit.date().toString("yyyy-MM-dd"),
            end_date=self.__window.endDateEdit.date().toString("yyyy-MM-dd"),
            goal=self.__window.goalLineEdit.text().strip(),
            budget=self.__window.budgetSpinBox.value(),
            company_name=self.__window.companyComboBox.currentText(),
        )

    def reset_data(self) -> None:
        max_id = self.select_max_id_from_table()
        self.__window.idLineEdit.setText(str(max_id + 1))
        self.__window.nameLineEdit.setPlaceholderText(f"Campaign #{max_id + 1}")
        self.__window.startDateEdit.setDate(QDate.currentDate())
        self.__window.endDateEdit.setDate(QDate.currentDate().addYears(5))
        self.__window.goalLineEdit.clear()
        self.__window.budgetSpinBox.setValue(1000)
        self.__window.companyComboBox.setCurrentIndex(0)

    def set_data(self, campaign: Campaign) -> None:
        self.__window.idLineEdit.setText(str(campaign.campaign_id))
        self.__window.nameLineEdit.setText(campaign.name or "")
        self.__window.startDateEdit.setDate(QDate.fromString(campaign.start_date, "yyyy-MM-dd"))
        self.__window.endDateEdit.setDate(QDate.fromString(campaign.end_date, "yyyy-MM-dd"))
        self.__window.goalLineEdit.setText(campaign.goal or "")
        self.__window.budgetSpinBox.setValue(campaign.budget or 0)
        self.__window.companyComboBox.setCurrentText(campaign.company_name or "")


class AddClientWindowController:
    def __init__(self, window):
        self.__window = window

    def validate_window(self) -> bool:
        client_name = self.__window.nameLineEdit.text().strip()
        client_phone = self.__window.phoneLineEdit.text().strip()
        client_email = self.__window.emailLineEdit.text().strip()
        if not client_name or not client_phone or not client_email:
            return False
        return True

    def get_data(self) -> Optional[Client]:

        return Client(
            company_name=self.__window.nameLineEdit.text().strip(),
            phone=self.__window.phoneLineEdit.text().strip(),
            email=self.__window.emailLineEdit.text().strip(),
            address=self.__window.addressLineEdit.text().strip(),
            type=self.__window.typeComboBox.currentText(),
            business_area=self.__window.areaComboBox.currentText(),
            available_budget=self.__window.budgetSpinBox.value()
        )

    def reset_data(self) -> None:
        self.__window.nameLineEdit.clear()
        self.__window.phoneLineEdit.clear()
        self.__window.emailLineEdit.clear()
        self.__window.addressLineEdit.clear()
        self.__window.typeComboBox.setCurrentIndex(0)
        self.__window.areaComboBox.setCurrentIndex(0)
        self.__window.budgetSpinBox.setValue(0)

    def set_data(self, client) -> None:
        self.__window.nameLineEdit.setText(client.company_name or "")
        self.__window.phoneLineEdit.setText(client.phone or "")
        self.__window.emailLineEdit.setText(client.email or "")
        self.__window.addressLineEdit.setText(client.address or "")
        self.__window.typeComboBox.setCurrentText(client.type or "")
        self.__window.areaComboBox.setCurrentText(client.business_area or "")
        self.__window.budgetSpinBox.setValue(client.available_budget or 0)


class TablesWindowController:
    def __init__(self, window):
        self.__window = window
        self.current_data = InitialData.Clients

    def fill_table(self, data) -> None:
        headers = data[0].GetData()[0]
        self.__window.dataTableWidget.setRowCount(len(data))
        self.__window.dataTableWidget.setColumnCount(len(headers))
        self.__window.dataTableWidget.setHorizontalHeaderLabels(headers)
        for row_ind, row_data in enumerate(data.get_items()):
            for col_ind, col_data in enumerate(row_data.GetData()[1]):
                item = QTableWidgetItem(str(col_data))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.__window.dataTableWidget.setItem(row_ind, col_ind, item)

    def update_table(self, data) -> None:
        self.fill_table(data)
        self.__window.databaseNameLabel.setText(data.get_str_models_name())
        self.current_data = data

    def navigate_first(self) -> None:
        if self.__window.dataTableWidget.rowCount() > 0:
            self.__window.dataTableWidget.selectRow(0)

    def navigate_previous(self) -> None:
        current_row = self.__window.dataTableWidget.currentRow()
        if current_row > 0:
            self.__window.dataTableWidget.selectRow(current_row - 1)

    def navigate_next(self) -> None:
        current_row = self.__window.dataTableWidget.currentRow()
        if current_row < self.__window.dataTableWidget.rowCount() - 1:
            self.__window.dataTableWidget.selectRow(current_row + 1)

    def navigate_last(self) -> None:
        if self.__window.dataTableWidget.rowCount() > 0:
            self.__window.dataTableWidget.selectRow(self.__window.dataTableWidget.rowCount() - 1)

    # def remove_item(self) -> None:
    #     table_name = self.current_data.get_str_models_name()
    #     key_columns = {
    #         "Clients": "company_name",
    #         "Campaigns": "campaign_id",
    #         "Advertisements": "advertisement_id"
    #     }
    #     selected_row = self.__window.dataTableWidget.currentRow()
    #     if selected_row != -1:
    #         key_value = self.__window.dataTableWidget.item(selected_row, 0).text()
    #         reply = QtWidgets.QMessageBox.question(
    #             self.__window,
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

    def remove_item(self, selected_row: int) -> Optional[str]:
        if selected_row == -1:
            return None

        key_value = self.__window.dataTableWidget.item(selected_row, 0).text()
        remove_item = next(
            (item for item in self.current_data.get_items() if str(item.GetData()[1][0]) == key_value),
            None
        )
        if remove_item:
            self.current_data.remove(remove_item)
            return key_value
        return None

    def get_item_for_edit(self, selected_row: int) -> Optional[Any]:
        if selected_row == -1:
            return None

        return self.current_data.get_items()[selected_row]

    def save_item(self, data: Any, edit: bool, selected_row: Optional[int] = None) -> None:
        if edit and selected_row is not None:
            self.current_data.update(selected_row, data)
        else:
            self.current_data.add(data)

    # def open_item_dialog(self, edit: bool = False) -> None:
    #     dialogs = {
    #         "Clients": AddClientWindow,
    #         "Campaigns": AddCampaignWindow,
    #         "Advertisements": AddAdvertisementWindow
    #     }
    #     table_name = self.current_data.get_str_models_name()
    #     dialog_class = dialogs.get(table_name)
    #     if not dialog_class:
    #         return
    #     if edit:
    #         selected_row = self.__window.dataTableWidget.currentRow()
    #         if selected_row == -1:
    #             QtWidgets.QMessageBox.warning(self.__window, "No data", "Please select a row to edit")
    #             return
    #         edit_item = self.current_data.get_items()[selected_row]
    #         dialog = dialog_class(self.__window)
    #         dialog.set_data(edit_item)
    #     else:
    #         dialog = dialog_class(self.__window)
    #     if dialog.exec_() == QtWidgets.QDialog.Accepted:
    #         data = dialog.get_data()
    #         if data:
    #             if edit:
    #                 self.current_data.update(selected_row, data)
    #             else:
    #                 self.current_data.add(data)
    #             self.update_table(self.current_data)
