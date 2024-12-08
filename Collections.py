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

    def sort_items(self, key_func):
        sorted_collection = self.__class__()
        sorted_collection._items = sorted(
            self._items,
            key=lambda x: (
                key_func(x) is None or key_func(x) == "",
                key_func(x) if key_func(x) is not None else ""
            )
        )
        return sorted_collection


class ClientCollection(Collection):
    def add(self, item):
        if not isinstance(item, Client):
            raise TypeError("Item must be an instance of Client.")
        super().add(item)

    def get_str_models_name(self):
        return "Clients"

    def save_to_db(self, db_manager):
        query_select_all = "SELECT company_name FROM Clients;"
        _, db_clients = db_manager.fetch_data(query_select_all)  # Извлекаем заголовки и строки
        db_ids = {row[0] for row in db_clients}
        current_ids = {client.company_name for client in self._items}
        ids_to_delete = db_ids - current_ids

        if ids_to_delete:
            delete_query = "DELETE FROM Clients WHERE company_name = ?;"
            for company_name in ids_to_delete:
                db_manager.execute_query(delete_query, [company_name])

        for client in self._items:
            query = """
                MERGE INTO Clients AS target
                USING (SELECT ? AS company_name, ? AS phone, ? AS email, ? AS password, 
                              ? AS address, ? AS type, ? AS business_area, ? AS available_budget) AS source
                ON target.company_name = source.company_name
                WHEN MATCHED THEN
                    UPDATE SET
                        phone = source.phone,
                        email = source.email,
                        password = source.password,
                        address = source.address,
                        type = source.type,
                        business_area = source.business_area,
                        available_budget = source.available_budget
                WHEN NOT MATCHED THEN
                    INSERT (company_name, phone, email, password, address, type, business_area, available_budget)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
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

    @staticmethod
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

    def find_contains(self, company_name: str, email: str, phone: str, area: str):
        results = []
        for item in self._items:
            company_name_value = item.company_name.lower() if item.company_name else ""
            email_value = item.email.lower() if item.email else ""
            phone_value = item.phone.lower() if item.phone else ""
            area_value = item.business_area.lower() if item.business_area else ""

            if company_name.lower() in company_name_value and email.lower() in email_value \
                    and phone.lower() in phone_value and area.lower() in area_value:
                results.append(item)
        return results


class CampaignCollection(Collection):
    def add(self, item):
        if not isinstance(item, Campaign):
            raise TypeError("Item must be an instance of Campaign.")
        super().add(item)

    def get_str_models_name(self):
        return "Campaigns"

    def save_to_db(self, db_manager):
        query_select_all = "SELECT campaign_id FROM Campaigns;"
        _, db_campaigns = db_manager.fetch_data(query_select_all)
        db_ids = {row[0] for row in db_campaigns}
        current_ids = {campaign.campaign_id for campaign in self._items}
        ids_to_delete = db_ids - current_ids

        if ids_to_delete:
            delete_query = "DELETE FROM Campaigns WHERE campaign_id = ?;"
            for campaign_id in ids_to_delete:
                db_manager.execute_query(delete_query, [campaign_id])

        for campaign in self._items:
            query = """
                MERGE INTO Campaigns AS target
                USING (SELECT ? AS campaign_id, ? AS campaign_name, ? AS start_date, ? AS end_date, 
                              ? AS goal, ? AS budget, ? AS company_name) AS source
                ON target.campaign_id = source.campaign_id
                WHEN MATCHED THEN
                    UPDATE SET
                        campaign_name = source.campaign_name,
                        start_date = source.start_date,
                        end_date = source.end_date,
                        goal = source.goal,
                        budget = source.budget,
                        company_name = source.company_name
                WHEN NOT MATCHED THEN
                    INSERT (campaign_id, campaign_name, start_date, end_date, goal, budget, company_name)
                    VALUES (?, ?, ?, ?, ?, ?, ?);
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

    @staticmethod
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

    def find_contains(self, campaign_name: str, goal: str):
        results = CampaignCollection()
        for item in self._items:
            campaign_name_value = item.campaign_name.lower() if item.campaign_name else ""
            goal_value = item.goal.lower() if item.goal else ""

            if campaign_name.lower() in campaign_name_value and goal.lower() in goal_value:
                results.add(item)
        return results


