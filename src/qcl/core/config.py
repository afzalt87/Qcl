"""Configuration management for QCL"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class Config:
    """Simple configuration class"""
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4.1"
    max_tokens: int = 4000
    temperature: float = 0.1
    
    # Processing
    batch_size: int = 10
    max_queries: Optional[int] = None
    chunk_size: int = 800
    chunk_overlap: int = 400

    # Rate limiting
    requests_per_minute: int = 50
    concurrent_requests: int = 5
    retry_attempts: int = 3
    
    # Paths
    data_dir: Path = Path("data")
    queries_dir: Path = Path("data/input/queries")
    guidelines_dir: Path = Path("data/input/guidelines")
    images_dir: Path = Path("data/input/images")
    output_dir: Path = Path("data/output")
    processed_dir: Path = Path("data/processed")
    logs_dir: Path = Path("logs")
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    def __post_init__(self):
        """Create directories and load config"""
        self._create_directories()
        self._load_from_env()
        self._load_from_file()
    
    def _create_directories(self):
        """Create necessary directories"""
        for path in [self.data_dir, self.queries_dir, self.guidelines_dir, 
                    self.images_dir, self.output_dir, self.processed_dir, self.logs_dir]:
            path.mkdir(parents=True, exist_ok=True)
    
    def _load_from_env(self):
        """Load settings from environment variables"""
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.environment = os.getenv("QCL_ENV", "development")
        self.debug = os.getenv("QCL_DEBUG", "true").lower() == "true"
        
        if os.getenv("BATCH_SIZE"):
            self.batch_size = int(os.getenv("BATCH_SIZE"))
        if os.getenv("MAX_QUERIES"):
            self.max_queries = int(os.getenv("MAX_QUERIES"))
        if os.getenv("REQUESTS_PER_MINUTE"):
            self.requests_per_minute = int(os.getenv("REQUESTS_PER_MINUTE"))
    
    def _load_from_file(self):
        """Load settings from YAML config file"""
        config_file = Path("configs/config.yaml")
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config_data = yaml.safe_load(f)
                
                # Update settings from file
                if 'openai' in config_data:
                    openai_config = config_data['openai']
                    self.openai_model = openai_config.get('model', self.openai_model)
                    self.max_tokens = openai_config.get('max_tokens', self.max_tokens)
                    self.temperature = openai_config.get('temperature', self.temperature)
                
                if 'processing' in config_data:
                    proc_config = config_data['processing']
                    self.batch_size = proc_config.get('batch_size', self.batch_size)
                    self.max_queries = proc_config.get('max_queries', self.max_queries)
                    self.chunk_size = proc_config.get('chunk_size', self.chunk_size)
                    self.chunk_overlap = proc_config.get('chunk_overlap', self.chunk_overlap)
                
                if 'rate_limit' in config_data:
                    rate_config = config_data['rate_limit']
                    self.requests_per_minute = rate_config.get('requests_per_minute', self.requests_per_minute)
                    self.concurrent_requests = rate_config.get('concurrent_requests', self.concurrent_requests)
                    self.retry_attempts = rate_config.get('retry_attempts', self.retry_attempts)
                
            except Exception as e:
                print(f"Warning: Could not load config file: {e}")
    
    def validate(self) -> bool:
        """Validate configuration"""
        if not self.openai_api_key or self.openai_api_key == "your_openai_api_key_here":
            print("Error: OpenAI API key not set. Please set OPENAI_API_KEY in .env file")
            return False
        
        if not self.data_dir.exists():
            print(f"Error: Data directory {self.data_dir} does not exist")
            return False
        
        return True

# Global config instance
_config = None

def get_config() -> Config:
    """Get the global configuration instance"""
    global _config
    if _config is None:
        _config = Config()
    return _config

def setup_logging():
    """Setup basic logging"""
    import logging
    
    config = get_config()
    
    # Create logs directory
    config.logs_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, config.log_level),
        format=config.log_format,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(config.logs_dir / "qcl.log")
        ]
    )
    
    return logging.getLogger("qcl")