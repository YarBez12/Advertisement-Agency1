from Models import *

class Collection:
    def __init__(self):
        self._items = []

    def add(self, item):
        if not isinstance(item, Model):
            raise TypeError("Item must be an instance of a model.")
        self._items.append(item)

    def remove(self, item):
        if item in self._items:
            self._items.remove(item)
        else:
            raise ValueError("Item not found in the collection.")

    def update(self, index: int, item):
        if not isinstance(item, Model):
            raise TypeError("Item must be an instance of a model.")
        if index < 0 or index >= len(self._items):
            raise IndexError("Index out of range.")
        self._items[index] = item

    def find(self, **criteria):
        results = []
        for item in self._items:
            if all(getattr(item, key, None) == value for key, value in criteria.items()):
                results.append(item)
        return results

    def get_items(self):
        return self._items

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __str__(self):
        return f"Collection({len(self._items)} items)"

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise TypeError("Index must be an integer.")
        if index < 0 or index >= len(self._items):
            raise IndexError("Index out of range.")
        return self._items[index]

    def get_str_models_name(self):
        return "Collection"

class ClientCollection(Collection):
    def add(self, item):
        if not isinstance(item, Client):
            raise TypeError("Item must be an instance of Client.")
        super().add(item)

    def get_str_models_name(self):
        return "Clients"

    def save_to_db(self, db_manager):
        for client in self._items:
            query = """
                MERGE INTO Clients AS target
                USING (SELECT ? AS company_name) AS source
                ON target.company_name = source.company_name
                WHEN MATCHED THEN
                    UPDATE SET
                        phone = ?, email = ?, password = ?, address = ?, type = ?, business_area = ?, available_budget = ?
                WHEN NOT MATCHED THEN
                    INSERT (company_name, phone, email, password, address, type, business_area, available_budget)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ;
            """
            params = [
                client.company_name,
                client.phone,
                client.email,
                client.password,
                client.address,
                client.type,
                client.business_area,
                client.available_budget,
                client.company_name,
                client.phone,
                client.email,
                client.password,
                client.address,
                client.type,
                client.business_area,
                client.available_budget,
            ]
            db_manager.execute_query(query, params)

class CampaignCollection(Collection):
    def add(self, item):
        if not isinstance(item, Campaign):
            raise TypeError("Item must be an instance of Campaign.")
        super().add(item)

    def get_str_models_name(self):
        return "Campaigns"

    def save_to_db(self, db_manager):
        for campaign in self._items:
            query = """
                MERGE INTO Campaigns AS target
                USING (SELECT ? AS campaign_id) AS source
                ON target.campaign_id = source.campaign_id
                WHEN MATCHED THEN
                    UPDATE SET
                        campaign_name = ?, start_date = ?, end_date = ?, goal = ?, budget = ?, company_name = ?
                WHEN NOT MATCHED THEN
                    INSERT (campaign_id, campaign_name, start_date, end_date, goal, budget, company_name)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ;
            """
            params = [
                campaign.campaign_id,
                campaign.campaign_name,
                campaign.start_date,
                campaign.end_date,
                campaign.goal,
                campaign.budget,
                campaign.company_name,
                campaign.campaign_id,
                campaign.campaign_name,
                campaign.start_date,
                campaign.end_date,
                campaign.goal,
                campaign.budget,
                campaign.company_name,
            ]
            db_manager.execute_query(query, params)

