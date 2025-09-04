#!/usr/bin/env python3
"""
Enhanced CSV converter that outputs proper classification schemas
and generates PRIME category reports matching the required format.
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime
import sys
from collections import Counter

# Import the PRIME categories mapping
PRIME_CATEGORIES = {
    # ANSWERS Categories (21 total)
    "ANSWERS_General": "Answers", "ANSWERS_Autos": "Answers", "ANSWERS_Dreams": "Answers",
    "ANSWERS_Education": "Answers", "ANSWERS_Finance": "Answers", "ANSWERS_Food": "Answers",
    "ANSWERS_Games": "Answers", "ANSWERS_Gardening": "Answers", "ANSWERS_Health": "Answers",
    "ANSWERS_Jobs": "Answers", "ANSWERS_Legal": "Answers", "ANSWERS_Music": "Answers",
    "ANSWERS_Parenting": "Answers", "ANSWERS_Relationships": "Answers", "ANSWERS_Religion": "Answers",
    "ANSWERS_Science_Math": "Answers", "ANSWERS_Sports": "Answers", "ANSWERS_Tech": "Answers",
    "ANSWERS_Travel": "Answers", "ANSWERS_Weddings": "Answers", "ANSWERS_Other": "Answers",
    
    # QUICKFACT Categories (16 total)
    "QUICKFACT_Astronomical_Event": "Quickfacts: Define, Crossword,", "QUICKFACT_Calories": "Quickfacts: Define, Crossword,",
    "QUICKFACT_Conversion": "Quickfacts: Define, Crossword,", "QUICKFACT_Crossword": "Quickfacts: Define, Crossword,",
    "QUICKFACT_Define": "Quickfacts: Define, Crossword,", "QUICKFACT_Directions": "Quickfacts: Define, Crossword,",
    "QUICKFACT_Flight_Tracker": "Quickfacts: Define, Crossword,", "QUICKFACT_Holiday": "Quickfacts: Define, Crossword,",
    "QUICKFACT_Phone_Codes": "Quickfacts: Define, Crossword,", "QUICKFACT_Phone_Number": "Quickfacts: Define, Crossword,",
    "QUICKFACT_Sunrise_Sunset": "Quickfacts: Define, Crossword,", "QUICKFACT_Table": "Quickfacts: Define, Crossword,",
    "QUICKFACT_Time": "Quickfacts: Define, Crossword,", "QUICKFACT_Traffic": "Quickfacts: Define, Crossword,",
    "QUICKFACT_Translate": "Quickfacts: Define, Crossword,", "QUICKFACT_Zip_Code": "Quickfacts: Define, Crossword,",
    
    # Notable Person Categories (4 total)
    "Notable_Person_Actor": "Entertainment: Celebrities,", "Notable_Person_Athlete": "Sports teams, leagues, athletes",
    "Notable_Person_Musician": "Entertainment: Celebrities,", "Notable_Person_Other": "Entertainment: Celebrities,",
    
    # Other specific categories
    "Shopping": "Product", "Local_Category": "Local", "Local_Chain": "Local", "Local_Single": "Local",
    "News": "News (undercounted)", "Place": "Place and Venue", "Weather": "Weather",
    "Movie_Current": "Entertainment: Movies", "Movie_Non_current": "Entertainment: Movies",
    "TV_Show": "Entertainment: TV", "Sports_Team": "Sports teams, leagues, athletes",
    
    # OTHER Categories (12 total)
    "OTHER_Academic": "Other categories", "OTHER_Adult": "Other: Adult and Web results",
    "OTHER_Airport": "Other categories", "OTHER_App": "Other categories", "OTHER_Events": "Other categories",
    "OTHER_Jobs": "Jobs and Real Estate", "OTHER_Music": "Entertainment: Music", "OTHER_Person_Search": "Other categories",
    "OTHER_Real_Estate": "Jobs and Real Estate", "OTHER_Web": "Other: Adult and Web results",
    "OTHER_Wiki": "Other categories", "OTHER_None_of_These": "Other categories",
    
    # Additional Prime Categories from the data
    "Navigational": "Navigational", "Entertainment_Celebrities": "Entertainment: Celebrities,",
    "Image_only": "Image only", "Jobs_and_Real_Estate": "Jobs and Real Estate",
    "Cannot_judge": "Cannot judge", "Celeb_other": "Celeb: other",
    "Reference_Health_Lottery": "Reference: Health, Lottery,", "Product": "Product",
    "Place_and_Venue": "Place and Venue", "Other_categories": "Other categories",
    "News_undercounted": "News (undercounted)", "Sports_teams_leagues_athletes": "Sports teams, leagues, athletes",
    "Autos": "Autos", "Other_Adult_and_Web_results": "Other: Adult and Web results"
}

def load_json_results(json_file_path):
    """Load results from JSON file"""
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def create_detailed_classification_csv(results_data, output_file):
    """Create detailed CSV with all classification schemas"""
    
    results = results_data.get('results', [])
    rows = []
    
    for result in results:
        query = result['query']
        annotation = result.get('annotation_schema', {})
        entity = result.get('entity_schema', {})
        intent = result.get('intent_schema', {})
        topic = result.get('topic_schema', {})
        prime = result.get('prime_category', {})
        
        # Create base row
        row = {
            'query_text': query['text'],
            'query_index': query['index'],
            'query_word_count': query['word_count'],
        }
        
        # Annotation Schema (3 classifications)
        row.update({
            'annotation_ambiguous': annotation.get('ambiguous', False),
            'annotation_misspelled_malformed': annotation.get('misspelled_malformed', False),
            'annotation_non_market_language': annotation.get('non_market_language', False),
        })
        
        # Entity Schema (18 classifications) - convert lists to comma-separated strings
        entity_fields = [
            'person_notable', 'person_non_notable', 'type_of_person', 'specific_organization',
            'type_of_organization', 'media_title', 'type_of_media', 'specific_product',
            'type_of_product', 'specific_place_city', 'specific_place_poi', 'specific_place_address',
            'specific_place_other', 'type_of_place', 'specific_event', 'type_of_event',
            'website', 'other_entity'
        ]
        
        for field in entity_fields:
            entities = entity.get(field, [])
            if isinstance(entities, list):
                row[f'entity_{field}'] = ', '.join([str(e) for e in entities]) if entities else ''
            else:
                row[f'entity_{field}'] = str(entities) if entities else ''
        
        # Intent Schema (10 classifications)
        intent_fields = [
            'website', 'porn_illegal', 'images_videos', 'local_info', 'event_info',
            'news', 'shopping', 'simple_fact', 'research', 'other_intent'
        ]
        
        for field in intent_fields:
            row[f'intent_{field}'] = intent.get(field, False)
        
        # Topic Schema (29 classifications)
        topic_fields = [
            'autos', 'education', 'entertainment_books', 'entertainment_games', 'entertainment_movies',
            'entertainment_music', 'entertainment_tv', 'entertainment_other', 'environment', 'finance',
            'food_dining', 'government_politics', 'health_medical', 'home_garden', 'jobs', 'legal',
            'people_search', 'personal_goods', 'pets_animals', 'real_estate', 'religion', 'retailers',
            'social_networking', 'sports_outdoors', 'tech_electronics', 'transit_traffic',
            'travel_lodging', 'weather', 'other_topic'
        ]
        
        for field in topic_fields:
            row[f'topic_{field}'] = topic.get(field, False)
        
        # PRIME Category (MECE - exactly one)
        if isinstance(prime, dict):
            row['prime_category'] = prime.get('category', '') or prime.get('prime_category', '')
        else:
            row['prime_category'] = str(prime) if prime else ''
        
        # Meta category for aggregation
        row['meta_category'] = PRIME_CATEGORIES.get(row['prime_category'], 'Other categories')
        
        # Additional fields
        row.update({
            'research_notes': result.get('research_notes', ''),
            'confidence_score': result.get('confidence_score', 0.0),
            'processing_time_seconds': result.get('processing_time', 0.0),
            'timestamp': result.get('timestamp', ''),
        })
        
        rows.append(row)
    
    # Create DataFrame and save
    df = pd.DataFrame(rows)
    df.to_csv(output_file, index=False)
    print(f"✅ Detailed classification CSV saved: {output_file}")
    print(f"   Columns: {len(df.columns)}, Rows: {len(df)}")
    
    return df

def create_prime_report(results_data, output_file):
    """Create PRIME category report matching Prime_report.csv format"""
    
    results = results_data.get('results', [])
    total_queries = len(results)
    
    # Count PRIME categories
    prime_counts = Counter()
    
    for result in results:
        prime = result.get('prime_category', {})
        if isinstance(prime, dict):
            category = prime.get('category', '') or prime.get('prime_category', '')
        else:
            category = str(prime) if prime else 'OTHER_None_of_These'
        
        if category:
            prime_counts[category] += 1
        else:
            prime_counts['OTHER_None_of_These'] += 1
    
    # Create report rows
    report_rows = []
    
    for prime_category, count in prime_counts.items():
        meta_category = PRIME_CATEGORIES.get(prime_category, 'Other categories')
        percentage = (count / total_queries) * 100 if total_queries > 0 else 0
        
        report_rows.append({
            'Meta (for aggregations and piechart)': meta_category,
            'PRIME (known as OYE in previous projects)': prime_category,
            'Query Count': count,
            'Percentage of Total': f"{percentage:.1f}%"
        })
    
    # Sort by count (descending)
    report_rows.sort(key=lambda x: x['Query Count'], reverse=True)
    
    # Create DataFrame and save
    df = pd.DataFrame(report_rows)
    df.to_csv(output_file, index=False)
    
    print(f"✅ PRIME category report saved: {output_file}")
    print(f"   Categories: {len(df)}, Total queries: {total_queries}")
    
    return df

def create_meta_aggregation_report(results_data, output_file):
    """Create meta category aggregation report"""
    
    results = results_data.get('results', [])
    total_queries = len(results)
    
    # Count by meta categories
    meta_counts = Counter()
    
    for result in results:
        prime = result.get('prime_category', {})
        if isinstance(prime, dict):
            category = prime.get('category', '') or prime.get('prime_category', '')
        else:
            category = str(prime) if prime else 'OTHER_None_of_These'
        
        meta_category = PRIME_CATEGORIES.get(category, 'Other categories')
        meta_counts[meta_category] += 1
    
    # Create report rows
    report_rows = []
    
    for meta_category, count in meta_counts.items():
        percentage = (count / total_queries) * 100 if total_queries > 0 else 0
        
        # Create definition based on meta category
        if "Answer" in meta_category:
            definition = "Show opinions, advice, recommendations from others"
        elif "Quickfact" in meta_category:
            definition = "Show quick factual answers and definitions" 
        elif "Entertainment" in meta_category:
            definition = "Entertainment content including celebrities, movies, music"
        elif meta_category == "Local":
            definition = "Local business listings with maps and contact information"
        elif meta_category == "Navigational":
            definition = "Website navigation and direct access queries"
        elif meta_category == "Product":
            definition = "Product information, prices, sellers, reviews"
        else:
            definition = f"Queries related to {meta_category.lower()}"
        
        report_rows.append({
            'category - groups include "Answers" equivalents': meta_category,
            'query volume for meta group': f"{count} ({percentage:.1f}%)",
            'definition of meta group': definition
        })
    
    # Sort by count (descending)
    report_rows.sort(key=lambda x: int(x['query volume for meta group'].split('(')[0].split()[0]), reverse=True)
    
    # Create DataFrame and save
    df = pd.DataFrame(report_rows)
    df.to_csv(output_file, index=False)
    
    print(f"✅ Meta aggregation report saved: {output_file}")
    print(f"   Meta categories: {len(df)}, Total queries: {total_queries}")
    
    return df

def print_classification_summary(results_data):
    """Print summary statistics of classifications"""
    
    results = results_data.get('results', [])
    total_queries = len(results)
    
    print(f"\n📊 Classification Summary:")
    print("=" * 50)
    print(f"Total queries classified: {total_queries}")
    
    # Count annotation issues
    annotation_counts = Counter()
    for result in results:
        annotation = result.get('annotation_schema', {})
        for key, value in annotation.items():
            if value:
                annotation_counts[key] += 1
    
    print(f"\nAnnotation Issues:")
    for issue, count in annotation_counts.items():
        print(f"  {issue}: {count} ({count/total_queries*100:.1f}%)")
    
    # Count top entities
    entity_counts = Counter()
    for result in results:
        entity = result.get('entity_schema', {})
        for key, value in entity.items():
            if value and (isinstance(value, list) and len(value) > 0):
                entity_counts[key] += 1
    
    print(f"\nTop Entity Types:")
    for entity_type, count in entity_counts.most_common(5):
        print(f"  {entity_type}: {count} queries")
    
    # Count intents
    intent_counts = Counter()
    for result in results:
        intent = result.get('intent_schema', {})
        for key, value in intent.items():
            if value:
                intent_counts[key] += 1
    
    print(f"\nTop Intents:")
    for intent, count in intent_counts.most_common(5):
        print(f"  {intent}: {count} queries")
    
    # Count topics
    topic_counts = Counter()
    for result in results:
        topic = result.get('topic_schema', {})
        for key, value in topic.items():
            if value:
                topic_counts[key] += 1
    
    print(f"\nTop Topics:")
    for topic, count in topic_counts.most_common(5):
        print(f"  {topic}: {count} queries")

def main():
    """Main function to convert JSON to multiple CSV formats"""
    
    # Default input and output paths
    input_file = Path("data/output/results.json")
    output_dir = Path("data/output")
    
    # Check if custom input file is provided
    if len(sys.argv) > 1:
        input_file = Path(sys.argv[1])
    
    print(f"🔄 Converting {input_file} to enhanced CSV formats...")
    
    try:
        # Load JSON results
        results_data = load_json_results(input_file)
        total_results = results_data.get('metadata', {}).get('total_results', 0)
        print(f"✅ Loaded {total_results} results")
        
        # Create detailed classification CSV
        detailed_csv = output_dir / "detailed_classifications.csv"
        detailed_df = create_detailed_classification_csv(results_data, detailed_csv)
        
        # Create PRIME category report
        prime_report_csv = output_dir / "prime_category_report.csv"
        prime_df = create_prime_report(results_data, prime_report_csv)
        
        # Create meta aggregation report
        meta_report_csv = output_dir / "meta_aggregation_report.csv"
        meta_df = create_meta_aggregation_report(results_data, meta_report_csv)
        
        # Print summary
        print_classification_summary(results_data)
        
        print(f"\n✅ All reports generated successfully!")
        print(f"📁 Files created:")
        print(f"   • {detailed_csv}")
        print(f"   • {prime_report_csv}")
        print(f"   • {meta_report_csv}")
        
    except FileNotFoundError:
        print(f"❌ Error: Could not find {input_file}")
        print("Make sure you have run the classification first with: make run")
    except Exception as e:
        print(f"❌ Error converting to CSV: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
