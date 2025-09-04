# Complete PRIME Categories Mapping (114 categories)
# Based on the guidelines PDF and Prime_report.csv structure

PRIME_CATEGORIES = {
    # ANSWERS Categories (with subclasses)
    "ANSWERS_General": "General advice and recommendations",
    "ANSWERS_Autos": "Auto advice and recommendations", 
    "ANSWERS_Dreams": "Dream interpretation advice",
    "ANSWERS_Education": "Educational advice and recommendations",
    "ANSWERS_Finance": "Financial advice and recommendations",
    "ANSWERS_Food": "Food and cooking advice",
    "ANSWERS_Games": "Gaming advice and recommendations", 
    "ANSWERS_Gardening": "Gardening advice and recommendations",
    "ANSWERS_Health": "Health advice and recommendations",
    "ANSWERS_Jobs": "Job and career advice",
    "ANSWERS_Legal": "Legal advice and recommendations",
    "ANSWERS_Music": "Music advice and recommendations",
    "ANSWERS_Parenting": "Parenting advice and recommendations",
    "ANSWERS_Relationships": "Relationship advice",
    "ANSWERS_Religion": "Religious advice and guidance",
    "ANSWERS_Science_Math": "Science and math explanations",
    "ANSWERS_Sports": "Sports advice and recommendations",
    "ANSWERS_Tech": "Technology advice and recommendations",
    "ANSWERS_Travel": "Travel advice and recommendations",
    "ANSWERS_Weddings": "Wedding advice and recommendations",
    "ANSWERS_Other": "Other advice and recommendations",

    # QUICKFACT Categories (with subclasses)
    "QUICKFACT_Astronomical_Event": "Astronomical events and dates",
    "QUICKFACT_Calories": "Calorie information",
    "QUICKFACT_Conversion": "Unit conversions",
    "QUICKFACT_Crossword": "Crossword clues and answers",
    "QUICKFACT_Define": "Definitions and meanings",
    "QUICKFACT_Directions": "Driving directions",
    "QUICKFACT_Flight_Tracker": "Flight status and tracking",
    "QUICKFACT_Holiday": "Holiday dates and information",
    "QUICKFACT_Phone_Codes": "Phone area codes",
    "QUICKFACT_Phone_Number": "Phone number lookup",
    "QUICKFACT_Sunrise_Sunset": "Sunrise and sunset times",
    "QUICKFACT_Table": "Data tables and charts",
    "QUICKFACT_Time": "Time zones and current time",
    "QUICKFACT_Traffic": "Traffic conditions",
    "QUICKFACT_Translate": "Language translation",
    "QUICKFACT_Zip_Code": "Zip code information",

    # Notable Person Categories
    "Notable_Person_Actor": "Famous actors and actresses",
    "Notable_Person_Athlete": "Famous athletes and sports figures", 
    "Notable_Person_Musician": "Famous musicians and singers",
    "Notable_Person_Other": "Other notable people",

    # Shopping Category
    "Shopping": "Product information, prices, reviews",

    # Local Categories
    "Local_Category": "Local business categories",
    "Local_Chain": "Chain store locations",
    "Local_Single": "Individual local businesses",

    # News Category
    "News": "Breaking news and current events",

    # Place Category  
    "Place": "Geographic locations and maps",

    # Weather Category
    "Weather": "Weather conditions and forecasts",

    # Movie Categories
    "Movie_Current": "Current movies and showtimes",
    "Movie_Non_current": "Older movies and film information",

    # TV Show Category
    "TV_Show": "Television shows and episodes",

    # Sports Team Category
    "Sports_Team": "Sports teams, scores, schedules",

    # OTHER Categories (when no other PRIME fits)
    "OTHER_Academic": "Academic and scholarly content",
    "OTHER_Adult": "Adult content",
    "OTHER_Airport": "Airport information",
    "OTHER_App": "Mobile applications",
    "OTHER_Events": "Events and activities",
    "OTHER_Jobs": "Job listings and employment",
    "OTHER_Music": "Music content not covered elsewhere",
    "OTHER_Person_Search": "Searching for people",
    "OTHER_Real_Estate": "Real estate information",
    "OTHER_Web": "Website navigation",
    "OTHER_Wiki": "Wikipedia-style information",
    "OTHER_None_of_These": "Does not fit any category",

    # Additional categories from Prime_report.csv analysis
    "Navigational": "Website navigation queries",
    "Entertainment_Celebrities": "Celebrity information",
    "Image_only": "Image search queries",
    "Jobs_and_Real_Estate": "Job and real estate combined",
    "Cannot_judge": "Cannot determine classification",
    "Celeb_other": "Other celebrity content",
    "Reference_Health_Lottery": "Health and lottery reference",
    "Quickfacts_Define_Crossword": "Quick facts and definitions",
    "Product": "Product information",
    "Place_and_Venue": "Places and venues",
    "Other_categories": "Other miscellaneous categories",
    "News_undercounted": "News content (undercounted)",
    "Sports_teams_leagues_athletes": "Sports-related content",
    "Autos": "Automotive content",
    "Other_Adult_and_Web_results": "Adult and web results"
}

