"""
Detection service module for helmet detection.
Integrates YOLOv11 model for object detection and classification.
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

from ultralytics import YOLO

from backend.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class DetectionResult:
    """Data class for detection results."""
    bike_boxes: List[np.ndarray]  # [x1, y1, x2, y2, conf, class_id]
    rider_boxes: List[np.ndarray]
    helmet_boxes: List[np.ndarray]
    violations: List[Dict]  # Riders without helmets
    frame: np.ndarray
    timestamp: datetime


class HelmetDetectionService:
    """
    Service for helmet detection using YOLOv11.
    
    Handles:
    - Model loading and inference
    - Detection processing (matching helmets to riders)
    - Violation identification
    - Result visualization
    """
    
    # YOLO class IDs (these need to be trained)
    BIKE_CLASS_ID = 0
    RIDER_CLASS_ID = 1
    HELMET_CLASS_ID = 2
    
    # Class names
    CLASS_NAMES = {
        BIKE_CLASS_ID: 'Bike',
        RIDER_CLASS_ID: 'Rider',
        HELMET_CLASS_ID: 'Helmet',
    }
    
    def __init__(
        self,
        model_path: str = 'yolov11n.pt',
        confidence_threshold: float = 0.5,
        iou_threshold: float = 0.45,
        device: str = 'cpu'
    ):
        """
        Initialize detection service.
        
        Args:
            model_path: Path to YOLOv11 model weights
            confidence_threshold: Minimum confidence for detections
            iou_threshold: IOU threshold for NMS
            device: Device to run inference on ('cpu' or 'cuda')
        """
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold
        self.iou_threshold = iou_threshold
        self.device = device
        
        try:
            # Load model
            logger.info(f'Loading YOLOv11 model from {model_path}')
            self.model = YOLO(model_path)
            self.model.to(device)
            logger.info(f'Model loaded successfully on device: {device}')
        except Exception as e:
            logger.error(f'Failed to load model: {e}')
            raise
    
    def detect(self, frame: np.ndarray) -> DetectionResult:
        """
        Perform detection on frame.
        
        Args:
            frame: Input frame/image
            
        Returns:
            DetectionResult with detections and violations
        """
        timestamp = datetime.now()
        
        try:
            # Run inference
            results = self.model(frame, conf=self.confidence_threshold, iou=self.iou_threshold)
            
            # Extract detections
            detections = results[0]  # First (and only) image
            boxes = detections.boxes.cpu().numpy()
            
            # Separate detections by class
            bike_boxes = []
            rider_boxes = []
            helmet_boxes = []
            
            for box in boxes:
                class_id = int(box.cls)
                if class_id == self.BIKE_CLASS_ID:
                    bike_boxes.append(box)
                elif class_id == self.RIDER_CLASS_ID:
                    rider_boxes.append(box)
                elif class_id == self.HELMET_CLASS_ID:
                    helmet_boxes.append(box)
            
            # Detect violations (riders without helmets)
            violations = self._match_riders_to_helmets(rider_boxes, helmet_boxes)
            
            # Draw results on frame
            frame_with_boxes = self._draw_detections(
                frame.copy(), bike_boxes, rider_boxes, helmet_boxes, violations
            )
            
            return DetectionResult(
                bike_boxes=bike_boxes,
                rider_boxes=rider_boxes,
                helmet_boxes=helmet_boxes,
                violations=violations,
                frame=frame_with_boxes,
                timestamp=timestamp
            )
            
        except Exception as e:
            logger.error(f'Detection failed: {e}')
            return DetectionResult(
                bike_boxes=[],
                rider_boxes=[],
                helmet_boxes=[],
                violations=[],
                frame=frame,
                timestamp=timestamp
            )
    
    def _match_riders_to_helmets(
        self,
        rider_boxes: List[np.ndarray],
        helmet_boxes: List[np.ndarray]
    ) -> List[Dict]:
        """
        Match helmets to riders and detect violations.
        
        A rider is considered safe if a helmet box is within the rider's bounding box.
        
        Args:
            rider_boxes: Bounding boxes of riders
            helmet_boxes: Bounding boxes of helmets
            
        Returns:
            List of violations (riders without helmets)
        """
        violations = []
        
        for rider_idx, rider_box in enumerate(rider_boxes):
            rider_x1, rider_y1, rider_x2, rider_y2 = rider_box.xyxy[0][:4]
            rider_conf = float(rider_box.conf)
            
            # Check if any helmet overlaps with rider
            helmet_found = False
            
            for helmet_box in helmet_boxes:
                helmet_x1, helmet_y1, helmet_x2, helmet_y2 = helmet_box.xyxy[0][:4]
                helmet_conf = float(helmet_box.conf)
                
                # Check if helmet center is within rider box (helmet detection logic)
                helmet_center_x = (helmet_x1 + helmet_x2) / 2
                helmet_center_y = (helmet_y1 + helmet_y2) / 2
                
                # Simple check: helmet center within rider box
                if (rider_x1 <= helmet_center_x <= rider_x2 and
                    rider_y1 <= helmet_center_y <= rider_y2):
                    helmet_found = True
                    break
            
            # If no helmet found, it's a violation
            if not helmet_found:
                violations.append({
                    'rider_id': rider_idx,
                    'rider_box': rider_box.xyxy[0][:4],
                    'rider_confidence': rider_conf,
                    'helmet_detected': False,
                    'violation_type': 'no_helmet'
                })
        
        return violations
    
    def _draw_detections(
        self,
        frame: np.ndarray,
        bike_boxes: List[np.ndarray],
        rider_boxes: List[np.ndarray],
        helmet_boxes: List[np.ndarray],
        violations: List[Dict]
    ) -> np.ndarray:
        """
        Draw bounding boxes and labels on frame.
        
        Args:
            frame: Input frame
            bike_boxes: Motorcycle boxes
            rider_boxes: Rider boxes
            helmet_boxes: Helmet boxes
            violations: Violation list
            
        Returns:
            Frame with drawn detections
        """
        result_frame = frame.copy()
        
        # Set of violating rider IDs
        violating_riders = {v['rider_id'] for v in violations}
        
        # Draw bikes (blue)
        for bike_box in bike_boxes:
            x1, y1, x2, y2 = map(int, bike_box.xyxy[0][:4])
            conf = float(bike_box.conf)
            cv2.rectangle(result_frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            label = f'Bike {conf:.2f}'
            cv2.putText(result_frame, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
        # Draw riders and helmets
        for rider_idx, rider_box in enumerate(rider_boxes):
            x1, y1, x2, y2 = map(int, rider_box.xyxy[0][:4])
            conf = float(rider_box.conf)
            
            # Green for safe, red for violation
            if rider_idx in violating_riders:
                color = (0, 0, 255)  # Red
                status = 'NO HELMET'
            else:
                color = (0, 255, 0)  # Green
                status = 'HELMET'
            
            cv2.rectangle(result_frame, (x1, y1), (x2, y2), color, 2)
            label = f'{status} {conf:.2f}'
            cv2.putText(result_frame, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Draw helmets (yellow)
        for helmet_box in helmet_boxes:
            x1, y1, x2, y2 = map(int, helmet_box.xyxy[0][:4])
            conf = float(helmet_box.conf)
            cv2.rectangle(result_frame, (x1, y1), (x2, y2), (0, 255, 255), 1)
            label = f'Helmet {conf:.2f}'
            cv2.putText(result_frame, label, (x1, y1 - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
        
        return result_frame
    
    def get_model_info(self) -> Dict:
        """Get model information."""
        return {
            'model_path': self.model_path,
            'confidence_threshold': self.confidence_threshold,
            'iou_threshold': self.iou_threshold,
            'device': self.device,
            'class_names': self.CLASS_NAMES,
        }
