from Collections import *

DB_CONFIG = {
    "DSN": "AppDB",
    "Uid": "su",
    "Pwd": "LUDRHQ2g4"
}

ADVERTISEMENT_FORMATS = [
            "Text",
            "Image",
            "Video",
            "Audio",
            "HTML",
            "Animation",
            "Carousel",
            "Interactive",
            "Push Notification",
            "Story"
        ]

LANGUAGES = [
            "English", "Spanish", "Mandarin", "Hindi", "Arabic",
            "Bengali", "Portuguese", "Irish", "Japanese", "Punjabi",
            "German", "Korean", "French", "Turkish", "Vietnamese",
            "Italian", "Urdu", "Thai", "Polish", "Dutch",
            "Persian", "Swahili", "Romanian", "Greek", "Hungarian",
            "Czech", "Finnish", "Hebrew", "Malay", "Indonesian",
            "Norwegian", "Swedish", "Danish", "Bulgarian", "Serbian",
            "Croatian", "Slovak", "Ukrainian", "Lithuanian", "Latvian",
            "Estonian", "Filipino", "Tamil", "Kannada", "Gujarati",
            "Marathi", "Telugu", "Malayalam", "Sinhala", "Burmese"
        ]

LOCATIONS = [
    "USA", "Spain", "China", "India", "Saudi Arabia", "Canada",
    "Bangladesh", "Brazil", "Ireland", "Japan", "India (Punjab)",
    "Germany", "South Korea", "France", "Turkey", "Vietnam", "Australia",
    "Italy", "Pakistan", "Thailand", "Poland", "Netherlands",
    "Iran", "Kenya", "Romania", "Greece", "Hungary",
    "Czech Republic", "Finland", "Israel", "Malaysia", "Indonesia",
    "Norway", "Sweden", "Denmark", "Bulgaria", "Serbia",
    "Croatia", "Slovakia", "Ukraine", "Lithuania", "Latvia",
    "Estonia", "Philippines", "Sri Lanka (Tamil Nadu)", "India (Karnataka)", "India (Gujarat)",
    "India (Maharashtra)", "India (Andhra Pradesh)", "India (Kerala)", "Sri Lanka", "Myanmar (Burma)", "UK"
]


CLIENT_AREAS = [
            "IT",
            "Energy",
            "Construction",
            "Automotive",
            "Marketing",
            "Healthcare",
            "Education",
            "Finance",
            "Retail",
            "Manufacturing",
            "Logistics",
            "Telecommunications",
            "Real Estate",
            "Hospitality",
            "Entertainment",
            "Agriculture",
            "Food & Beverage",
            "Pharmaceuticals",
            "Aerospace",
            "Environmental Services",
            "Home Services",
            "Environment"
        ]

PLATFORM_TYPES = [
    "Social Media",
    "Video Streaming",
    "Search Engine",
    "E-Commerce",
    "Music Streaming",
    "Messaging",
    "Advertising Network",
    "Gaming",
    "News & Blogs",
    "Discussion Forum",
    "Mobile Ads",
    "Email Marketing",
    "Business Networking",
    "Influencer Marketing",
    "Retail Media",
    "Programmatic Ads",
    "OTT Platform",
    "Audio Ads",
    "Native Ads",
    "Affiliate Marketing",
    "Knowledge Base"
]

DEVICES = [
    "Smartphone",
    "Tablet",
    "Laptop",
    "Desktop",
    "Smart TV",
    "Gaming Console",
    "Smart Speaker"
]


Clients = ClientCollection()
Campaigns = CampaignCollection()
Advertisements = AdvertisementCollection()
MediaPlatforms = MediaPlatformCollection()
CampaignPlatforms = CampaignPlatformCollection()
AudienceSegments = AudienceSegmentCollection()
SegmentPlatforms = SegmentPlatformCollection()
Users = UserCollection()



