class Client:
    def __init__(self, company_name, phone, email, type, business_area, address=None, available_budget=None):
        self.company_name = company_name
        self.phone = phone
        self.email = email
        self.address = address
        self.type = type
        self.business_area = business_area
        self.available_budget = available_budget


class Campaign:
    def __init__(self, campaign_id, name, goal, company_name, start_date=None, end_date=None,  budget=None):
        self.campaign_id = campaign_id
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.goal = goal
        self.budget = budget
        self.company_name = company_name


class Advertisement:
    def __init__(self, advertisement_id, format=None, topic=None, text=None, send_time=None, language=None,
                 attachment=None, clicks=None, views=None, campaign_id=None, platform_id=None):
        self.advertisement_id = advertisement_id
        self.text = text
        self.format = format
        self.send_time = send_time
        self.topic = topic
        self.language = language
        self.attachment = attachment
        self.clicks = clicks
        self.views = views
        self.campaign_id = campaign_id
        self.platform_id = platform_id


class MediaPlatform:
    def __init__(self, platform_id, name, platform_type=None, main_ad_format=None, audience_size=None):
        self.platform_id = platform_id
        self.name = name
        self.platform_type = platform_type
        self.main_ad_format = main_ad_format
        self.audience_size = audience_size


class CampaignPlatform:
    def __init__(self, campaign_id, platform_id, budget_allocation=None):
        self.campaign_id = campaign_id
        self.platform_id = platform_id
        self.budget_allocation = budget_allocation


class AudienceSegment:
    def __init__(self, segment_id, age_range, gender, language, name=None, location=None, general_interest=None,
                 socioeconomic_status=None, behavioral_characteristics=None, device_used=None):
        self.segment_id = segment_id
        self.name = name
        self.age_range = age_range
        self.gender = gender
        self.location = location
        self.general_interest = general_interest
        self.socioeconomic_status = socioeconomic_status
        self.language = language
        self.behavioral_characteristics = behavioral_characteristics
        self.device_used = device_used



class SegmentPlatform:
    def __init__(self, segment_id, platform_id):
        self.segment_id = segment_id
        self.platform_id = platform_id


class CampaignSegment:
    def __init__(self, campaign_id, segment_id, ad_frequency=None):
        self.campaign_id = campaign_id
        self.segment_id = segment_id
        self.ad_frequency = ad_frequency


class User:
    def __init__(self, user_id, age, gender, country, account_creation_date,
                 last_purchase_date=None, segment_id=None):
        self.user_id = user_id
        self.age = age
        self.gender = gender
        self.country = country
        self.account_creation_date = account_creation_date
        self.last_purchase_date = last_purchase_date
        self.segment_id = segment_id
