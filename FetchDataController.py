from Models import *


def load_clients_from_db(db_manager, clients_collection):
    query = """
            SELECT company_name, phone, email, password, address, type, business_area, available_budget
            FROM Clients;
        """
    _, rows = db_manager.fetch_data(query)
    for row in rows:
        client = Client(
            company_name=row[0],
            phone=row[1],
            email=row[2],
            password=row[3],
            address=row[4],
            type=row[5],
            business_area=row[6],
            available_budget=row[7]
        )
        clients_collection.add(client)

def load_campaigns_from_db(db_manager, campaign_collection):
    query = """
            SELECT campaign_id, campaign_name, start_date, end_date, goal, budget, company_name
            FROM Campaigns;
        """
    _, rows = db_manager.fetch_data(query)
    for row in rows:
        campaign = Campaign(
            campaign_id=row[0],
            campaign_name=row[1],
            start_date=row[2],
            end_date=row[3],
            goal=row[4],
            budget=row[5],
            company_name=row[6],
        )
        campaign_collection.add(campaign)

def load_advertisements_from_db(db_manager, advertisement_collection):
    query = """
            SELECT advertisement_id, format, topic, text, send_time, language, 
                   attachment, clicks, views, campaign_id, platform_id
            FROM Advertisements;
        """
    _, rows = db_manager.fetch_data(query)
    for row in rows:
        advertisement = Advertisement(
            advertisement_id=row[0],
            format=row[1],
            topic=row[2],
            text=row[3],
            send_time=row[4],
            language=row[5],
            attachment=row[6],
            clicks=row[7],
            views=row[8],
            campaign_id=row[9],
            platform_id=row[10],
        )
        advertisement_collection.add(advertisement)

def load_media_platforms_from_db(db_manager, media_platform_collection):
    query = """
        SELECT platform_id, platform_name, platform_type, main_ad_format, audience_size
        FROM MediaPlatforms;
    """
    _, rows = db_manager.fetch_data(query)
    for row in rows:
        platform = MediaPlatform(
            platform_id=row[0],
            platform_name=row[1],
            platform_type=row[2],
            main_ad_format=row[3],
            audience_size=row[4]
        )
        media_platform_collection.add(platform)


def load_campaign_platforms_from_db(db_manager, campaign_platform_collection):
    query = """
        SELECT campaign_id, platform_id, budget_allocation
        FROM CampaignPlatforms;
    """
    _, rows = db_manager.fetch_data(query)
    for row in rows:
        campaign_platform = CampaignPlatform(
            campaign_id=row[0],
            platform_id=row[1],
            budget_allocation=row[2]
        )
        campaign_platform_collection.add(campaign_platform)


def load_audience_segments_from_db(db_manager, audience_segment_collection):
    query = """
        SELECT segment_id, segment_name, age_range, gender, location, general_interest, 
               socioeconomic_status, language, behavioral_characteristics, device_used
        FROM AudienceSegments;
    """
    _, rows = db_manager.fetch_data(query)
    for row in rows:
        segment = AudienceSegment(
            segment_id=row[0],
            segment_name=row[1],
            age_range=row[2],
            gender=row[3],
            location=row[4],
            general_interest=row[5],
            socioeconomic_status=row[6],
            language=row[7],
            behavioral_characteristics=row[8],
            device_used=row[9]
        )
        audience_segment_collection.add(segment)


def load_segment_platforms_from_db(db_manager, segment_platform_collection):
    query = """
        SELECT segment_id, platform_id
        FROM SegmentPlatforms;
    """
    _, rows = db_manager.fetch_data(query)
    for row in rows:
        segment_platform = SegmentPlatform(
            segment_id=row[0],
            platform_id=row[1]
        )
        segment_platform_collection.add(segment_platform)


def load_campaign_segments_from_db(db_manager, campaign_segment_collection):
    query = """
        SELECT campaign_id, segment_id, ad_frequency
        FROM CampaignSegments;
    """
    _, rows = db_manager.fetch_data(query)
    for row in rows:
        campaign_segment = CampaignSegment(
            campaign_id=row[0],
            segment_id=row[1],
            ad_frequency=row[2]
        )
        campaign_segment_collection.add(campaign_segment)


def load_users_from_db(db_manager, user_collection):
    query = """
            SELECT email, password, age, gender, country, account_creation_date, last_purchase_date, segment_id
            FROM Users;
        """
    _, rows = db_manager.fetch_data(query)
    for row in rows:
        user = User(
            email=row[0],  # Adjusted to use 'email' as user_id from DB.
            password=row[1],
            age=row[2],
            gender=row[3],
            country=row[4],
            account_creation_date=row[5],
            last_purchase_date=row[6],
            segment_id=row[7]
        )
        user_collection.add(user)



