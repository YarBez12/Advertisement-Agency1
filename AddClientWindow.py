from PyQt5 import QtWidgets, uic
from typing import Tuple, Optional


class AddClientWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("addClientWindow.ui", self)
        self.typeComboBox.addItems(["Individual", "Company"])
        self.areaComboBox.addItems([
            "IT",
            "Energy",
            "Construction",
            "Automotive",
            "Marketing",
            "Healthcare",
            "Education",
            "Finance",
            "Retail",
            "Manufacturing",
            "Logistics",
            "Telecommunications",
            "Real Estate",
            "Hospitality",
            "Entertainment",
            "Agriculture",
            "Food & Beverage",
            "Pharmaceuticals",
            "Aerospace",
            "Environmental Services"
        ])
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

    def get_data(self) -> Optional[Tuple[str, ...]]:
        return (
            self.nameLineEdit.text().strip(),
            self.phoneLineEdit.text().strip(),
            self.emailLineEdit.text().strip(),
            self.addressLineEdit.text().strip(),
            self.typeComboBox.currentText(),
            self.areaComboBox.currentText(),
            self.budgetSpinBox.value(),
        )

    def reset(self) -> None:
        self.nameLineEdit.clear()
        self.phoneLineEdit.clear()
        self.emailLineEdit.clear()
        self.addressLineEdit.clear()
        self.typeComboBox.setCurrentIndex(0)
        self.areaComboBox.setCurrentIndex(0)
        self.budgetSpinBox.setValue(0)

    def set_data(self, data) -> None:
        self.nameLineEdit.setText(data[0] if data[0] else "")
        self.phoneLineEdit.setText(data[1] if data[1] else "")
        self.emailLineEdit.setText(data[2] if data[2] else "")
        self.addressLineEdit.setText(data[3] if data[3] else "")
        self.typeComboBox.setCurrentText(data[4] if data[4] else "")
        self.areaComboBox.setCurrentText(data[5] if data[5] else "")
        self.budgetSpinBox.setValue(int(data[6]) if data[6] != "None" else 0)