class AdvertisementCollection(Collection):
    def add(self, item):
        if not isinstance(item, Advertisement):
            raise TypeError("Item must be an instance of Advertisement.")
        super().add(item)

    def get_str_models_name(self):
        return "Advertisements"

    def save_to_db(self, db_manager):
        query_select_all = "SELECT advertisement_id FROM Advertisements;"
        _, db_advertisements = db_manager.fetch_data(query_select_all)
        db_ids = {row[0] for row in db_advertisements}
        current_ids = {ad.advertisement_id for ad in self._items}
        ids_to_delete = db_ids - current_ids
        if ids_to_delete:
            delete_query = "DELETE FROM Advertisements WHERE advertisement_id = ?;"
            for advertisement_id in ids_to_delete:
                db_manager.execute_query(delete_query, [advertisement_id])
        for advertisement in self._items:
            query = """
                MERGE INTO Advertisements AS target
                USING (SELECT ? AS advertisement_id, ? AS text, ? AS format, ? AS send_time, ? AS topic, 
                              ? AS language, ? AS attachment, ? AS clicks, ? AS views, ? AS campaign_id, ? AS platform_id) AS source
                ON target.advertisement_id = source.advertisement_id
                WHEN MATCHED THEN
                    UPDATE SET
                        text = source.text,
                        format = source.format,
                        send_time = source.send_time,
                        topic = source.topic,
                        language = source.language,
                        attachment = source.attachment,
                        clicks = source.clicks,
                        views = source.views,
                        campaign_id = source.campaign_id,
                        platform_id = source.platform_id
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

    @staticmethod
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


    def filter(self, formats=None, languages=None, before_date=None, after_date=None, min_clicks=None):
        results = AdvertisementCollection()
        for item in self._items:
            if formats and item.format not in formats:
                continue
            if item.language is None and languages or languages and item.language not in languages:
                continue
            if item.send_time is None and before_date is not None or before_date and item.send_time and item.send_time >= before_date:
                continue
            if item.send_time is None and after_date is not None or after_date and item.send_time and item.send_time <= after_date:
                continue
            if item.clicks is None and min_clicks or min_clicks and item.clicks is not None and item.clicks <= min_clicks:
                continue
            results.add(item)
        return results


class MediaPlatformCollection(Collection):
    def add(self, item):
        if not isinstance(item, MediaPlatform):
            raise TypeError("Item must be an instance of Media Platform.")
        super().add(item)

    def get_str_models_name(self):
        return "Media Platforms"

    def save_to_db(self, db_manager):
        query_select_all = "SELECT platform_id FROM MediaPlatforms;"
        _, db_platforms = db_manager.fetch_data(query_select_all)
        db_ids = {row[0] for row in db_platforms}
        current_ids = {platform.platform_id for platform in self._items}
        ids_to_delete = db_ids - current_ids

        if ids_to_delete:
            delete_query = "DELETE FROM MediaPlatforms WHERE platform_id = ?;"
            for platform_id in ids_to_delete:
                db_manager.execute_query(delete_query, [platform_id])

        for platform in self._items:
            query = """
                MERGE INTO MediaPlatforms AS target
                USING (SELECT ? AS platform_id, ? AS platform_name, ? AS platform_type, 
                              ? AS main_ad_format, ? AS audience_size) AS source
                ON target.platform_id = source.platform_id
                WHEN MATCHED THEN
                    UPDATE SET
                        platform_name = source.platform_name,
                        platform_type = source.platform_type,
                        main_ad_format = source.main_ad_format,
                        audience_size = source.audience_size
                WHEN NOT MATCHED THEN
                    INSERT (platform_id, platform_name, platform_type, main_ad_format, audience_size)
                    VALUES (?, ?, ?, ?, ?);
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

    @staticmethod
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

class CampaignPlatformCollection(Collection):
    def add(self, item):
        if not isinstance(item, CampaignPlatform):
            raise TypeError("Item must be an instance of CampaignPlatform model.")
        super().add(item)

    def get_str_models_name(self):
        return "CampaignPlatformCollection"

    def save_to_db(self, db_manager):
        query_select_all = "SELECT campaign_id, platform_id FROM CampaignPlatforms;"
        _, db_campaign_platforms = db_manager.fetch_data(query_select_all)
        db_ids = {(row[0], row[1]) for row in db_campaign_platforms}
        current_ids = {(cp.campaign_id, cp.platform_id) for cp in self._items}
        ids_to_delete = db_ids - current_ids

        if ids_to_delete:
            delete_query = "DELETE FROM CampaignPlatforms WHERE campaign_id = ? AND platform_id = ?;"
            for campaign_id, platform_id in ids_to_delete:
                db_manager.execute_query(delete_query, [campaign_id, platform_id])

        for cp in self._items:
            query = """
                    MERGE INTO CampaignPlatforms AS target
                    USING (SELECT ? AS campaign_id, ? AS platform_id, ? AS budget_allocation) AS source
                    ON target.campaign_id = source.campaign_id AND target.platform_id = source.platform_id
                    WHEN MATCHED THEN
                        UPDATE SET
                            budget_allocation = source.budget_allocation
                    WHEN NOT MATCHED THEN
                        INSERT (campaign_id, platform_id, budget_allocation)
                        VALUES (?, ?, ?);
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

    @staticmethod
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


class AudienceSegmentCollection(Collection):
    def add(self, item):
        if not isinstance(item, AudienceSegment):
            raise TypeError("Item must be an instance of Audience Segment.")
        super().add(item)

    def get_str_models_name(self):
        return "Audience Segments"

    def save_to_db(self, db_manager):
        query_select_all = "SELECT segment_id FROM AudienceSegments;"
        _, db_segments = db_manager.fetch_data(query_select_all)
        db_ids = {row[0] for row in db_segments}
        current_ids = {segment.segment_id for segment in self._items}
        ids_to_delete = db_ids - current_ids

        if ids_to_delete:
            delete_query = "DELETE FROM AudienceSegments WHERE segment_id = ?;"
            for segment_id in ids_to_delete:
                db_manager.execute_query(delete_query, [segment_id])

        for segment in self._items:
            query = """
                    MERGE INTO AudienceSegments AS target
                    USING (SELECT ? AS segment_id, ? AS segment_name, ? AS age_range, ? AS gender, 
                                  ? AS location, ? AS general_interest, ? AS socioeconomic_status, 
                                  ? AS language, ? AS behavioral_characteristics, ? AS device_used) AS source
                    ON target.segment_id = source.segment_id
                    WHEN MATCHED THEN
                        UPDATE SET
                            segment_name = source.segment_name,
                            age_range = source.age_range,
                            gender = source.gender,
                            location = source.location,
                            general_interest = source.general_interest,
                            socioeconomic_status = source.socioeconomic_status,
                            language = source.language,
                            behavioral_characteristics = source.behavioral_characteristics,
                            device_used = source.device_used
                    WHEN NOT MATCHED THEN
                        INSERT (segment_id, segment_name, age_range, gender, location, general_interest, 
                                socioeconomic_status, language, behavioral_characteristics, device_used)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
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

    @staticmethod
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

    def filter(self, genders=None, locations=None, devices=None, min_age=None, max_age =None):
        results = AudienceSegmentCollection()
        for item in self._items:
            if genders and item.gender not in genders:
                continue
            if item.location is None and locations or locations and item.location not in locations:
                continue
            if item.device_used and devices is None or devices and item.device_used not in devices:
                continue
            if min_age and int(item.age_range[:2]) < min_age:
                continue
            if max_age and int(item.age_range[3:]) > max_age:
                continue
            results.add(item)
        return results

