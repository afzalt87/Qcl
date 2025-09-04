"""Simple data models for QCL"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime
import re

@dataclass
class Query:
    """Represents a search query"""
    text: str
    index: int = 0
    
    @property
    def slug(self) -> str:
        """URL-safe version of the query"""
        slug = re.sub(r'[^\w\s-]', '', self.text.lower())
        return re.sub(r'[-\s]+', '_', slug).strip('_')
    
    @property
    def word_count(self) -> int:
        """Number of words in the query"""
        return len(self.text.split())

@dataclass
class ClassificationResult:
    """Classification result for a query"""
    query: Query
    annotation_schema: Dict[str, Any]
    entity_schema: Dict[str, Any]
    intent_schema: Dict[str, Any]
    topic_schema: Dict[str, Any]
    prime_category: Dict[str, Any]
    research_notes: str = ""
    confidence_score: float = 1.0
    processing_time: float = 0.0
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "query": {
                "text": self.query.text,
                "index": self.query.index,
                "slug": self.query.slug,
                "word_count": self.query.word_count
            },
            "annotation_schema": self.annotation_schema,
            "entity_schema": self.entity_schema,
            "intent_schema": self.intent_schema,
            "topic_schema": self.topic_schema,
            "prime_category": self.prime_category,
            "research_notes": self.research_notes,
            "confidence_score": self.confidence_score,
            "processing_time": self.processing_time,
            "timestamp": self.timestamp.isoformat()
        }