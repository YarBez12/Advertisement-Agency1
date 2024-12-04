from PyQt5 import QtWidgets
from DatabaseController import DatabaseController
from Windows import TablesWindow
from FetchDataController import *
import InitialData
DB_CONFIG = {
    "Driver": "{ODBC Driver 17 for SQL Server}",
    "Server": "localhost,1433",
    "Database": "Advertising Agency",
    "Uid": "SA",
    "Pwd": "LUDRHQ2g4",
    "Encrypt": "no",
    "TrustServerCertificate": "yes"
}

app = QtWidgets.QApplication([])

db_manager = DatabaseController(DB_CONFIG)
load_clients_from_db(db_manager, InitialData.Clients)
load_campaigns_from_db(db_manager, InitialData.Campaigns)
load_advertisements_from_db(db_manager, InitialData.Advertisements)
load_media_platforms_from_db(db_manager, InitialData.MediaPlatforms)
load_campaign_platforms_from_db(db_manager, InitialData.CampaignPlatforms)
load_audience_segments_from_db(db_manager, InitialData.AudienceSegments)
load_segment_platforms_from_db(db_manager, InitialData.SegmentPlatforms)
load_campaign_segments_from_db(db_manager, InitialData.CampaignSegments)
load_users_from_db(db_manager, InitialData.Users)
window = TablesWindow()
window.show()
app.exec_()
InitialData.Clients.save_to_db(db_manager)
InitialData.Campaigns.save_to_db(db_manager)
InitialData.Advertisements.save_to_db(db_manager)
InitialData.MediaPlatforms.save_to_db(db_manager)
InitialData.CampaignPlatforms.save_to_db(db_manager)
InitialData.AudienceSegments.save_to_db(db_manager)
InitialData.SegmentPlatforms.save_to_db(db_manager)
InitialData.CampaignSegments.save_to_db(db_manager)
InitialData.Users.save_to_db(db_manager)
