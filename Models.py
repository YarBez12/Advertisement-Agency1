import os
import re
from InitialData import *
from datetime import datetime


class Model:
    def __str__(self):
        return "Model"
    def GetData(self):
        return [], []

class Client(Model):
    def __init__(self, company_name, phone, email, password, type, business_area, address=None, available_budget=None):
        self.__company_name = company_name
        self.__phone = phone
        self.__email = email
        self.__password = password
        self.__address = address
        self.__type = type
        self.__business_area = business_area
        self.__available_budget = available_budget

    def __str__(self):
        return f"Client({self.__company_name}, {self.__type}, {self.__business_area})"

    def GetData(self):
        headers = ["Company Name", "Phone", "Email", "Password", "Address", "Type", "Business Area", "Available Budget"]
        data = [self.__company_name, self.__phone, self.__email, self.__password, self.__address, self.__type,
                self.__business_area, self.__available_budget]
        return headers, data

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        self.__password = value

    @property
    def company_name(self):
        return self.__company_name

    @company_name.setter
    def company_name(self, value):
        if len(value) <= 2:
            raise ValueError("Too short company name")
        self.__company_name = value

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value):
        pattern = r"^\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$"
        if not re.match(pattern, value):
            raise ValueError("Invalid phone format (e.g., +1234567890 or 123-456-7890).")
        self.__phone = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, value):
            raise ValueError("Invalid email format. Example: user@gmail.com")
        self.__email = value

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        if value:
            if len(value) < 5:
                raise ValueError("Address must be at least 5 characters long.")
            if not any(char.isalnum() for char in value):
                raise ValueError("Address must contain at least one alphanumeric character.")
        self.__address = value

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        if value not in ["Individual", "Company"]:
            raise ValueError("Type must be 'Individual' or 'Company'")
        self.__type = value

    @property
    def business_area(self):
        return self.__business_area

    @business_area.setter
    def business_area(self, value):
        if value not in CLIENT_AREAS:
            raise ValueError("Business area cannot be empty.")
        self.__business_area = value

    @property
    def available_budget(self):
        return self.__available_budget

    @available_budget.setter
    def available_budget(self, value):
        if value:
            if not isinstance(value, int):
                raise TypeError("Budget must be an integer number.")
            if value < 0:
                raise ValueError("Budget cannot be negative.")
        self.__available_budget = value


