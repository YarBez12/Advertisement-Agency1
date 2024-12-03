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
                        phone = ?, email = ?, address = ?, type = ?, business_area = ?, available_budget = ?
                WHEN NOT MATCHED THEN
                    INSERT (company_name, phone, email, address, type, business_area, available_budget)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ;
            """
            params = [
                client.company_name,
                client.phone,
                client.email,
                client.address,
                client.type,
                client.business_area,
                client.available_budget,
                client.company_name,
                client.phone,
                client.email,
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
                        name = ?, start_date = ?, end_date = ?, goal = ?, budget = ?, company_name = ?
                WHEN NOT MATCHED THEN
                    INSERT (campaign_id, name, start_date, end_date, goal, budget, company_name)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ;
            """
            params = [
                campaign.campaign_id,
                campaign.name,
                campaign.start_date,
                campaign.end_date,
                campaign.goal,
                campaign.budget,
                campaign.company_name,
                campaign.campaign_id,
                campaign.name,
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

class CampaignPlatformCollection(Collection):
    def add(self, item):
        if not isinstance(item, CampaignPlatform):
            raise TypeError("Item must be an instance of CampaignPlatform model.")
        super().add(item)

    def get_str_models_name(self):
        return "CampaignPlatformCollection"

class AudienceSegmentCollection(Collection):
    def add(self, item):
        if not isinstance(item, AudienceSegment):
            raise TypeError("Item must be an instance of Audience Segment.")
        super().add(item)

    def get_str_models_name(self):
        return "Audience Segments"

class SegmentPlatformCollection(Collection):
    def add(self, item):
        if not isinstance(item, SegmentPlatform):
            raise TypeError("Item must be an instance of SegmentPlatform model.")
        super().add(item)

    def get_str_models_name(self):
        return "SegmentPlatformCollection"

class CampaignSegmentCollection(Collection):
    def add(self, item):
        if not isinstance(item, CampaignSegment):
            raise TypeError("Item must be an instance of CampaignSegment model.")
        super().add(item)

    def get_str_models_name(self):
        return "CampaignSegmentCollection"

class UserCollection(Collection):
    def add(self, item):
        if not isinstance(item, User):
            raise TypeError("Item must be an instance of User.")
        super().add(item)

    def get_str_models_name(self):
        return "Users"
