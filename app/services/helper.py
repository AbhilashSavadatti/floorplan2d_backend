import cv2
import numpy as np
from typing import List, Dict, Tuple

def detect_rooms(image: np.ndarray, walls: List[Dict]) -> Tuple[np.ndarray, List[Dict]]:
    """
    Detect rooms in a floor plan based on wall positions.
    
    Args:
        image: Input floor plan image
        walls: List of wall detections, each containing 'box' (x1,y1,x2,y2) and 'conf'
        
    Returns:
        Tuple containing:
        - Image with room detections drawn
        - List of detected rooms with their coordinates
    """
    img = image.copy()
    
    # Convert to grayscale and threshold
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    rooms = []
    room_counter = 1
    
    for contour in contours:
        # Filter small contours
        area = cv2.contourArea(contour)
        if area < 1000:  # Skip small contours
            continue
            
        # Get bounding box
        x, y, w, h = cv2.boundingRect(contour)
        
        # Calculate center
        center_x = x + w // 2
        center_y = y + h // 2
        
        room = {
            'id': room_counter,
            'box': (x, y, x+w, y+h),  # x1, y1, x2, y2
            'center': (center_x, center_y),
            'area': area
        }
        rooms.append(room)
        room_counter += 1
    
    return img, rooms