# Classification Schema Mappings
ANNOTATION_SCHEMA = {
    "ambiguous": "Query has multiple distinct meanings",
    "misspelled_malformed": "Query has spelling/grammar errors", 
    "non_market_language": "Query is not in English"
}

ENTITY_SCHEMA = {
    "person_notable": "Famous/notable people",
    "person_non_notable": "Non-famous people", 
    "type_of_person": "Categories of people",
    "specific_organization": "Named organizations/companies",
    "type_of_organization": "Categories of organizations",
    "media_title": "Named books/movies/songs/games",
    "type_of_media": "Categories of media",
    "specific_product": "Named product models",
    "type_of_product": "Product categories",
    "specific_place_city": "Named cities",
    "specific_place_poi": "Points of interest",
    "specific_place_address": "Street addresses",
    "specific_place_other": "Other specific places",
    "type_of_place": "Place categories",
    "specific_event": "Named events",
    "type_of_event": "Event categories", 
    "website": "Named websites/URLs",
    "other_entity": "Other entities"
}

INTENT_SCHEMA = {
    "website": "Navigate to specific website",
    "porn_illegal": "Adult/illegal content",
    "images_videos": "Visual media search",
    "local_info": "Local business information",
    "event_info": "Event information/tickets",
    "news": "News articles",
    "shopping": "Product research/purchase",
    "simple_fact": "Quick factual answer",
    "research": "Detailed information research",
    "other_intent": "Other intentions"
}

TOPIC_SCHEMA = {
    "autos": "Cars, motorcycles, automotive",
    "education": "Schools, learning, educational resources",
    "entertainment_books": "Books, authors, libraries",
    "entertainment_games": "Video games, board games",
    "entertainment_movies": "Films, actors, theaters",
    "entertainment_music": "Musicians, songs, concerts",
    "entertainment_tv": "TV shows, networks, streaming",
    "entertainment_other": "Other entertainment",
    "environment": "Ecology, climate, conservation",
    "finance": "Banking, investments, insurance",
    "food_dining": "Restaurants, recipes, cooking",
    "government_politics": "Government services, politics",
    "health_medical": "Medical conditions, healthcare",
    "home_garden": "Home improvement, gardening",
    "jobs": "Employment, careers",
    "legal": "Law, lawyers, legal issues",
    "people_search": "Finding individuals",
    "personal_goods": "Clothing, beauty, personal care",
    "pets_animals": "Pet care, animal information",
    "real_estate": "Property sales, rentals",
    "religion": "Religious topics, worship",
    "retailers": "General merchandise stores",
    "social_networking": "Social media, dating",
    "sports_outdoors": "Sports, recreation, outdoor activities",
    "tech_electronics": "Technology, computers, electronics",
    "transit_traffic": "Transportation, commuting",
    "travel_lodging": "Travel, tourism, hotels",
    "weather": "Weather conditions, forecasts",
    "other_topic": "Topics not covered above"
}

def get_prime_category_from_classification(classification_result):
    """
    Map classification result to proper PRIME category
    """
    # This function would analyze the classification and return the appropriate PRIME category
    # Implementation would depend on the specific logic for mapping
    pass

def validate_prime_category(category):
    """
    Validate that a PRIME category exists in our mapping
    """
    return category in PRIME_CATEGORIES

def get_all_prime_categories():
    """
    Get list of all 114 PRIME categories
    """
    return list(PRIME_CATEGORIES.keys())

def get_meta_category(prime_category):
    """
    Map PRIME category to Meta category for aggregation
    """
    meta_mapping = {
        # Answers categories
        **{k: "Answers" for k in PRIME_CATEGORIES.keys() if k.startswith("ANSWERS_")},
        
        # Quickfact categories  
        **{k: "Quickfacts: Define, Crossword," for k in PRIME_CATEGORIES.keys() if k.startswith("QUICKFACT_")},
        
        # Entertainment categories
        "Notable_Person_Actor": "Entertainment: Celebrities,",
        "Notable_Person_Musician": "Entertainment: Celebrities,",
        "Notable_Person_Athlete": "Sports teams, leagues, athletes",
        "Notable_Person_Other": "Entertainment: Celebrities,",
        
        # Local and navigation
        "Local_Category": "Local", 
        "Local_Chain": "Local",
        "Local_Single": "Local",
        "Navigational": "Navigational",
        
        # Shopping and products
        "Shopping": "Product",
        
        # Places and venues
        "Place": "Place and Venue",
        
        # Weather
        "Weather": "Weather",
        
        # News
        "News": "News (undercounted)",
        
        # Other categories
        "OTHER_Adult": "Other: Adult and Web results",
        "OTHER_Web": "Other: Adult and Web results", 
        "OTHER_None_of_These": "Other categories",
    }
    
    return meta_mapping.get(prime_category, "Other categories")
