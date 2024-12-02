from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget
from typing import List, Tuple, Any
import pyodbc

from LabWork1.DatabaseController import DatabaseController
from LabWork1.DatabaseQueryError import DatabaseQueryError

DB_CONFIG = {
    "Driver": "{ODBC Driver 17 for SQL Server}",
    "Server": "localhost,1433",
    "Database": "LabWork1",
    "Uid": "SA",
    "Pwd": "LUDRHQ2g4",
    "Encrypt": "no",
    "TrustServerCertificate": "yes"
}


class SQLEditorWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("sqlEditorForm.ui", self)
        self.db_manager = DatabaseController(DB_CONFIG)
        self.queryTextEdit.setText("SELECT")
        self.executeButton.clicked.connect(self.execute_query)
        self.clearButton.clicked.connect(self.clear_result)
        self.exitButton.clicked.connect(self.close)

    def execute_query(self):
        query = self.queryTextEdit.toPlainText().strip()
        if not query:
            QtWidgets.QMessageBox.warning(self, "Warning", "Enter your SQL Query")
            return

        try:
            headers, data = self.db_manager.fetch_data(query)
            self.display_result(data, headers)
        except DatabaseQueryError as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Error during SQL Query: {e}")

    def display_result(self, data: List[Tuple[Any, ...]], headers: List[str]):
        self.resultTableWidget.setRowCount(len(data))
        self.resultTableWidget.setColumnCount(len(headers))
        self.resultTableWidget.setHorizontalHeaderLabels(headers)

        for row_ind, row_data in enumerate(data):
            for col_ind, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.resultTableWidget.setItem(row_ind, col_ind, item)

    def clear_result(self):
        self.queryTextEdit.clear()
        self.resultTableWidget.clear()
        self.resultTableWidget.setRowCount(0)
        self.resultTableWidget.setColumnCount(0)
