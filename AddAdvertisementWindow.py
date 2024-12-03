from PyQt5 import QtWidgets, uic
from typing import Tuple, Optional, List, Any
from PyQt5.QtCore import QDate, QTimer
from DatabaseController import DatabaseController
from InitialData import *
from Models import *

DB_CONFIG = {
    "Driver": "{ODBC Driver 17 for SQL Server}",
    "Server": "localhost,1433",
    "Database": "LabWork1",
    "Uid": "SA",
    "Pwd": "LUDRHQ2g4",
    "Encrypt": "no",
    "TrustServerCertificate": "yes"
}




class AddAdvertisementWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_manager = DatabaseController(DB_CONFIG)
        max_id = self.select_max_id_from_table()
        uic.loadUi("addAdvertisementWindow.ui", self)
        self.idLineEdit.setText(str(max_id + 1))
        self.sendDateEdit.setDate(QDate.currentDate().addMonths(1))
        self.sendDateEdit.setCalendarPopup(True)
        self.formatComboBox.addItems(ADVERTISEMENT_FORMATS)
        self.languageComboBox.addItems(ADVERTISEMENT_LANGUAGES)
        self.addAtachmentButton.clicked.connect(self.choose_file)
        all_campaigns = self.get_all_campaigns()
        self.campaignComboBox.addItems([campaign.name for campaign in all_campaigns])
        self.saveButton.clicked.connect(self.save)
        self.cancelButton.clicked.connect(self.reject)
        self.resetButton.clicked.connect(self.reset)

    def choose_file(self) -> None:
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Choose your file", "", "All Files (*.*)",
                                                             options=options)
        if file_path:
            self.attachmentLineEdit.setText(file_path)

    def select_max_id_from_table(self) -> int:
        query = "SELECT MAX(advertisement_id) FROM Advertisements"
        try:
            _, rows = self.db_manager.fetch_data(query)
            max_id = rows[0][0] if rows and rows[0][0] is not None else -1
            return max_id
        except Exception:
            return -1

    def get_all_campaigns(self) -> List[Campaign]:
        query = "SELECT campaign_id, goal, company_name, name, start_date, end_date, budget FROM Campaigns;"
        try:
            _, rows = self.db_manager.fetch_data(query)
            campaigns = [
                Campaign(
                    campaign_id=row[0],
                    goal=row[1],
                    company_name=row[2],
                    name = row[3],
                    start_date=row[4],
                    end_date=row[5],
                    budget=row[6],
                )
                for row in rows
            ]
            return campaigns
        except Exception:
            return []

    def validate(self) -> bool:
        advertisement_topic = self.topicLineEdit.text().strip()
        if not advertisement_topic:
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

    def get_data(self) -> Optional[Advertisement]:
        campaign_name = self.campaignComboBox.currentText().strip()
        query = "SELECT campaign_id FROM Campaigns WHERE name = ?;"
        _, rows = self.db_manager.fetch_data(query, (campaign_name,))
        campaign_id = rows[0][0]

        return Advertisement(
            advertisement_id=int(self.idLineEdit.text().strip()),
            text=self.textLineEdit.text().strip(),
            format=self.formatComboBox.currentText(),
            send_time=self.sendDateEdit.date().toString("yyyy-MM-dd"),
            topic=self.topicLineEdit.text().strip(),
            language=self.languageComboBox.currentText(),
            attachment=self.attachmentLineEdit.text().strip(),
            clicks=int(self.clicksLineEdit.text().strip()) if self.clicksLineEdit.text().strip() else None,
            views=int(self.viewsLineEdit.text().strip()) if self.viewsLineEdit.text().strip() else None,
            campaign_id=campaign_id
        )

    def reset(self) -> None:
        self.idLineEdit.clear()
        self.textLineEdit.clear()
        self.formatComboBox.setCurrentIndex(0)
        self.sendDateEdit.setDate(QDate.currentDate().addMonths(1))
        self.topicLineEdit.clear()
        self.languageComboBox.setCurrentIndex(0)
        self.attachmentLineEdit.clear()
        self.clicksLineEdit.clear()
        self.viewsLineEdit.clear()
        self.campaignComboBox.setCurrentIndex(0)

    def set_data(self, advertisement: Advertisement) -> None:
        self.idLineEdit.setText(str(advertisement.advertisement_id))
        self.textLineEdit.setText(advertisement.text or "")
        self.formatComboBox.setCurrentText(advertisement.format or "")
        self.sendDateEdit.setDate(
            QDate.fromString(advertisement.send_time, "yyyy-MM-dd") if advertisement.send_time else QDate.currentDate())
        self.topicLineEdit.setText(advertisement.topic or "")
        self.languageComboBox.setCurrentText(advertisement.language or "")
        self.attachmentLineEdit.setText(advertisement.attachment or "")
        self.clicksLineEdit.setText(str(advertisement.clicks) if advertisement.clicks is not None else "")
        self.viewsLineEdit.setText(str(advertisement.views) if advertisement.views is not None else "")
        query = "SELECT name FROM Campaigns WHERE campaign_id = ?;"
        _, rows = self.db_manager.fetch_data(query, (advertisement.campaign_id,))
        self.campaignComboBox.setCurrentText(rows[0][0] if rows else "")

    def set_campaign_name(self, campaign_name: int):
        self.campaignComboBox.setCurrentText(str(campaign_name))
        self.campaignComboBox.setEnabled(False)
