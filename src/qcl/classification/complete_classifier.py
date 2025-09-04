"""Query classifier using OpenAI GPT-4.1"""

from qcl.data.prime_categories_mapping import (
    PRIME_CATEGORIES,
    validate_prime_category,
    get_meta_category,
    ANNOTATION_SCHEMA,
    ENTITY_SCHEMA,
    INTENT_SCHEMA,
    TOPIC_SCHEMA
)

import logging
import json  
import time
import re
from pathlib import Path
from typing import Dict, Any, List
from openai import OpenAI

from ..data.models import Query, ClassificationResult

logger = logging.getLogger(__name__)

class QueryClassifier:
    """Simple GPT-4.1 based query classifier"""

    def __init__(self, config):
        self.config = config
        self.client = OpenAI(api_key=config.openai_api_key)
        self.classification_prompt = self._load_classification_prompt()
    
    def _load_classification_prompt(self) -> str:
        """Load the classification prompt template"""
        prompt_file = Path("configs/classification_prompt.txt")
        
        if prompt_file.exists():
            with open(prompt_file, 'r') as f:
                return f.read()
        
        # Default prompt if file doesn't exist (this is your new 5-schema prompt)
        return """You are an expert Query Classification Analyst following the official Query Classification Guidelines for LLM.

CRITICAL: You must classify each query across ALL FIVE schemas exactly as specified in the guidelines.

Classification Schemas:
1. ANNOTATION SCHEMA (mark only if applicable):
   - ambiguous: Query has multiple distinct meanings or unclear intent
   - misspelled_malformed: Spelling errors, malformed syntax, poor grammar  
   - non_market_language: Not in English or common English phrases

2. ENTITY SCHEMA (identify ALL entities):
   - person_notable: Current, historical, or fictional famous people
   - person_non_notable: People without public fame
   - type_of_person: Categories by gender, occupation, age, ethnicity
   - specific_organization: Named companies, teams, bands, schools
   - type_of_organization: Categories of organizations/businesses
   - media_title: Named books, songs, movies, albums, games, newspapers
   - type_of_media: Categories of media formats
   - specific_product: Named product models, families, manufacturers
   - type_of_product: Product categories
   - specific_place_city: Named cities
   - specific_place_poi: Points of interest (landmarks, attractions)
   - specific_place_address: Street addresses
   - specific_place_other: States, countries, regions, zip codes
   - type_of_place: Place categories
   - specific_event: Named specific events
   - type_of_event: Event categories
   - website: Named websites or URLs
   - other_entity: Phone numbers, diseases, foods, animals, etc.

3. INTENT SCHEMA (mark ALL applicable):
   - website: Navigate to specific website
   - porn_illegal: Adult content, illegal activities
   - images_videos: Visual media (explicit or implicit)
   - local_info: Local business/service information
   - event_info: Information about scheduled events
   - news: Current, evolving news stories
   - shopping: Product research or purchase intent
   - simple_fact: Short factual answers (≤8 words)
   - research: Longer, exploratory information needs
   - other_intent: Intents not covered above

4. TOPIC SCHEMA (mark ALL applicable):
   - autos: Cars, motorcycles, parts, dealers, mechanics
   - education: Schools, teaching, studying, educational resources
   - entertainment_books: Books, authors, libraries, e-readers
   - entertainment_games: Video games, board games, card games, lottery
   - entertainment_movies: Films, actors, theaters, showtimes
   - entertainment_music: Musicians, songs, concerts, music venues
   - entertainment_tv: TV shows, networks, streaming, TV personalities
   - entertainment_other: Comics, radio, theater, art, other entertainment
   - environment: Ecology, green issues, climate, conservation
   - finance: Banking, investments, insurance, financial services
   - food_dining: Restaurants, recipes, food, beverages, cooking
   - government_politics: Government services, politics, civic issues
   - health_medical: Medical conditions, treatments, healthcare providers
   - home_garden: Home improvement, gardening, furniture, appliances
   - jobs: Employment, careers, job search, workplace issues
   - legal: Law, lawyers, legal issues, court cases
   - people_search: Finding non-famous individuals
   - personal_goods: Clothing, accessories, beauty, personal care
   - pets_animals: Pet care, veterinarians, animal information
   - real_estate: Property sales, rentals, real estate services
   - religion: Religious topics, places of worship, spiritual matters
   - retailers: General merchandise stores (not specialized)
   - social_networking: Social media, dating, communication platforms
   - sports_outdoors: Sports, teams, outdoor activities, recreation
   - tech_electronics: Technology, computers, software, electronics
   - transit_traffic: Local transportation, traffic, commuting
   - travel_lodging: Travel, tourism, hotels, destinations
   - weather: Weather conditions, forecasts, weather events
   - other_topic: Topics not covered above

5. PRIME CATEGORY (select EXACTLY ONE from 114 categories):

ANSWERS Categories:
- ANSWERS_General, ANSWERS_Autos, ANSWERS_Dreams, ANSWERS_Education, ANSWERS_Finance, ANSWERS_Food, ANSWERS_Games, ANSWERS_Gardening, ANSWERS_Health, ANSWERS_Jobs, ANSWERS_Legal, ANSWERS_Music, ANSWERS_Parenting, ANSWERS_Relationships, ANSWERS_Religion, ANSWERS_Science_Math, ANSWERS_Sports, ANSWERS_Tech, ANSWERS_Travel, ANSWERS_Weddings, ANSWERS_Other

QUICKFACT Categories:
- QUICKFACT_Astronomical_Event, QUICKFACT_Calories, QUICKFACT_Conversion, QUICKFACT_Crossword, QUICKFACT_Define, QUICKFACT_Directions, QUICKFACT_Flight_Tracker, QUICKFACT_Holiday, QUICKFACT_Phone_Codes, QUICKFACT_Phone_Number, QUICKFACT_Sunrise_Sunset, QUICKFACT_Table, QUICKFACT_Time, QUICKFACT_Traffic, QUICKFACT_Translate, QUICKFACT_Zip_Code

Specific Experience Categories:
- Notable_Person_Actor, Notable_Person_Athlete, Notable_Person_Musician, Notable_Person_Other
- Shopping
- Local_Category, Local_Chain, Local_Single
- News
- Place
- Weather
- Movie_Current, Movie_Non_current
- TV_Show
- Sports_Team

OTHER Categories:
- OTHER_Academic, OTHER_Adult, OTHER_Airport, OTHER_App, OTHER_Events, OTHER_Jobs, OTHER_Music, OTHER_Person_Search, OTHER_Real_Estate, OTHER_Web, OTHER_Wiki, OTHER_None_of_These

Query to classify: "{query_text}"

Guidelines context: {guidelines_context}

Respond with EXACTLY this JSON format:

{{
  "annotation_schema": {{
    "ambiguous": false,
    "misspelled_malformed": false,
    "non_market_language": false
  }},
  "entity_schema": {{
    "person_notable": [],
    "person_non_notable": [],
    "type_of_person": [],
    "specific_organization": [],
    "type_of_organization": [],
    "media_title": [],
    "type_of_media": [],
    "specific_product": [],
    "type_of_product": [],
    "specific_place_city": [],
    "specific_place_poi": [],
    "specific_place_address": [],
    "specific_place_other": [],
    "type_of_place": [],
    "specific_event": [],
    "type_of_event": [],
    "website": [],
    "other_entity": []
  }},
  "intent_schema": {{
    "website": false,
    "porn_illegal": false,
    "images_videos": false,
    "local_info": false,
    "event_info": false,
    "news": false,
    "shopping": false,
    "simple_fact": false,
    "research": false,
    "other_intent": false
  }},
  "topic_schema": {{
    "autos": false,
    "education": false,
    "entertainment_books": false,
    "entertainment_games": false,
    "entertainment_movies": false,
    "entertainment_music": false,
    "entertainment_tv": false,
    "entertainment_other": false,
    "environment": false,
    "finance": false,
    "food_dining": false,
    "government_politics": false,
    "health_medical": false,
    "home_garden": false,
    "jobs": false,
    "legal": false,
    "people_search": false,
    "personal_goods": false,
    "pets_animals": false,
    "real_estate": false,
    "religion": false,
    "retailers": false,
    "social_networking": false,
    "sports_outdoors": false,
    "tech_electronics": false,
    "transit_traffic": false,
    "travel_lodging": false,
    "weather": false,
    "other_topic": false
  }},
  "prime_category": "EXACT_PRIME_CATEGORY_NAME",
  "research_notes": "Brief explanation of classification decisions",
  "confidence_score": 0.95
}}

CRITICAL REQUIREMENTS:
1. Use ONLY the exact category names listed above
2. Mark multiple classifications where applicable (except PRIME - only one)
3. For entities, list actual entity names found in the query
4. PRIME category must be one of the 114 official categories
5. Respond ONLY with valid JSON - no other text"""
    
    def classify_query(self, query: Query, guidelines: Dict[str, Any]) -> ClassificationResult:
        """Classify a single query"""
        
        # Get relevant guideline context (simple approach - use first few chunks)
        guidelines_context = "\n\n".join(guidelines["chunks"][:3])  # Use first 3 chunks
        
        # Build the prompt
        prompt = self.classification_prompt.format(
            query_text=query.text,
            guidelines_context=guidelines_context
        )
        
        # Call OpenAI API
        try:
            response = self.client.chat.completions.create(
                model=self.config.openai_model,
                messages=[
                    {"role": "system", "content": "You are an expert query classification analyst. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature
            )
            
            # Parse the response using the enhanced parser
            response_text = response.choices[0].message.content.strip()
            classification_data = self._parse_llm_response(response_text)
            
            # Ensure prime_category is a string (not a dict)
            if isinstance(classification_data.get("prime_category"), dict):
                prime_cat = classification_data["prime_category"]
                if "category" in prime_cat:
                    classification_data["prime_category"] = prime_cat["category"]
                else:
                    classification_data["prime_category"] = "OTHER_None_of_These"
            
            # Create the result
            result = ClassificationResult(
                query=query,
                annotation_schema=classification_data.get("annotation_schema", {}),
                entity_schema=classification_data.get("entity_schema", {}),
                intent_schema=classification_data.get("intent_schema", {}),
                topic_schema=classification_data.get("topic_schema", {}),
                prime_category=classification_data.get("prime_category", "OTHER_None_of_These"),
                research_notes=classification_data.get("research_notes", ""),
                confidence_score=classification_data.get("confidence_score", 0.5)
            )
            
            return result
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            # Return a default classification on error using the new format
            return ClassificationResult(
                query=query,
                annotation_schema={"ambiguous": False, "misspelled_malformed": False, "non_market_language": False},
                entity_schema={},
                intent_schema={"research": True, "other_intent": False},
                topic_schema={"other_topic": True},
                prime_category="OTHER_None_of_These",
                research_notes=f"Classification failed due to API error: {e}",
                confidence_score=0.0
            )
    
    def _get_default_classification(self) -> Dict[str, Any]:
        """Get a default classification when parsing fails - UPDATED FORMAT"""
        return {
            "annotation_schema": {
                "ambiguous": False,
                "misspelled_malformed": False,
                "non_market_language": False
            },
            "entity_schema": {
                "person_notable": [],
                "person_non_notable": [],
                "type_of_person": [],
                "specific_organization": [],
                "type_of_organization": [],
                "media_title": [],
                "type_of_media": [],
                "specific_product": [],
                "type_of_product": [],
                "specific_place_city": [],
                "specific_place_poi": [],
                "specific_place_address": [],
                "specific_place_other": [],
                "type_of_place": [],
                "specific_event": [],
                "type_of_event": [],
                "website": [],
                "other_entity": []
            },
            "intent_schema": {
                "website": False,
                "porn_illegal": False,
                "images_videos": False,
                "local_info": False,
                "event_info": False,
                "news": False,
                "shopping": False,
                "simple_fact": False,
                "research": True,  # Default to True since it's a research intent
                "other_intent": False
            },
            "topic_schema": {
                "autos": False,
                "education": False,
                "entertainment_books": False,
                "entertainment_games": False,
                "entertainment_movies": False,
                "entertainment_music": False,
                "entertainment_tv": False,
                "entertainment_other": False,
                "environment": False,
                "finance": False,
                "food_dining": False,
                "government_politics": False,
                "health_medical": False,
                "home_garden": False,
                "jobs": False,
                "legal": False,
                "people_search": False,
                "personal_goods": False,
                "pets_animals": False,
                "real_estate": False,
                "religion": False,
                "retailers": False,
                "social_networking": False,
                "sports_outdoors": False,
                "tech_electronics": False,
                "transit_traffic": False,
                "travel_lodging": False,
                "weather": False,
                "other_topic": True  # Default to True
            },
            "prime_category": "OTHER_None_of_These",  # String, not dict!
            "research_notes": "Failed to parse classification response - using default",
            "confidence_score": 0.0
        }

    def _parse_llm_response(self, response_content: str) -> Dict[str, Any]:
        """
        Parse LLM response content and handle various response formats
        """
        try:
            # First, try to parse the entire response as JSON
            return json.loads(response_content)
        except json.JSONDecodeError:
            pass
        
        # If that fails, try to extract JSON from the response
        try:
            # Look for JSON block in the response
            json_match = re.search(r'\{.*\}', response_content, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass
        
        # If still no luck, try to find JSON between ```json and ``` markers
        try:
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', response_content, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass
        
        # If all parsing fails, log the issue and return default
        logger.warning(f"Failed to parse LLM response: {response_content[:200]}...")
        return self._get_default_classification()
