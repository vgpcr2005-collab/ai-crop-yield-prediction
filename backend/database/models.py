"""
Database models for Helmet Detection System.
Defines SQLAlchemy ORM models for storing detection and violation data.
"""

from datetime import datetime
from pathlib import Path
from typing import Optional

from sqlalchemy import Column, String, Float, DateTime, Boolean, Integer, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()


class Violation(Base):
    """
    Violation model for storing helmet detection violations.
    
    Attributes:
        id: Unique violation ID
        violation_id: User-friendly violation identifier
        camera_id: ID of the camera that detected the violation
        timestamp: When the violation occurred
        image_path: Path to the screenshot
        image_data: Binary image data (optional)
        confidence: Detection confidence score (0-1)
        biker_detected: Whether a biker was detected
        helmet_detected: Whether a helmet was detected
        status: Violation status (e.g., 'new', 'reviewed', 'resolved')
        created_at: Database record creation time
        updated_at: Last update time
    """
    
    __tablename__ = 'violations'
    
    id = Column(Integer, primary_key=True)
    violation_id = Column(String(50), unique=True, nullable=False, index=True)
    camera_id = Column(String(50), nullable=False, default='0')
    timestamp = Column(DateTime, nullable=False)
    image_path = Column(String(500), nullable=True)
    image_data = Column(LargeBinary, nullable=True)
    
    # Detection details
    confidence = Column(Float, nullable=False)
    biker_detected = Column(Boolean, default=True)
    helmet_detected = Column(Boolean, default=False)
    
    # Status
    status = Column(String(20), default='new', nullable=False)  # new, reviewed, resolved
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'violation_id': self.violation_id,
            'camera_id': self.camera_id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'image_path': self.image_path,
            'confidence': self.confidence,
            'biker_detected': self.biker_detected,
            'helmet_detected': self.helmet_detected,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class Detection(Base):
    """
    Detection model for storing detection statistics and metadata.
    
    Attributes:
        id: Unique detection record ID
        camera_id: ID of the camera
        timestamp: When detection occurred
        total_bikes: Total motorcycles detected in frame
        total_riders: Total riders detected in frame
        riders_with_helmet: Number of riders wearing helmets
        riders_without_helmet: Number of riders without helmets
    """
    
    __tablename__ = 'detections'
    
    id = Column(Integer, primary_key=True)
    camera_id = Column(String(50), nullable=False, default='0')
    timestamp = Column(DateTime, nullable=False, index=True)
    
    # Detection counts
    total_bikes = Column(Integer, default=0)
    total_riders = Column(Integer, default=0)
    riders_with_helmet = Column(Integer, default=0)
    riders_without_helmet = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'camera_id': self.camera_id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'total_bikes': self.total_bikes,
            'total_riders': self.total_riders,
            'riders_with_helmet': self.riders_with_helmet,
            'riders_without_helmet': self.riders_without_helmet,
        }


class CameraConfig(Base):
    """
    Camera configuration model for managing multiple camera sources.
    
    Attributes:
        id: Primary key
        camera_id: Unique camera identifier
        name: Display name for the camera
        source: Camera source (URL, file path, or device ID)
        is_active: Whether the camera is currently active
    """
    
    __tablename__ = 'camera_configs'
    
    id = Column(Integer, primary_key=True)
    camera_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    source = Column(String(500), nullable=False)  # RTSP URL, file path, or device ID
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'camera_id': self.camera_id,
            'name': self.name,
            'source': self.source,
            'is_active': self.is_active,
        }


def init_db(engine) -> None:
    """Initialize database and create tables."""
    Base.metadata.create_all(engine)


def drop_all(engine) -> None:
    """Drop all tables (use with caution)."""
    Base.metadata.drop_all(engine)