class AdvertisementCollection(Collection):
    def add(self, item):
        if not isinstance(item, Advertisement):
            raise TypeError("Item must be an instance of Advertisement.")
        super().add(item)

    def get_str_models_name(self):
        return "Advertisements"

    def save_to_db(self, db_manager):
        for advertisement in self._items:
            query = """
                MERGE INTO Advertisements AS target
                USING (SELECT ? AS advertisement_id) AS source
                ON target.advertisement_id = source.advertisement_id
                WHEN MATCHED THEN
                    UPDATE SET
                        text = ?, format = ?, send_time = ?, topic = ?, language = ?, attachment = ?, clicks = ?, views = ?, campaign_id = ?, platform_id = ?
                WHEN NOT MATCHED THEN
                    INSERT (advertisement_id, text, format, send_time, topic, language, attachment, clicks, views, campaign_id, platform_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ;
            """
            params = [
                advertisement.advertisement_id,
                advertisement.text,
                advertisement.format,
                advertisement.send_time,
                advertisement.topic,
                advertisement.language,
                advertisement.attachment,
                advertisement.clicks,
                advertisement.views,
                advertisement.campaign_id,
                advertisement.platform_id,
                advertisement.advertisement_id,
                advertisement.text,
                advertisement.format,
                advertisement.send_time,
                advertisement.topic,
                advertisement.language,
                advertisement.attachment,
                advertisement.clicks,
                advertisement.views,
                advertisement.campaign_id,
                advertisement.platform_id,
            ]
            db_manager.execute_query(query, params)

class MediaPlatformCollection(Collection):
    def add(self, item):
        if not isinstance(item, MediaPlatform):
            raise TypeError("Item must be an instance of Media Platform.")
        super().add(item)

    def get_str_models_name(self):
        return "Media Platforms"

    def save_to_db(self, db_manager):
        for platform in self._items:
            query = """
                MERGE INTO MediaPlatforms AS target
                USING (SELECT ? AS platform_id) AS source
                ON target.platform_id = source.platform_id
                WHEN MATCHED THEN
                    UPDATE SET
                        platform_name = ?, platform_type = ?, main_ad_format = ?, audience_size = ?
                WHEN NOT MATCHED THEN
                    INSERT (platform_id, platform_name, platform_type, main_ad_format, audience_size)
                    VALUES (?, ?, ?, ?, ?)
                ;
            """
            params = [
                platform.platform_id,
                platform.platform_name,
                platform.platform_type,
                platform.main_ad_format,
                platform.audience_size,
                platform.platform_id,
                platform.platform_name,
                platform.platform_type,
                platform.main_ad_format,
                platform.audience_size,
            ]
            db_manager.execute_query(query, params)

class CampaignPlatformCollection(Collection):
    def add(self, item):
        if not isinstance(item, CampaignPlatform):
            raise TypeError("Item must be an instance of CampaignPlatform model.")
        super().add(item)

    def get_str_models_name(self):
        return "CampaignPlatformCollection"

    def save_to_db(self, db_manager):
        for cp in self._items:
            query = """
                MERGE INTO CampaignPlatforms AS target
                USING (SELECT ? AS campaign_id, ? AS platform_id) AS source
                ON target.campaign_id = source.campaign_id AND target.platform_id = source.platform_id
                WHEN MATCHED THEN
                    UPDATE SET budget_allocation = ?
                WHEN NOT MATCHED THEN
                    INSERT (campaign_id, platform_id, budget_allocation)
                    VALUES (?, ?, ?)
                ;
            """
            params = [
                cp.campaign_id,
                cp.platform_id,
                cp.budget_allocation,
                cp.campaign_id,
                cp.platform_id,
                cp.budget_allocation,
            ]
            db_manager.execute_query(query, params)

class AudienceSegmentCollection(Collection):
    def add(self, item):
        if not isinstance(item, AudienceSegment):
            raise TypeError("Item must be an instance of Audience Segment.")
        super().add(item)

    def get_str_models_name(self):
        return "Audience Segments"

    def save_to_db(self, db_manager):
        for segment in self._items:
            query = """
                MERGE INTO AudienceSegments AS target
                USING (SELECT ? AS segment_id) AS source
                ON target.segment_id = source.segment_id
                WHEN MATCHED THEN
                    UPDATE SET
                        segment_name = ?, age_range = ?, gender = ?, location = ?, general_interest = ?, 
                        socioeconomic_status = ?, language = ?, behavioral_characteristics = ?, device_used = ?
                WHEN NOT MATCHED THEN
                    INSERT (segment_id, segment_name, age_range, gender, location, general_interest, 
                            socioeconomic_status, language, behavioral_characteristics, device_used)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ;
            """
            params = [
                segment.segment_id,
                segment.segment_name,
                segment.age_range,
                segment.gender,
                segment.location,
                segment.general_interest,
                segment.socioeconomic_status,
                segment.language,
                segment.behavioral_characteristics,
                segment.device_used,
                segment.segment_id,
                segment.segment_name,
                segment.age_range,
                segment.gender,
                segment.location,
                segment.general_interest,
                segment.socioeconomic_status,
                segment.language,
                segment.behavioral_characteristics,
                segment.device_used,
            ]
            db_manager.execute_query(query, params)

