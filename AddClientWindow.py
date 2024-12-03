from PyQt5 import QtWidgets, uic
from typing import Tuple, Optional
from InitialData import CLIENT_AREAS
from Models import Client
class AddClientWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("addClientWindow.ui", self)
        self.typeComboBox.addItems(["Individual", "Company"])
        self.areaComboBox.addItems(CLIENT_AREAS)
        self.saveButton.clicked.connect(self.save)
        self.cancelButton.clicked.connect(self.reject)
        self.resetButton.clicked.connect(self.reset)

    def validate(self) -> bool:
        client_name = self.nameLineEdit.text().strip()
        client_phone = self.phoneLineEdit.text().strip()
        client_email = self.emailLineEdit.text().strip()
        if not client_name or not client_phone or not client_email:
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

    def get_data(self) -> Optional[Client]:

        return Client(
            company_name=self.nameLineEdit.text().strip(),
            phone=self.phoneLineEdit.text().strip(),
            email=self.emailLineEdit.text().strip(),
            address=self.addressLineEdit.text().strip(),
            type=self.typeComboBox.currentText(),
            business_area=self.areaComboBox.currentText(),
            available_budget=self.budgetSpinBox.value()
        )

    def reset(self) -> None:
        self.nameLineEdit.clear()
        self.phoneLineEdit.clear()
        self.emailLineEdit.clear()
        self.addressLineEdit.clear()
        self.typeComboBox.setCurrentIndex(0)
        self.areaComboBox.setCurrentIndex(0)
        self.budgetSpinBox.setValue(0)

    def set_data(self, client) -> None:
        self.nameLineEdit.setText(client.company_name or "")
        self.phoneLineEdit.setText(client.phone or "")
        self.emailLineEdit.setText(client.email or "")
        self.addressLineEdit.setText(client.address or "")
        self.typeComboBox.setCurrentText(client.type or "")
        self.areaComboBox.setCurrentText(client.business_area or "")
        self.budgetSpinBox.setValue(client.available_budget or 0)
