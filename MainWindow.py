from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from typing import List, Tuple, Any

from AddAdvertisementWindow import AddAdvertisementWindow
from AddCampaignWindow import AddCampaignWindow
from AddClientWindow import AddClientWindow
from CampaignAndAdvertisementsWindow import CampaignAndAdvertisementsWindow
from DatabaseController import DatabaseController
from SQLEditorWindow import SQLEditorWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, db_manager: DatabaseController, ui_file: str) -> None:
        super().__init__()
        self.db_manager = db_manager
        uic.loadUi(ui_file, self)
        self.addButton.clicked.connect(self.open_dialog)
        self.editButton.clicked.connect(lambda : self.open_dialog(True))
        self.removeButton.clicked.connect(self.remove_item)
        self.firstButton.clicked.connect(lambda: self.navigate_first(self.dataTableWidget))
        self.previousButton.clicked.connect(lambda: self.navigate_previous(self.dataTableWidget))
        self.nextButton.clicked.connect(lambda: self.navigate_next(self.dataTableWidget))
        self.lastButton.clicked.connect(lambda: self.navigate_last(self.dataTableWidget))
        self.actionGoClients.triggered.connect(lambda: self.update_table("Clients"))
        self.actionGoCampaigns.triggered.connect(lambda: self.update_table("Campaigns"))
        self.actionGoAdvertisements.triggered.connect(lambda: self.update_table("Advertisements"))
        self.actionAdd.triggered.connect(self.open_dialog)
        self.actionUpdate.triggered.connect(lambda : self.open_dialog(True))
        self.actionDelete.triggered.connect(self.remove_item)
        # self.actionCampaignAndAdvertisements.triggered.connect(self.open_campaign_advertisements_dialog)
        self.update_table("Clients")

    def fill_table(self, widget: QTableWidget, data: List[Tuple[Any, ...]], headers: List[str]) -> None:
        widget.setRowCount(len(data))
        widget.setColumnCount(len(headers))
        widget.setHorizontalHeaderLabels(headers)
        for row_ind, row_data in enumerate(data):
            for col_ind, col_data in enumerate(row_data):
                item  = QTableWidgetItem(str(col_data))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                widget.setItem(row_ind, col_ind, item)

    def update_table(self, table_name: str) -> None:
        headers, data = self.db_manager.fetch_data(f"SELECT * FROM {table_name}")
        self.fill_table(self.dataTableWidget, data, headers)
        self.databaseNameLabel.setText(table_name)

    def navigate_first(self, widget: QTableWidget) -> None:
        if widget.rowCount() > 0:
            widget.selectRow(0)

    def navigate_previous(self, widget: QTableWidget) -> None:
        current_row = widget.currentRow()
        if current_row > 0:
            widget.selectRow(current_row - 1)

    def navigate_next(self, widget: QTableWidget) -> None:
        current_row = widget.currentRow()
        if current_row < widget.rowCount() - 1:
            widget.selectRow(current_row + 1)

    def navigate_last(self, widget: QTableWidget) -> None:
        if widget.rowCount() > 0:
            widget.selectRow(widget.rowCount() - 1)

    def remove_item(self) -> None:
        table_name = self.databaseNameLabel.text()
        key_columns = {
            "Clients" : "company_name",
            "Campaigns" : "campaign_id",
            "Advertisements" : "advertisement_id"
        }
        selected_row = self.dataTableWidget.currentRow()
        if selected_row != -1:
            key_value = self.dataTableWidget.item(selected_row, 0).text()
            reply = QtWidgets.QMessageBox.question(self,
                "Confirmation",
                f"Are you sure you want to delete item with {key_columns[table_name]} = {key_value}",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            if reply == QtWidgets.QMessageBox.Yes:
                query = f"DELETE FROM {table_name} WHERE {key_columns[table_name]} = ?"
                self.db_manager.execute_query(query, (key_value,))
                self.update_table(table_name)
            else:
                return

    def open_dialog(self, edit : bool = False) -> None:
        dialogs = {
            "Clients" : AddClientWindow,
            "Campaigns" : AddCampaignWindow,
            "Advertisements" : AddAdvertisementWindow
        }
        add_data = {
            "Clients": self.add_client,
            "Campaigns": self.add_campaign,
            "Advertisements" : self.add_advertisement
        }
        edit_data = {
            "Clients": self.edit_client,
            "Campaigns": self.edit_campaign,
            "Advertisements": self.edit_advertisement
        }
        table_name = self.databaseNameLabel.text()
        dialog_class = dialogs.get(table_name)
        if not dialog_class:
            return
        if edit:
            selected_row = self.dataTableWidget.currentRow();
            if selected_row == -1:
                QtWidgets.QMessageBox.warning(self, "No data", "Please select a row to edit")
                return
            current_data = [self.dataTableWidget.item(selected_row, col_ind).text()
                            for col_ind in range(self.dataTableWidget.columnCount())]
            dialog = dialog_class(self)
            dialog.set_data(current_data)
        else:
            dialog = dialog_class(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            data = dialog.get_data()
            if data:
                if edit:
                    edit_data[table_name](data)
                else:
                    add_data[table_name](data)

    def add_client(self, data):
        query = """
                INSERT INTO Clients (company_name, phone, email, address, type, business_area, available_budget)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """
        self.db_manager.execute_query(query, data)
        self.update_table("Clients")

    def add_advertisement(self, data):
        query = """
                INSERT INTO Advertisements (advertisement_id, text, format,
                send_time, topic, language, attachment, clicks, views, campaign_id )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
        self.db_manager.execute_query(query, data)
        self.update_table("Advertisements")

    def edit_client(self, data):
        query = """
                UPDATE Clients
                SET phone = ?, email = ?, address = ?, type = ?, business_area = ?, available_budget = ?
                WHERE company_name = ?
                """
        self.db_manager.execute_query(query, data[1:] + data[:1])
        self.update_table("Clients")

    def edit_campaign(self, data):
        query = """
                UPDATE Campaigns
                SET name = ?, start_date = ?, end_date = ?, goal = ?, budget = ?, company_name = ?
                WHERE campaign_id = ?
                """
        self.db_manager.execute_query(query, data[1:] + data[:1])
        self.update_table("Campaigns")

    def edit_advertisement(self, data):
        query = """
                UPDATE Advertisements
                SET text = ?, format = ?,
                send_time = ?, topic = ?, language = ?, attachment = ?,
                clicks = ?, views = ?, campaign_id = ?
                WHERE advertisement_id = ?
                """
        self.db_manager.execute_query(query, data[1:] + data[:1])
        self.update_table("Advertisements")

    def add_campaign(self, data):
        query = """
                    INSERT INTO Campaigns (campaign_id, name, start_date, end_date, goal, budget, company_name)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """
        self.db_manager.execute_query(query, data)
        self.update_table("Campaigns")

    def open_query_dialog(self):
        dialog = SQLEditorWindow()
        dialog.exec_()

    def open_campaign_advertisements_dialog(self):
        dialog = CampaignAndAdvertisementsWindow(self.db_manager)
        dialog.exec_()







