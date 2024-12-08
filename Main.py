from PyQt5 import QtWidgets
from DatabaseController import DatabaseController
from Windows import TablesWindow, MainWindow
from Collections import *
import InitialData
from FetchDataController import *


app = QtWidgets.QApplication([])
db_manager = DatabaseController(InitialData.DB_CONFIG)
load_all_tables_from_db(db_manager)
window = MainWindow()
window.show()
app.exec_()
save_all_tables_to_db(db_manager)
