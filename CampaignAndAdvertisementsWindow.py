from PyQt5 import QtWidgets, uic
from typing import List, Tuple, Any, Optional

from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QTableWidgetItem

from DatabaseController import DatabaseController
from AddAdvertisementWindow import AddAdvertisementWindow


class CampaignAndAdvertisementsWindow(QtWidgets.QDialog):
    def __init__(self, db_manager: DatabaseController, parent=None):
        super().__init__(parent)
        uic.loadUi("campaignAndAdvertisementsWindow.ui", self)
        self.db_manager = db_manager
        self.load_campaigns()
        self.nextButton.clicked.connect(self.navigate_next)
        self.previousButton.clicked.connect(self.navigate_previous)
        self.saveButton.clicked.connect(self.save_changes)
        self.addButton.clicked.connect(self.add_advertisement)
        self.editButton.clicked.connect(self.edit_advertisement)
        self.removeButton.clicked.connect(self.remove_advertisement)

    def load_campaigns(self) -> None:
        query = "SELECT * FROM Campaigns ORDER BY campaign_id;"
        headers, data = self.db_manager.fetch_data(query)
        self.campaign_data = data
        self.current_campaign_index = 0
        all_client_names = self.get_client_names()
        self.companyComboBox.addItems(all_client_names)
        if data:
            self.display_campaign(self.current_campaign_index)

    def get_client_names(self) -> List[str]:
        query = "SELECT company_name FROM Clients;"
        try:
            _, rows = self.db_manager.fetch_data(query)
            client_names = [row[0] for row in rows]
            return client_names
        except Exception:
            return []

    def display_campaign(self, index: int) -> None:
        if 0 <= index < len(self.campaign_data):
            campaign = self.campaign_data[index]
            self.idLineEdit.setText(str(campaign[0]))
            self.nameLineEdit.setText(campaign[1] if campaign[1] else "")
            self.startDateEdit.setDate(
                QDate.fromString(campaign[2].strftime("%Y-%m-%d"), "yyyy-MM-dd") if campaign[2] else QDate.currentDate()
            )
            self.endDateEdit.setDate(
                QDate.fromString(campaign[3].strftime("%Y-%m-%d"), "yyyy-MM-dd") if campaign[3] else QDate.currentDate()
            )
            self.goalLineEdit.setText(campaign[4] if campaign[4] else "")
            self.budgetSpinBox.setValue(int(campaign[5]) if campaign[5] != "None" and campaign[5] is not None else 0)
            self.companyComboBox.setCurrentText(campaign[6])
            self.load_advertisements(campaign[0])
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid campaign index!")

    def navigate_next(self) -> None:
        if self.current_campaign_index < len(self.campaign_data) - 1:
            self.current_campaign_index += 1
            self.display_campaign(self.current_campaign_index)

    def navigate_previous(self) -> None:
        if self.current_campaign_index > 0:
            self.current_campaign_index -= 1
            self.display_campaign(self.current_campaign_index)

    def load_advertisements(self, campaign_id: int) -> None:
        query = "SELECT * FROM Advertisements WHERE campaign_id = ?;"
        headers, data = self.db_manager.fetch_data(query, (campaign_id,))
        self.fill_table(self.advertisementsTableWidget, data, headers)

    def fill_table(self, table_widget: QtWidgets.QTableWidget, data: List[Tuple[Any, ...]], headers: List[str]) -> None:
        table_widget.setRowCount(len(data))
        table_widget.setColumnCount(len(headers))
        table_widget.setHorizontalHeaderLabels(headers)
        for row_ind, row_data in enumerate(data):
            for col_ind, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                table_widget.setItem(row_ind, col_ind, item)

    def save_changes(self) -> None:
        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure you want to save changes?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            campaign_id = self.idLineEdit.text().strip()
            name = self.nameLineEdit.text().strip()
            start_date = self.startDateEdit.date().toString("yyyy-MM-dd")
            end_date = self.endDateEdit.date().toString("yyyy-MM-dd")
            goal = self.goalLineEdit.text().strip()
            budget = self.budgetSpinBox.value()
            company_name = self.companyComboBox.currentText()

            if not goal:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Incomplete Data",
                    "Please fill in all the fields before saving!"
                )
                return
            query = """
                                UPDATE Campaigns
                                SET name = ?, start_date = ?, end_date = ?, goal = ?, budget = ?, company_name = ?
                                WHERE campaign_id = ?
                            """
            self.db_manager.execute_query(query, (
            name, start_date, end_date, goal, int(budget), company_name, int(campaign_id)))
            QtWidgets.QMessageBox.information(self, "Success", "Changes saved successfully!")


    def add_advertisement(self) -> None:
        campaign_name = self.nameLineEdit.text()
        if not campaign_name:
            QtWidgets.QMessageBox.warning(self, "Error", "Select a campaign!")
            return
        dialog = AddAdvertisementWindow(self)
        dialog.set_campaign_name(campaign_name)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            data = dialog.get_data()
            query = """
                INSERT INTO Advertisements (advertisement_id, text, format, send_time, topic, language, attachment, clicks, views, campaign_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            self.db_manager.execute_query(query, data)
            self.load_advertisements(int(self.idLineEdit.text()))

    def edit_advertisement(self) -> None:
        selected_row = self.advertisementsTableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Select an advertisement to edit!")
            return
        current_data = [self.advertisementsTableWidget.item(selected_row, col_ind).text()
                        for col_ind in range(self.advertisementsTableWidget.columnCount())]
        if not current_data:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to load advertisement data!")
            return
        dialog = AddAdvertisementWindow(self)
        dialog.set_data(current_data)
        dialog.set_campaign_name(self.nameLineEdit.text())
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            updated_data = dialog.get_data()
            query = """
                UPDATE Advertisements
                SET text = ?, format = ?, send_time = ?, topic = ?, language = ?, attachment = ?, clicks = ?, views = ?, campaign_id = ?
                WHERE advertisement_id = ?
            """
            self.db_manager.execute_query(query, updated_data[1:] + (updated_data[0],))
            self.load_advertisements(self.idLineEdit.text())

    def remove_advertisement(self) -> None:
        selected_row = self.advertisementTableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Select an advertisement to remove!")
            return
        advertisement_id = self.advertisementTableWidget.item(selected_row, 0).text()
        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirmation",
            f"Are you sure you want to delete advertisement with ID {advertisement_id}?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            query = "DELETE FROM Advertisements WHERE advertisement_id = ?;"
            self.db_manager.execute_query(query, (advertisement_id,))
            self.load_advertisements(self.idLineEdit.text())