class SegmentPlatformCollection(Collection):
    def add(self, item):
        if not isinstance(item, SegmentPlatform):
            raise TypeError("Item must be an instance of SegmentPlatform model.")
        super().add(item)

    def get_str_models_name(self):
        return "SegmentPlatformCollection"

    def save_to_db(self, db_manager):
        for sp in self._items:
            query = """
                MERGE INTO SegmentPlatforms AS target
                USING (SELECT ? AS segment_id, ? AS platform_id) AS source
                ON target.segment_id = source.segment_id AND target.platform_id = source.platform_id
                WHEN MATCHED THEN
                    UPDATE SET segment_id = ?, platform_id = ?
                WHEN NOT MATCHED THEN
                    INSERT (segment_id, platform_id)
                    VALUES (?, ?)
                ;
            """
            params = [
                sp.segment_id,
                sp.platform_id,
                sp.segment_id,
                sp.platform_id,
                sp.segment_id,
                sp.platform_id,
            ]
            db_manager.execute_query(query, params)

class CampaignSegmentCollection(Collection):
    def add(self, item):
        if not isinstance(item, CampaignSegment):
            raise TypeError("Item must be an instance of CampaignSegment model.")
        super().add(item)

    def get_str_models_name(self):
        return "CampaignSegmentCollection"

    def save_to_db(self, db_manager):
        for cs in self._items:
            query = """
                MERGE INTO CampaignSegments AS target
                USING (SELECT ? AS campaign_id, ? AS segment_id) AS source
                ON target.campaign_id = source.campaign_id AND target.segment_id = source.segment_id
                WHEN MATCHED THEN
                    UPDATE SET ad_frequency = ?
                WHEN NOT MATCHED THEN
                    INSERT (campaign_id, segment_id, ad_frequency)
                    VALUES (?, ?, ?)
                ;
            """
            params = [
                cs.campaign_id,
                cs.segment_id,
                cs.ad_frequency,
                cs.campaign_id,
                cs.segment_id,
                cs.ad_frequency,
            ]
            db_manager.execute_query(query, params)


class UserCollection(Collection):
    def add(self, item):
        if not isinstance(item, User):
            raise TypeError("Item must be an instance of User.")
        super().add(item)

    def get_str_models_name(self):
        return "Users"

    def save_to_db(self, db_manager):
        for user in self._items:
            query = """
                MERGE INTO Users AS target
                USING (SELECT ? AS email) AS source
                ON target.email = source.email
                WHEN MATCHED THEN
                    UPDATE SET
                        password = ?, age = ?, gender = ?, country = ?, account_creation_date = ?, 
                        last_purchase_date = ?, segment_id = ?
                WHEN NOT MATCHED THEN
                    INSERT (email, password, age, gender, country, account_creation_date, 
                            last_purchase_date, segment_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ;
            """
            params = [
                user.email,
                user.password,
                user.age,
                user.gender,
                user.country,
                user.account_creation_date,
                user.last_purchase_date,
                user.segment_id,
                user.email,
                user.password,
                user.age,
                user.gender,
                user.country,
                user.account_creation_date,
                user.last_purchase_date,
                user.segment_id,
            ]
            db_manager.execute_query(query, params)