class SegmentPlatformCollection(Collection):
    def add(self, item):
        if not isinstance(item, SegmentPlatform):
            raise TypeError("Item must be an instance of SegmentPlatform model.")
        super().add(item)

    def get_str_models_name(self):
        return "SegmentPlatformCollection"

    def save_to_db(self, db_manager):
        query_select_all = "SELECT segment_id, platform_id FROM SegmentPlatforms;"
        _, db_segment_platforms = db_manager.fetch_data(query_select_all)
        db_ids = {(row[0], row[1]) for row in db_segment_platforms}
        current_ids = {(sp.segment_id, sp.platform_id) for sp in self._items}
        ids_to_delete = db_ids - current_ids

        if ids_to_delete:
            delete_query = "DELETE FROM SegmentPlatforms WHERE segment_id = ? AND platform_id = ?;"
            for segment_id, platform_id in ids_to_delete:
                db_manager.execute_query(delete_query, [segment_id, platform_id])

        for sp in self._items:
            query = """
                    MERGE INTO SegmentPlatforms AS target
                    USING (SELECT ? AS segment_id, ? AS platform_id) AS source
                    ON target.segment_id = source.segment_id AND target.platform_id = source.platform_id
                    WHEN MATCHED THEN
                        UPDATE SET segment_id = source.segment_id, platform_id = source.platform_id
                    WHEN NOT MATCHED THEN
                        INSERT (segment_id, platform_id)
                        VALUES (?, ?);
                """
            params = [
                sp.segment_id,
                sp.platform_id,
                sp.segment_id,
                sp.platform_id
            ]
            db_manager.execute_query(query, params)

    @staticmethod
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




class UserCollection(Collection):
    def add(self, item):
        if not isinstance(item, User):
            raise TypeError("Item must be an instance of User.")
        super().add(item)

    def get_str_models_name(self):
        return "Users"

    def save_to_db(self, db_manager):
        query_select_all = "SELECT email FROM Users;"
        _, db_users = db_manager.fetch_data(query_select_all)
        db_ids = {row[0] for row in db_users}
        current_ids = {user.email for user in self._items}
        ids_to_delete = db_ids - current_ids

        if ids_to_delete:
            delete_query = "DELETE FROM Users WHERE email = ?;"
            for email in ids_to_delete:
                db_manager.execute_query(delete_query, [email])

        for user in self._items:
            query = """
                    MERGE INTO Users AS target
                    USING (SELECT ? AS email, ? AS password, ? AS age, ? AS gender, 
                                  ? AS country, ? AS account_creation_date, 
                                  ? AS last_purchase_date, ? AS segment_id) AS source
                    ON target.email = source.email
                    WHEN MATCHED THEN
                        UPDATE SET
                            password = source.password,
                            age = source.age,
                            gender = source.gender,
                            country = source.country,
                            account_creation_date = source.account_creation_date,
                            last_purchase_date = source.last_purchase_date,
                            segment_id = source.segment_id
                    WHEN NOT MATCHED THEN
                        INSERT (email, password, age, gender, country, account_creation_date, 
                                last_purchase_date, segment_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
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

    @staticmethod
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