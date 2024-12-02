from PyQt5 import QtWidgets, uic
from typing import Tuple, Optional, List
from PyQt5.QtCore import QDate
from LabWork1.DatabaseController import DatabaseController


DB_CONFIG = {
    "Driver": "{ODBC Driver 17 for SQL Server}",
    "Server": "localhost,1433",
    "Database": "LabWork1",
    "Uid": "SA",
    "Pwd": "LUDRHQ2g4",
    "Encrypt": "no",
    "TrustServerCertificate": "yes"
}


class AddCampaignWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_manager = DatabaseController(DB_CONFIG)
        max_id = self.select_max_id_from_table()
        uic.loadUi("addCampaignWindow.ui", self)
        self.idLineEdit.setText(str(max_id + 1))
        self.nameLineEdit.setPlaceholderText(f"Campaign #{max_id + 1}")
        self.startDateEdit.setDate(QDate.currentDate())
        self.endDateEdit.setDate(QDate.currentDate().addYears(5))
        self.startDateEdit.setCalendarPopup(True)
        self.endDateEdit.setCalendarPopup(True)
        all_client_names = self.get_client_names()
        self.companyComboBox.addItems(all_client_names)
        self.saveButton.clicked.connect(self.save)
        self.cancelButton.clicked.connect(self.reject)
        self.resetButton.clicked.connect(self.reset)

    def select_max_id_from_table(self) -> int:
        query = "SELECT MAX(campaign_id) FROM Campaigns"
        try:
            _, rows = self.db_manager.fetch_data(query)
            max_id = rows[0][0] if rows and rows[0][0] is not None else -1
            return max_id
        except Exception:
            return -1

    def get_client_names(self) -> List[str]:
        query = "SELECT company_name FROM Clients;"
        try:
            _, rows = self.db_manager.fetch_data(query)
            client_names = [row[0] for row in rows]
            return client_names
        except Exception:
            return []

    def validate(self) -> bool:
        campaign_goal = self.goalLineEdit.text().strip()
        if not campaign_goal:
            QtWidgets.QMessageBox.warning(
                self,
                "Unfilled fields",
                "Please fill in all necessary fields"
            )
            return False
        return True

    def save(self) -> None:
        if self.validate():
            self.accept()

    def get_data(self) -> Optional[Tuple[str, ...]]:
        return (
            self.idLineEdit.text().strip(),
            self.nameLineEdit.text().strip(),
            self.startDateEdit.date().toString("yyyy-MM-dd"),
            self.endDateEdit.date().toString("yyyy-MM-dd"),
            self.goalLineEdit.text().strip(),
            self.budgetSpinBox.value(),
            self.companyComboBox.currentText(),
        )

    def reset(self) -> None:
        self.idLineEdit.clear()
        self.nameLineEdit.clear()
        self.startDateEdit.setDate(QDate.currentDate())
        self.endDateEdit.setDate(QDate.currentDate().addYears(5))
        self.goalLineEdit.clear()
        self.budgetSpinBox.setValue(1000)
        self.companyComboBox.setCurrentIndex(0)

    def set_data(self, data) -> None:
        self.idLineEdit.setText(str(data[0]))
        self.nameLineEdit.setText(data[1] if data[1] else "")
        # self.startDateEdit.setDate(QDate.fromString(data[2], "yyyy-MM-dd") if data[2] else QDate.currentDate())
        # self.endDateEdit.setDate(QDate.fromString(data[3], "yyyy-MM-dd") if data[3] else QDate.currentDate())
        self.startDateEdit.setDate(QDate.fromString(data[2][:10], "yyyy-MM-dd"))
        self.endDateEdit.setDate(QDate.fromString(data[3][:10], "yyyy-MM-dd"))
        self.goalLineEdit.setText(data[4] if data[4] else "")
        self.budgetSpinBox.setValue(int(data[5]) if data[5] != "None" else 0)
        self.companyComboBox.setCurrentText(data[6] if data[6] else "")
