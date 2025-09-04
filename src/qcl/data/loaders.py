"""Simple data loading functions"""

import pandas as pd
from pypdf import PdfReader
import pickle
from pathlib import Path
from typing import List, Dict, Any
import logging
import time
import datetime
from datetime import datetime

logger = logging.getLogger(__name__)

def load_queries_from_csv(file_path: Path) -> List['Query']:
    """Load queries from CSV file"""
    from .models import Query
    
    if not file_path.exists():
        raise FileNotFoundError(f"Query file not found: {file_path}")
    
    logger.info(f"Loading queries from {file_path}")
    
    # Read CSV
    df = pd.read_csv(file_path)
    
    # Validate
    if 'query' not in df.columns:
        raise ValueError("CSV must contain a 'query' column")
    
    # Clean data
    df = df.dropna(subset=['query'])
    df['query'] = df['query'].str.strip()
    df = df[df['query'].str.len() > 0]
    
    # Create Query objects
    queries = []
    for idx, row in df.iterrows():
        query = Query(text=row['query'], index=idx)
        queries.append(query)
    
    logger.info(f"Loaded {len(queries)} queries")
    return queries

def load_guidelines_from_pdf(file_path: Path, chunk_size: int = 800, chunk_overlap: int = 400) -> Dict[str, Any]:
    """Load and chunk guidelines from PDF"""
    if not file_path.exists():
        raise FileNotFoundError(f"Guidelines file not found: {file_path}")
    
    logger.info(f"Loading guidelines from {file_path}")
    
    # Extract text from PDF using pypdf
    text_parts = []
    try:
        reader = PdfReader(file_path)
        for page_num, page in enumerate(reader.pages):
            try:
                page_text = page.extract_text()
                if page_text and page_text.strip():
                    text_parts.append(page_text)
            except Exception as e:
                logger.warning(f"Could not extract text from page {page_num}: {e}")
    except Exception as e:
        logger.error(f"Error reading PDF file '{file_path}': {e}")
        raise e
    
    full_text = "\n\n".join(text_parts)
    
    # Simple text chunking
    chunks = []
    words = full_text.split()
    for i in range(0, len(words), chunk_size - chunk_overlap):
        chunk_words = words[i:i + chunk_size]
        chunk_text = " ".join(chunk_words)
        chunks.append(chunk_text)
    
    logger.info(f"Created {len(chunks)} text chunks")
    
    return {
        "source_file": str(file_path),
        "total_text_length": len(full_text),
        "chunk_count": len(chunks),
        "chunks": chunks,
        "full_text": full_text
    }

def save_results(results: List['ClassificationResult'], output_file: Path):
    """Save classification results to JSON file"""
    import json
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert to serializable format
    results_data = {
        "metadata": {
            "total_results": len(results),
            "created_at": datetime.now().isoformat(),
        },
        "results": [result.to_dict() for result in results]
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results_data, f, indent=2, default=str)
    
    logger.info(f"Results saved to {output_file}")

def load_cached_embeddings(cache_file: Path) -> Dict[str, Any]:
    """Load cached embeddings if they exist"""
    if cache_file.exists():
        logger.info(f"Loading cached embeddings from {cache_file}")
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    return None

def save_cached_embeddings(data: Dict[str, Any], cache_file: Path):
    """Save embeddings to cache"""
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    with open(cache_file, 'wb') as f:
        pickle.dump(data, f)
    logger.info(f"Embeddings cached to {cache_file}")