import json
import pandas as pd

# Load JSON results
with open('data/output/results.json', 'r') as f:
    data = json.load(f)

# Convert to simple DataFrame
rows = []
for result in data['results']:
    # Get active intents and topics
    intents = [k for k, v in result['intent_schema'].items() if v]
    topics = [k for k, v in result['topic_schema'].items() if v]
    
    row = {
        'query_text': result['query']['text'],
        'query_word_count': result['query']['word_count'],
        'prime_category': result['prime_category']['category'],
        'prime_subclass': result['prime_category'].get('subclass', ''),
        'confidence_score': result['confidence_score'],
        'processing_time_seconds': round(result['processing_time'], 2),
        'primary_intents': ', '.join(intents),
        'primary_topics': ', '.join(topics),
        'research_notes': result['research_notes']
    }
    rows.append(row)

df = pd.DataFrame(rows)
df.to_csv('data/output/results.csv', index=False)

print(f'✅ CSV saved to data/output/results.csv')
print(f'📊 {len(df)} rows, {len(df.columns)} columns')
print('\nPreview:')
print(df[['query_text', 'prime_category', 'confidence_score']].head().to_string(index=False))