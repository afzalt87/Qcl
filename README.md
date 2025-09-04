# QCL - Query Classification System

A mobile query intent classification system that processes search queries using GPT-4.1 and provides comprehensive multi-schema categorization for search result optimization.

![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)
![Local Development](https://img.shields.io/badge/deployment-local-green.svg)

## 🎯 What It Does

QCL classifies search queries across five comprehensive schemas:

1. **Annotation Schema** - Language, spelling, and ambiguity detection
2. **Entity Schema** - People, places, products, organizations identification  
3. **Intent Schema** - User intentions (shopping, research, local info, etc.)
4. **Topic Schema** - Subject matter domains (entertainment, tech, health, etc.)
5. **PRIME Category** - Single most important experience to prioritize

## ✨ Features

- 🧠 **GPT-4.1 Classification** - Leverages OpenAI's latest models for accurate categorization
- 📄 **PDF Guidelines Processing** - Automatically processes classification guidelines from PDF
- 🔄 **Batch Processing** - Handles multiple queries efficiently with rate limiting
- 📊 **Multiple Output Formats** - JSON and CSV export capabilities
- 🛠️ **Simple Setup** - Local development focused with easy commands
- ⚡ **Fast Processing** - ~3-5 seconds per query with high accuracy

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- OpenAI API key
- Git

### 1. Setup Project

```bash
# Clone or create project directory
mkdir qcl && cd qcl

# Set up structure and environment
make quick-start

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```

### 2. Install Dependencies

```bash
# Install required packages
make install
# or
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Create environment file
cp .env.example .env

# Edit .env with your OpenAI API key
nano .env  # or use your preferred editor
```

**Required in .env:**
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Add Your Data

```bash
# Place your files:
# - CSV with queries in data/input/queries/
# - PDF guidelines in data/input/guidelines/
# - Optional: SERP images in data/input/images/

# Or create sample data for testing:
make create-sample-data
```

### 5. Run Classification

```bash
# Test with sample data (5 queries)
make run-sample

# Convert results to CSV
make convert-csv

# View results
cat data/output/results.csv
```

## 📁 Project Structure

```
qcl/
├── src/qcl/                    # Main Python package
│   ├── core/
│   │   └── config.py           # Configuration management
│   ├── data/
│   │   ├── models.py           # Data classes and structures
│   │   └── loaders.py          # File loading utilities
│   ├── classification/
│   │   └── classifier.py       # GPT-4.1 classification engine
│   └── pipeline/
│       └── __init__.py         # Pipeline components
├── scripts/
│   ├── run_classification.py   # Main classification script
│   └── json_to_csv.py         # Results converter
├── data/
│   ├── input/
│   │   ├── queries/            # Your query CSV files
│   │   ├── guidelines/         # Classification guideline PDFs
│   │   └── images/             # SERP screenshots (optional)
│   ├── processed/              # Cached embeddings and data
│   └── output/                 # Classification results
├── configs/
│   ├── config.yaml            # Application settings
│   └── classification_prompt.txt # GPT-4.1 prompt template
├── logs/                      # Application logs
├── requirements.txt           # Python dependencies
├── Makefile                   # Development commands
├── .env                       # Environment variables
└── README.md                  # This file
```

## 🔧 Usage

### Command Line Interface

**Basic Classification:**
```bash
# Classify queries from CSV
python scripts/run_classification.py classify \
  --queries data/input/queries/your_queries.csv \
  --guidelines data/input/guidelines/guidelines.pdf \
  --output data/output/results.json

# Limit number of queries for testing
python scripts/run_classification.py classify \
  --queries data/input/queries/your_queries.csv \
  --guidelines data/input/guidelines/guidelines.pdf \
  --output data/output/results.json \
  --max-queries 10
```

**Data Validation:**
```bash
# Validate your input files
python scripts/run_classification.py validate \
  --queries data/input/queries/your_queries.csv \
  --guidelines data/input/guidelines/guidelines.pdf
```

### Makefile Commands (Recommended)

```bash
# Show all available commands
make help

# Quick test with sample data
make run-sample

# Run full classification
make run

# Convert JSON results to CSV
make convert-csv

# Check project status
make status

# View recent logs
make logs

# Clean up temporary files
make clean
```

## 📊 Input Data Format

### Query CSV File
Your CSV file should have a `query` column:

```csv
query
best restaurants near me
weather today
how to cook pasta
iphone 15 price
taylor swift
```

### Guidelines PDF
- Place your classification guidelines PDF in `data/input/guidelines/`
- The system will automatically chunk and process the text
- Supports multi-page documents

## 📈 Output Formats

### JSON Output
Detailed classification with all schemas:
```json
{
  "query": {
    "text": "best restaurants near me",
    "word_count": 4
  },
  "annotation_schema": {
    "non_market_language": false,
    "misspelled_malformed": false,
    "ambiguous": false
  },
  "entity_schema": {
    "other_entity": [{"entity": "restaurants", "type": "business"}]
  },
  "intent_schema": {
    "local_info": true
  },
  "topic_schema": {
    "food_dining": true
  },
  "prime_category": {
    "category": "local_info",
    "confidence": 0.98
  }
}
```

### CSV Output
Simplified tabular format for analysis:
```csv
query_text,prime_category,confidence_score,processing_time,primary_intents,primary_topics
"best restaurants near me",local_info,0.98,5.31,"local_info","food_dining"
"weather today",weather,0.99,10.09,"simple_fact, news","weather"
```

## ⚙️ Configuration

### Environment Variables (.env)
```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional
QCL_ENV=development
QCL_DEBUG=true
BATCH_SIZE=10
REQUESTS_PER_MINUTE=50
```

### Config File (configs/config.yaml)
```yaml
# Processing settings
processing:
  batch_size: 10
  chunk_size: 1000
  chunk_overlap: 200

# Rate limiting
rate_limit:
  requests_per_minute: 50
  concurrent_requests: 5

# OpenAI settings
openai:
  model: "gpt-4.1" #Multimodal model
  temperature: 0.1
```

## 📊 Classification Schemas

### Annotation Schema
Identifies language and quality issues:
- `non_market_language` - Non-English queries
- `misspelled_malformed` - Spelling/grammar errors
- `ambiguous` - Multiple possible meanings
- `cannot_classify` - Unable to categorize

### Entity Schema
Recognizes entities in queries:
- `person_notable` - Famous people
- `specific_organization` - Companies, brands
- `media_title` - Movies, books, songs
- `specific_product` - Product names/models
- `specific_place_city` - Geographic locations
- `website` - Web domains
- `other_entity` - Other entities

### Intent Schema
Determines user intentions:
- `website` - Navigate to specific site
- `images_videos` - Visual content search
- `local_info` - Local business information
- `shopping` - Product research/purchase
- `simple_fact` - Quick factual answer
- `research` - Detailed information
- `news` - Current events

### Topic Schema
Categorizes subject matter:
- `entertainment_*` - Movies, music, TV, books
- `tech_electronics` - Technology products
- `health_medical` - Health information
- `finance` - Financial services
- `education` - Learning resources
- `sports_outdoors` - Sports and recreation
- `travel_lodging` - Travel information
- `food_dining` - Restaurants and recipes
- `weather` - Weather information
- And more...

### PRIME Category
Single most important classification:
- `Notable Person` - Celebrity/famous person
- `Shopping` - Product information
- `Local` - Local business
- `Weather` - Weather conditions
- `News` - Breaking news
- `ANSWERS` - How-to/advice content
- `QUICKFACT` - Simple factual queries
- `OTHER` - Doesn't fit other categories

## 🎯 Example Results

| Query | Prime Category | Confidence | Processing Time | Intent | Topic |
|-------|---------------|------------|-----------------|--------|-------|
| best restaurants near me | local_info | 0.98 | 5.31s | local_info | food_dining |
| weather today | weather | 0.99 | 10.09s | simple_fact, news | weather |
| how to cook pasta | food_dining | 0.98 | 3.84s | research | food_dining |
| iphone 15 price | shopping | 0.98 | 4.39s | shopping | tech_electronics |
| taylor swift | entertainment_music | 0.98 | 4.43s | images_videos, research | entertainment_music |

**Average Confidence: 98.2%** ✨

## 🔍 Monitoring and Analysis

### View Processing Logs
```bash
# Recent log entries
make logs

# Full log file
tail -f logs/qcl.log
```

### Performance Metrics
- **Average processing time**: ~5 seconds per query
- **Typical confidence scores**: 0.95-0.99
- **Rate limit**: 50 requests per minute (configurable)
- **Success rate**: >99% with proper API key

### Analyzing Results
```python
import pandas as pd

# Load and analyze results
df = pd.read_csv('data/output/results.csv')

# Confidence distribution
print(df['confidence_score'].describe())

# Most common categories
print(df['prime_category'].value_counts())

# Processing time analysis
print(f"Average processing time: {df['processing_time'].mean():.2f}s")
```

## 🛠️ Development

### Adding New Queries
1. Add queries to your CSV file in `data/input/queries/`
2. Run classification: `make run`
3. Convert to CSV: `make convert-csv`

### Customizing Classification
1. Edit the prompt template in `configs/classification_prompt.txt`
2. Adjust settings in `configs/config.yaml`
3. Modify rate limits in `.env`

### Code Quality
```bash
# Format code (optional)
black src/ scripts/
isort src/ scripts/

# Basic validation
make validate
```

## 🐛 Troubleshooting

### Common Issues

**1. OpenAI API Key Error**
```bash
# Check your .env file
cat .env | grep OPENAI_API_KEY

# Test API connection
python -c "import openai; client = openai.OpenAI(); print('✅ API key works')"
```

**2. File Not Found Errors**
```bash
# Check your data files
ls -la data/input/queries/
ls -la data/input/guidelines/

# Create sample data if needed
make create-sample-data
```

**3. Import Errors**
```bash
# Make sure virtual environment is active
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**4. Rate Limit Errors**
- Reduce `REQUESTS_PER_MINUTE` in `.env`
- Increase delays in `configs/config.yaml`
- Check your OpenAI usage limits

### Getting Help

```bash
# Check project status
make status

# Show available commands
make help

# Validate setup
make validate
```

### Performance Optimization

**For faster processing:**
- Increase `REQUESTS_PER_MINUTE` (if your OpenAI plan allows)
- Use smaller batch sizes for memory efficiency
- Enable caching for repeated guideline processing

**For better accuracy:**
- Lower the `temperature` setting in config
- Provide more detailed guidelines
- Use more specific prompts for your domain

## 📈 Scaling Up

### Processing Large Datasets
```bash
# Process in smaller batches
python scripts/run_classification.py classify \
  --queries large_dataset.csv \
  --guidelines guidelines.pdf \
  --output results.json \
  --batch-size 25

# Monitor progress
tail -f logs/qcl.log
```

### Custom Domains
1. Update the classification prompt for your specific domain
2. Add domain-specific entities and topics
3. Adjust confidence thresholds based on your needs

### Making Changes
1. Test with sample data first: `make run-sample`
2. Validate your changes: `make validate`
3. Run full processing: `make run`
4. Review results: `make convert-csv`

### Adding Features
- New classification schemas: Modify `src/qcl/data/models.py`
- Custom processing: Extend `src/qcl/classification/classifier.py`
- Additional outputs: Update `scripts/json_to_csv.py`
