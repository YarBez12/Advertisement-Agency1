from PyQt5 import QtWidgets
from DatabaseController import DatabaseController
from MainWindow import MainWindow

DB_CONFIG = {
    "Driver": "{ODBC Driver 17 for SQL Server}",
    "Server": "localhost,1433",
    "Database": "LabWork1",
    "Uid": "SA",
    "Pwd": "LUDRHQ2g4",
    "Encrypt": "no",
    "TrustServerCertificate": "yes"
}

app = QtWidgets.QApplication([])

db_manager = DatabaseController(DB_CONFIG)

window = MainWindow(db_manager, "form.ui")
window.show()
app.exec_()
