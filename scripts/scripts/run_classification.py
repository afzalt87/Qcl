#!/usr/bin/env python3
"""
Script for running QCL query classification locally.
"""

import sys
import os
from pathlib import Path
import time
from pathlib import Path
from typing import List
import argparse
import logging

# Add src directory to Python path
script_dir = Path(__file__).parent.absolute()
src_dir = script_dir.parent / "src"
sys.path.insert(0, str(src_dir))

from qcl.classification.classifier import QueryClassifier
from qcl.core.config import Config
from qcl.data.loaders import load_queries_from_csv, save_results, load_guidelines_from_pdf
from qcl.data.models import Query
from qcl.core.config import get_config, setup_logging
from qcl.data.models import ClassificationResult



def main():
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging()
    logger.info("Starting QCL Query Classification")
    
    # Get configuration
    config = get_config()
    
    # Validate configuration
    if not config.validate():
        sys.exit(1)
    
    try:
        if args.command == "classify":
            run_classification(args, config, logger)
        elif args.command == "validate":
            validate_data(args, config, logger)
        else:
            parser.print_help()
            
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: {e}")
        if config.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def create_parser():
    """Create argument parser"""
    parser = argparse.ArgumentParser(description="QCL Query Classification System")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Classification command
    classify_parser = subparsers.add_parser("classify", help="Run query classification")
    classify_parser.add_argument("--queries", type=Path, required=True, help="Path to queries CSV file")
    classify_parser.add_argument("--guidelines", type=Path, required=True, help="Path to guidelines PDF file")
    classify_parser.add_argument("--output", type=Path, required=True, help="Path to output JSON file")
    classify_parser.add_argument("--max-queries", type=int, help="Maximum number of queries to process")
    classify_parser.add_argument("--batch-size", type=int, help="Batch size for processing")
    
    # Validation command
    validate_parser = subparsers.add_parser("validate", help="Validate input data")
    validate_parser.add_argument("--queries", type=Path, required=True, help="Path to queries CSV file")
    validate_parser.add_argument("--guidelines", type=Path, help="Path to guidelines PDF file")
    
    return parser


def run_classification(args, config, logger):
    """Run the classification pipeline"""
    
    # Override config with command line args
    if args.max_queries:
        config.max_queries = args.max_queries
    if args.batch_size:
        config.batch_size = args.batch_size
    
    logger.info(f"Loading queries from {args.queries}")
    queries = load_queries_from_csv(args.queries)
    
    # Limit queries if specified
    if config.max_queries:
        queries = queries[:config.max_queries]
        logger.info(f"Limited to {len(queries)} queries for processing")
    
    logger.info(f"Loading guidelines from {args.guidelines}")
    guidelines = load_guidelines_from_pdf(args.guidelines, config.chunk_size, config.chunk_overlap)
    
    # Initialize classifier
    logger.info("Initializing classifier")
    classifier = QueryClassifier(config)
    
    # Process queries
    logger.info(f"Starting classification of {len(queries)} queries")
    results = []
    
    start_time = time.time()
    
    for i, query in enumerate(queries):
        logger.info(f"Processing query {i+1}/{len(queries)}: '{query.text}'")
        
        try:
            query_start = time.time()
            
            # Classify the query
            result = classifier.classify_query(query, guidelines)
            result.processing_time = time.time() - query_start
            
            results.append(result)
            
            logger.info(f"✓ Classified as: {result.prime_category.get('category', 'Unknown')} "
                       f"(confidence: {result.confidence_score:.2f}, time: {result.processing_time:.2f}s)")
            
            # Add delay to respect rate limits
            time.sleep(60 / config.requests_per_minute)
            
        except Exception as e:
            logger.error(f"✗ Failed to classify query '{query.text}': {e}")
            continue
    
    total_time = time.time() - start_time
    
    # Save results
    logger.info(f"Saving results to {args.output}")
    save_results(results, args.output)
    
    # Print summary
    logger.info("=" * 50)
    logger.info("CLASSIFICATION SUMMARY")
    logger.info("=" * 50)
    logger.info(f"Total queries processed: {len(results)}")
    logger.info(f"Total time: {total_time:.2f} seconds")
    logger.info(f"Average time per query: {total_time/len(results):.2f} seconds")
    logger.info(f"Success rate: {len(results)/len(queries)*100:.1f}%")
    logger.info(f"Results saved to: {args.output}")


def validate_data(args, config, logger):
    """Validate input data"""
    
    logger.info("Validating input data")
    
    # Validate queries
    try:
        queries = load_queries_from_csv(args.queries)
        logger.info(f"✓ Queries file valid: {len(queries)} queries loaded")
        
        # Basic stats
        avg_length = sum(len(q.text) for q in queries) / len(queries)
        avg_words = sum(q.word_count for q in queries) / len(queries)
        
        logger.info(f"  Average query length: {avg_length:.1f} characters")
        logger.info(f"  Average word count: {avg_words:.1f} words")
        
        # Check for duplicates
        unique_queries = set(q.text.lower() for q in queries)
        duplicates = len(queries) - len(unique_queries)
        if duplicates > 0:
            logger.warning(f"  Found {duplicates} duplicate queries")
        
    except Exception as e:
        logger.error(f"✗ Queries file invalid: {e}")
        return False
    
    # Validate guidelines if provided
    if args.guidelines:
        try:
            guidelines = load_guidelines_from_pdf(args.guidelines)
            logger.info(f"✓ Guidelines file valid: {guidelines['chunk_count']} chunks created")
            logger.info(f"  Total text length: {guidelines['total_text_length']} characters")
        except Exception as e:
            logger.error(f"✗ Guidelines file invalid: {e}")
            return False
    
    logger.info("✓ All validation checks passed")
    return True


if __name__ == "__main__":
    main()