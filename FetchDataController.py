from Collections import *


def load_all_tables_from_db(db_manager):
    ClientCollection.load_clients_from_db(db_manager, InitialData.Clients)
    CampaignCollection.load_campaigns_from_db(db_manager, InitialData.Campaigns)
    AdvertisementCollection.load_advertisements_from_db(db_manager, InitialData.Advertisements)
    MediaPlatformCollection.load_media_platforms_from_db(db_manager, InitialData.MediaPlatforms)
    CampaignPlatformCollection.load_campaign_platforms_from_db(db_manager, InitialData.CampaignPlatforms)
    AudienceSegmentCollection.load_audience_segments_from_db(db_manager, InitialData.AudienceSegments)
    SegmentPlatformCollection.load_segment_platforms_from_db(db_manager, InitialData.SegmentPlatforms)
    UserCollection.load_users_from_db(db_manager, InitialData.Users)


def save_all_tables_to_db(db_manager):
    InitialData.Clients.save_to_db(db_manager)
    InitialData.Campaigns.save_to_db(db_manager)
    InitialData.Advertisements.save_to_db(db_manager)
    InitialData.MediaPlatforms.save_to_db(db_manager)
    InitialData.CampaignPlatforms.save_to_db(db_manager)
    InitialData.AudienceSegments.save_to_db(db_manager)
    InitialData.SegmentPlatforms.save_to_db(db_manager)
    InitialData.Users.save_to_db(db_manager)