"""
Configuration module for Helmet Detection System.
Handles environment-based configuration and constants.
"""

import os
from pathlib import Path
from typing import Optional


class Config:
    """Base configuration class."""
    
    # Flask
    DEBUG: bool = False
    TESTING: bool = False
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DATABASE_PATH = BASE_DIR / 'backend' / 'database' / 'helmet_detection.db'
    SQLALCHEMY_DATABASE_URI: str = f'sqlite:///{DATABASE_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    
    # Upload paths
    VIOLATIONS_UPLOAD_DIR = BASE_DIR / 'backend' / 'runs' / 'violations'
    DETECTIONS_UPLOAD_DIR = BASE_DIR / 'backend' / 'runs' / 'detections'
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max
    
    # Detection
    CONFIDENCE_THRESHOLD: float = 0.5
    IOU_THRESHOLD: float = 0.45
    MODEL_NAME: str = 'yolov11n.pt'  # nano model for faster inference
    DEVICE: str = 'cpu'  # or 'cuda' for GPU
    
    # API
    API_VERSION: str = 'v1'
    CORS_ORIGINS: list = ['http://localhost:5173', 'http://localhost:3000']
    
    # Logging
    LOG_LEVEL: str = 'INFO'
    LOG_FILE: Path = BASE_DIR / 'backend' / 'logs' / 'app.log'
    
    # Camera
    DEFAULT_CAMERA_ID: str = '0'
    FRAME_SKIP: int = 5  # Process every 5th frame for faster inference
    
    @classmethod
    def ensure_directories(cls) -> None:
        """Ensure all required directories exist."""
        cls.VIOLATIONS_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        cls.DETECTIONS_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        cls.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
        cls.LOG_FILE.parent.mkdir(parents=True, exist_ok=True)


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    DEVICE: str = 'cuda'  # Use GPU in production


def get_config(env: Optional[str] = None) -> Config:
    """Get configuration based on environment."""
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    
    config_map = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
    }
    
    return config_map.get(env, DevelopmentConfig)