class Campaign(Model):
    def __init__(self, campaign_id, campaign_name, goal, company_name, start_date=None, end_date=None, budget=None):
        self.__campaign_id = campaign_id
        self.__campaign_name = campaign_name
        self.__start_date = start_date
        self.__end_date = end_date
        self.__goal = goal
        self.__budget = budget
        self.__company_name = company_name

    def __str__(self):
        return f"Campaign({self.__campaign_name or 'Unnamed'}, Goal: {self.__goal}, Company: {self.__company_name})"

    def GetData(self):
        headers = ["Campaign ID", "Campaign Name", "Start Date", "End Date", "Goal", "Budget", "Company Name"]
        data = [self.__campaign_id, self.__campaign_name, self.__start_date, self.__end_date, self.__goal,
                self.__budget, self.__company_name]
        return headers, data

    @property
    def campaign_id(self):
        return self.__campaign_id

    @campaign_id.setter
    def campaign_id(self, value):
        if not isinstance(value, int):
            raise TypeError("Campaign ID must be an integer.")
        if value <= 0:
            raise ValueError("Campaign ID must be a positive number.")
        self.__campaign_id = value

    @property
    def campaign_name(self):
        return self.__campaign_name

    @campaign_name.setter
    def campaign_name(self, value):
        if len(value) <= 2:
            raise ValueError("Too short campaign name.")
        self.__campaign_name = value

    @property
    def start_date(self):
        return self.__start_date

    @start_date.setter
    def start_date(self, value):
        if value and not self.__validate_date(value):
            raise ValueError("Start date must be in the format YYYY-MM-DD.")
        self.__start_date = value

    @property
    def end_date(self):
        return self.__end_date

    @end_date.setter
    def end_date(self, value):
        if value:
            if not self.__validate_date(value):
                raise ValueError("End date must be in the format YYYY-MM-DD.")
            if self.__start_date and value < self.__start_date:
                raise ValueError("End date cannot be earlier than start date.")
        self.__end_date = value

    @property
    def goal(self):
        return self.__goal

    @goal.setter
    def goal(self, value):
        if len(value) < 3:
            raise ValueError("Too short campaign goal.")
        self.__goal = value

    @property
    def budget(self):
        return self.__budget

    @budget.setter
    def budget(self, value):
        if value:
            if not isinstance(value, int):
                raise TypeError("Budget must be an integer number.")
            if value < 0:
                raise ValueError("Budget cannot be negative.")
        self.__budget = value

    @property
    def company_name(self):
        return self.__company_name

    @company_name.setter
    def company_name(self, value):
        if len(value) <= 2:
            raise ValueError("Too short company name.")
        self.__company_name = value

    @staticmethod
    def __validate_date(date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False



class Advertisement(Model):
    def __init__(self, advertisement_id, format, topic, text=None, send_time=None, language=None,
                 attachment=None, clicks=None, views=None, campaign_id=None, platform_id=None):
        self.__advertisement_id = advertisement_id
        self.__text = text
        self.__format = format
        self.__send_time = send_time
        self.__topic = topic
        self.__language = language
        self.__attachment = attachment
        self.__clicks = clicks
        self.__views = views
        self.__campaign_id = campaign_id
        self.__platform_id = platform_id

    def __str__(self):
        return f"Advertisement({self.__topic or 'No Topic'}, Format: {self.__format}, Language: {self.__language})"

    def GetData(self):
        headers = ["Advertisement ID", "Text", "Format", "Send Time", "Topic", "Language", "Attachment", "Clicks",
                   "Views", "Campaign ID", "Platform ID"]
        data = [self.__advertisement_id, self.__text, self.__format, self.__send_time, self.__topic, self.__language,
                self.__attachment, self.__clicks, self.__views, self.__campaign_id, self.__platform_id]
        return headers, data

    @property
    def advertisement_id(self):
        return self.__advertisement_id

    @advertisement_id.setter
    def advertisement_id(self, value):
        if not isinstance(value, int):
            raise TypeError("Advertisement ID must be an integer.")
        if value <= 0:
            raise ValueError("Advertisement ID must be a positive number.")
        self.__advertisement_id = value

    @property
    def format(self):
        return self.__format

    @format.setter
    def format(self, value):
        if value not in ADVERTISEMENT_FORMATS:
            raise ValueError("There is no such format in the system")
        self.__format = value

    @property
    def topic(self):
        return self.__topic

    @topic.setter
    def topic(self, value):
        if len(value) <= 2:
            raise ValueError("Too short topic.")
        self.__topic = value

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        if value and len(value) <= 7:
            raise ValueError("Too short text.")
        self.__text = value

    @property
    def send_time(self):
        return self.__send_time

    @send_time.setter
    def send_time(self, value):
        if value and not self.__validate_date(value):
            raise ValueError("Send time must be in the format YYYY-MM-DD.")
        self.__send_time = value

    @property
    def language(self):
        return self.__language

    @language.setter
    def language(self, value):
        if value and value not in LANGUAGES:
            raise ValueError("The is no such language in the system.")
        self.__language = value

    @property
    def attachment(self):
        return self.__attachment

    @attachment.setter
    def attachment(self, value):
        if value:
            if not isinstance(value, str):
                raise TypeError("Attachment must be a string representing the file path.")
            if not os.path.isfile(value):
                raise ValueError(f"Attachment must be a valid file path. File not found: {value}")
        self.__attachment = value

    @property
    def clicks(self):
        return self.__clicks

    @clicks.setter
    def clicks(self, value):
        if value:
            if not isinstance(value, int):
                raise TypeError("Clicks must be an integer number.")
            if value < 0:
                raise ValueError("Clicks must be a non-negative number.")

        self.__clicks = value

    @property
    def views(self):
        return self.__views

    @views.setter
    def views(self, value):
        if value:
            if not isinstance(value, int):
                raise TypeError("Views must be an integer number.")
            if value < 0:
                raise ValueError("Views must be a non-negative number.")
        self.__views = value

    # Property for campaign_id
    @property
    def campaign_id(self):
        return self.__campaign_id

    @campaign_id.setter
    def campaign_id(self, value):
        if value:
            if not isinstance(value, int):
                raise TypeError("Campaign ID must be an integer number.")
            if value <= 0:
                raise ValueError("Campaign ID must be a positive number.")
        self.__campaign_id = value


    @property
    def platform_id(self):
        return self.__platform_id

    @platform_id.setter
    def platform_id(self, value):
        if value:
            if not isinstance(value, int):
                raise TypeError("Platform ID must be an integer number.")
            if value <= 0:
                raise ValueError("Platform ID must be a positive number.")

        self.__platform_id = value

    @staticmethod
    def __validate_date(date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False



class MediaPlatform(Model):
    def __init__(self, platform_id, platform_name, platform_type=None, main_ad_format=None, audience_size=None):
        self.__platform_id = platform_id
        self.__platform_name = platform_name
        self.__platform_type = platform_type
        self.__main_ad_format = main_ad_format
        self.__audience_size = audience_size

    def __str__(self):
        return f"MediaPlatform({self.__platform_name}, Type: {self.__platform_type})"

    def GetData(self):
        headers = ["Platform ID", "Platform Name", "Type", "Main Ad Format", "Audience Size"]
        data = [self.__platform_id, self.__platform_name, self.__platform_type, self.__main_ad_format,
                self.__audience_size]
        return headers, data

    @property
    def platform_id(self):
        return self.__platform_id

    @platform_id.setter
    def platform_id(self, value):
        if not isinstance(value, int):
            raise TypeError("Platform ID must be an integer number.")
        if value <= 0:
            raise ValueError("Platform ID must be a positive number.")
        self.__platform_id = value

    @property
    def platform_name(self):
        return self.__platform_name

    @platform_name.setter
    def platform_name(self, value):
        if not value:
            raise ValueError("Platform name is empty.")
        self.__platform_name = value

    @property
    def platform_type(self):
        return self.__platform_type

    @platform_type.setter
    def platform_type(self, value):
        if value not in PLATFORM_TYPES:
            raise ValueError("There is no such platform type in the system")
        self.__platform_type = value

    @property
    def main_ad_format(self):
        return self.__main_ad_format

    @main_ad_format.setter
    def main_ad_format(self, value):
        if value and value not in ADVERTISEMENT_FORMATS:
            raise ValueError("There is no such advertisement format in the system")
        self.__main_ad_format = value

    @property
    def audience_size(self):
        return self.__audience_size

    @audience_size.setter
    def audience_size(self, value):
        if value:
            if not isinstance(value, int):
                raise TypeError("Audience size must be an integer number.")
            if value < 0:
                raise ValueError("Audience size cannot be negative.")
        self.__audience_size = value



class CampaignPlatform(Model):
    def __init__(self, campaign_id, platform_id, budget_allocation=None):
        self.__campaign_id = campaign_id
        self.__platform_id = platform_id
        self.__budget_allocation = budget_allocation

    def __str__(self):
        return f"CampaignPlatform(Campaign ID: {self.__campaign_id}, Platform ID: {self.__platform_id})"

    def GetData(self):
        headers = ["Campaign ID", "Platform ID", "Budget Allocation"]
        data = [self.__campaign_id, self.__platform_id, self.__budget_allocation]
        return headers, data

    @property
    def campaign_id(self):
        return self.__campaign_id

    @campaign_id.setter
    def campaign_id(self, value):
        if not isinstance(value, int):
            raise TypeError("Campaign ID must be an integer.")
        if value <= 0:
            raise ValueError("Campaign ID must be a positive number.")
        self.__campaign_id = value

    @property
    def platform_id(self):
        return self.__platform_id

    @platform_id.setter
    def platform_id(self, value):
        if not isinstance(value, int):
            raise TypeError("Platform ID must be an integer.")
        if value <= 0:
            raise ValueError("Platform ID must be a positive number.")

        self.__platform_id = value

    @property
    def budget_allocation(self):
        return self.__budget_allocation

    @budget_allocation.setter
    def budget_allocation(self, value):
        if value:
            if not isinstance(value, int):
                raise TypeError("Budget allocation must be an integer number.")
            if value < 0:
                raise ValueError("Budget allocation cannot be negative.")
        self.__budget_allocation = value



class AudienceSegment(Model):
    def __init__(self, segment_id, age_range, gender, language, segment_name=None, location=None, general_interest=None,
                 socioeconomic_status=None, behavioral_characteristics=None, device_used=None):
        self.__segment_id = segment_id
        self.__segment_name = segment_name
        self.__age_range = age_range
        self.__gender = gender
        self.__location = location
        self.__general_interest = general_interest
        self.__socioeconomic_status = socioeconomic_status
        self.__language = language
        self.__behavioral_characteristics = behavioral_characteristics
        self.__device_used = device_used

    def __str__(self):
        return f"AudienceSegment({self.__segment_name or 'Unnamed'}, Age Range: {self.__age_range}, Gender: {self.__gender})"

    def GetData(self):
        headers = ["Segment ID", "Name", "Age Range", "Gender", "Location", "General Interest",
                   "Socioeconomic Status", "Language", "Behavioral Characteristics", "Device Used"]
        data = [self.__segment_id, self.__segment_name, self.__age_range, self.__gender, self.__location,
                self.__general_interest, self.__socioeconomic_status, self.__language,
                self.__behavioral_characteristics, self.__device_used]
        return headers, data

    @property
    def segment_id(self):
        return self.__segment_id

    @segment_id.setter
    def segment_id(self, value):
        if not isinstance(value, int):
            raise TypeError("Segment ID must be an integer number.")
        if value <= 0:
            raise ValueError("Segment ID must be a positive integer.")

        self.__segment_id = value

    @property
    def segment_name(self):
        return self.__segment_name

    @segment_name.setter
    def segment_name(self, value):
        if value and len(value) <= 3:
            raise ValueError("Too short audience segment name.")
        self.__segment_name = value

    @property
    def age_range(self):
        return self.__age_range

    @age_range.setter
    def age_range(self, value):
        if not isinstance(value, str) or "-" not in value:
            raise ValueError("Age range must be a string in the format 'min-max'.")
        self.__age_range = value

    @property
    def gender(self):
        return self.__gender

    @gender.setter
    def gender(self, value):
        if value not in ["Male", "Female", "Other"]:
            raise ValueError("Gender must be 'Male', 'Female', or 'Other'.")
        self.__gender = value

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, value):
        if value and value not in LOCATIONS:
            raise ValueError("There is no such location in the system.")
        self.__location = value

    @property
    def general_interest(self):
        return self.__general_interest

    @general_interest.setter
    def general_interest(self, value):
        if value and len(value) <= 3:
            raise ValueError("Too short interest.")
        self.__general_interest = value

    @property
    def socioeconomic_status(self):
        return self.__socioeconomic_status

    @socioeconomic_status.setter
    def socioeconomic_status(self, value):
        if value and len(value) <= 3:
            raise ValueError("Too short status.")
        self.__socioeconomic_status = value

    @property
    def language(self):
        return self.__language

    @language.setter
    def language(self, value):
        if value not in LANGUAGES:
            raise ValueError("There is no such language in the system.")
        self.__language = value

    @property
    def behavioral_characteristics(self):
        return self.__behavioral_characteristics

    @behavioral_characteristics.setter
    def behavioral_characteristics(self, value):
        if value and len(value) <= 5:
            raise ValueError("Too short characteristics.")
        self.__behavioral_characteristics = value

    @property
    def device_used(self):
        return self.__device_used

    @device_used.setter
    def device_used(self, value):
        if value and len(value) < 2:
            raise ValueError("Too short device name.")
        self.__device_used = value




class SegmentPlatform(Model):
    def __init__(self, segment_id, platform_id):
        self.__segment_id = segment_id
        self.__platform_id = platform_id

    def __str__(self):
        return f"SegmentPlatform(Segment ID: {self.__segment_id}, Platform ID: {self.__platform_id})"

    def GetData(self):
        headers = ["Segment ID", "Platform ID"]
        data = [self.__segment_id, self.__platform_id]
        return headers, data

    @property
    def segment_id(self):
        return self.__segment_id

    @segment_id.setter
    def segment_id(self, value):
        if not isinstance(value, int):
            raise TypeError("Segment ID must be an integer number.")
        if value <= 0:
            raise ValueError("Segment ID must be a positive integer.")
        self.__segment_id = value

    @property
    def platform_id(self):
        return self.__platform_id

    @platform_id.setter
    def platform_id(self, value):
        if not isinstance(value, int):
            raise TypeError("Platform ID must be an integer number.")
        if value <= 0:
            raise ValueError("Platform ID must be a positive integer.")
        self.__platform_id = value


class CampaignSegment(Model):
    def __init__(self, campaign_id, segment_id, ad_frequency=None):
        self.__campaign_id = campaign_id
        self.__segment_id = segment_id
        self.__ad_frequency = ad_frequency

    def __str__(self):
        return f"CampaignSegment(Campaign ID: {self.__campaign_id}, Segment ID: {self.__segment_id})"

    def GetData(self):
        headers = ["Campaign ID", "Segment ID", "Ad Frequency"]
        data = [self.__campaign_id, self.__segment_id, self.__ad_frequency]
        return headers, data

    @property
    def campaign_id(self):
        return self.__campaign_id

    @campaign_id.setter
    def campaign_id(self, value):
        if not isinstance(value, int):
            raise TypeError("Campaign ID must be an integer number.")
        if value <= 0:
            raise ValueError("Campaign ID must be a positive integer.")
        self.__campaign_id = value

    @property
    def segment_id(self):
        return self.__segment_id

    @segment_id.setter
    def segment_id(self, value):
        if not isinstance(value, int):
            raise TypeError("Segment ID must be an integer number.")
        if value <= 0:
            raise ValueError("Segment ID must be a positive integer.")
        self.__segment_id = value

    @property
    def ad_frequency(self):
        return self.__ad_frequency

    @ad_frequency.setter
    def ad_frequency(self, value):
        if value is not None:
            if not isinstance(value, int):
                raise TypeError("Ad Frequency must be an integer number.")
            if value <= 0:
                raise ValueError("Ad Frequency must be a positive integer.")
        self.__ad_frequency = value


class User(Model):
    def __init__(self, email, password, age, gender, country, account_creation_date,
                 last_purchase_date=None, segment_id=None):
        self.__email = email
        self.__password = password
        self.__age = age
        self.__gender = gender
        self.__country = country
        self.__account_creation_date = account_creation_date
        self.__last_purchase_date = last_purchase_date
        self.__segment_id = segment_id

    def __str__(self):
        return f"User(Email: {self.__email}, Age: {self.__age}, Gender: {self.__gender})"

    def GetData(self):
        headers = ["Email", "Password", "Age", "Gender", "Country", "Account Creation Date", "Last Purchase Date", "Segment ID"]
        data = [self.__email, self.__password, self.__age, self.__gender, self.__country,
                self.__account_creation_date, self.__last_purchase_date, self.__segment_id]
        return headers, data

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, value):
            raise ValueError("Invalid email format. Example: user@gmail.com")
        self.__email = value

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        self.__password = value

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        if not isinstance(value, int):
            raise TypeError("Age must be an integer number.")
        if value <= 0:
            raise ValueError("Age must be a positive number.")

        self.__age = value

    @property
    def gender(self):
        return self.__gender

    @gender.setter
    def gender(self, value):
        if value not in ["Male", "Female", "Other"]:
            raise ValueError("Gender must be 'Male', 'Female', or 'Other'.")
        self.__gender = value

    @property
    def country(self):
        return self.__country

    @country.setter
    def country(self, value):
        if value not in LOCATIONS:
            raise ValueError("There is no such country in our system")
        self.__country = value

    @property
    def account_creation_date(self):
        return self.__account_creation_date

    @account_creation_date.setter
    def account_creation_date(self, value):
        if not self.__validate_date(value):
            raise ValueError("Account creation date must be in the format YYYY-MM-DD.")
        self.__account_creation_date = value

    @property
    def last_purchase_date(self):
        return self.__last_purchase_date

    @last_purchase_date.setter
    def last_purchase_date(self, value):
        if value:
            if not self.__validate_date(value):
                raise ValueError("Last purchase date must be in the format YYYY-MM-DD.")
            if value < self.__account_creation_date:
                raise ValueError("Last purchase date cannot be earlier than account creation date.")
        self.__last_purchase_date = value

    @property
    def segment_id(self):
        return self.__segment_id

    @segment_id.setter
    def segment_id(self, value):
        if value is not None:
            if not isinstance(value, int):
                raise TypeError("Segment ID must be an integer number.")
            if value <= 0:
                raise ValueError("Segment ID must be a positive integer.")
        self.__segment_id = value

    @staticmethod
    def __validate_date(date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False