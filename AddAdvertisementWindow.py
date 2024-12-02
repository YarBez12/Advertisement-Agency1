from PyQt5 import QtWidgets, uic
from typing import Tuple, Optional, List, Any
from PyQt5.QtCore import QDate, QTimer
from DatabaseController import DatabaseController


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
    # ffff
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_manager = DatabaseController(DB_CONFIG)
        max_id = self.select_max_id_from_table()
        uic.loadUi("addAdvertisementWindow.ui", self)
        self.idLineEdit.setText(str(max_id + 1))
        self.sendDateEdit.setDate(QDate.currentDate().addMonths(1))
        self.sendDateEdit.setCalendarPopup(True)
        self.formatComboBox.addItems([
            "Text",
            "Image",
            "Video",
            "Audio",
            "HTML",
            "Animation",
            "Carousel",
            "Interactive",
            "Push Notification",
            "Story"
        ])
        self.languageComboBox.addItems([
            "English", "Spanish", "Mandarin", "Hindi", "Arabic",
            "Bengali", "Portuguese", "Irish", "Japanese", "Punjabi",
            "German", "Korean", "French", "Turkish", "Vietnamese",
            "Italian", "Urdu", "Thai", "Polish", "Dutch",
            "Persian", "Swahili", "Romanian", "Greek", "Hungarian",
            "Czech", "Finnish", "Hebrew", "Malay", "Indonesian",
            "Norwegian", "Swedish", "Danish", "Bulgarian", "Serbian",
            "Croatian", "Slovak", "Ukrainian", "Lithuanian", "Latvian",
            "Estonian", "Filipino", "Tamil", "Kannada", "Gujarati",
            "Marathi", "Telugu", "Malayalam", "Sinhala", "Burmese"
        ])
        self.addAtachmentButton.clicked.connect(self.choose_file)
        all_campaigns = self.get_all_campaigns()
        self.campaignComboBox.addItems(all_campaigns)
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

    def get_all_campaigns(self) -> List[str]:
        query = "SELECT name FROM Campaigns;"
        try:
            _, rows = self.db_manager.fetch_data(query)
            campaign_names = [row[0] for row in rows]
            return campaign_names
        except Exception as e:
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

    def get_data(self) -> Optional[Tuple[Any, ...]]:
        campaign_name = self.campaignComboBox.currentText().strip()
        query = "SELECT campaign_id FROM Campaigns WHERE name = ?;"
        _, rows = self.db_manager.fetch_data(query, (campaign_name,))
        campaign_id = rows[0][0]
        return (
            self.idLineEdit.text().strip(),
            self.textLineEdit.text().strip(),
            self.formatComboBox.currentText(),
            self.sendDateEdit.date().toString("yyyy-MM-dd"),
            self.topicLineEdit.text().strip(),
            self.languageComboBox.currentText(),
            self.attachmentLineEdit.text().strip(),
            self.clicksLineEdit.text().strip(),
            self.viewsLineEdit.text().strip(),
            campaign_id
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

    def set_data(self, data) -> None:
        self.idLineEdit.setText(str(data[0]))
        self.textLineEdit.setText(data[1] if data[1] else "")
        self.formatComboBox.setCurrentText(data[2] if data[2] else "")
        self.sendDateEdit.setDate(QDate.fromString(data[3], "yyyy-MM-dd") if data[3] else QDate.currentDate())
        self.topicLineEdit.setText(data[4] if data[4] else "")
        self.languageComboBox.setCurrentText(data[5] if data[5] else "")
        self.attachmentLineEdit.setText(data[6] if data[6] else "")
        self.clicksLineEdit.setText(str(data[7]) if data[7] != "None" else "0")
        self.viewsLineEdit.setText(str(data[8]) if data[8] != "None" else "0")
        query = "SELECT name FROM Campaigns WHERE campaign_id = ?;"
        _, rows = self.db_manager.fetch_data(query, (data[9],))
        self.campaignComboBox.setCurrentText(rows[0][0] if rows else "")

    def set_campaign_name(self, campaign_name: int):
        self.campaignComboBox.setCurrentText(str(campaign_name))
        self.campaignComboBox.setEnabled(False)
