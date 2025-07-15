from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from ultralytics import YOLO
import cv2
import numpy as np
import os
from typing import List, Dict, Any
import json

from app.services.helper import detect_rooms
from app.config import config

# Initialize the router
router = APIRouter()

# Initialize model
model = YOLO(config.MODEL_PATH, task='detect')

@router.post("/detect")
async def detect_objects(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    
    try:
        # Read image file
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise HTTPException(status_code=400, detail="Could not decode image")
        
        # Convert to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Run detection
        results = model(img_rgb, conf=0.5)
        
        # Process results
        detections = []
        for result in results:
            for box in result.boxes:
                label = model.names[int(box.cls)]
                conf = float(box.conf)
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                
                detections.append({
                    'label': label,
                    'confidence': conf,
                    'box': {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
                })
        
        # Detect rooms if walls are found
        walls_detected = any(d['label'] == 'Wall' for d in detections)
        rooms = []
        if walls_detected:
            wall_boxes = [{'box': [d['box']['x1'], d['box']['y1'], d['box']['x2'], d['box']['y2']], 
                         'conf': d['confidence']} 
                        for d in detections if d['label'] == 'Wall']
            
            _, rooms_info = detect_rooms(img, wall_boxes)
            rooms = [{'id': r['id'], 'area': r['area'], 
                     'box': {'x1': r['box'][0], 'y1': r['box'][1], 
                            'x2': r['box'][2], 'y2': r['box'][3]}}
                    for r in rooms_info]
        
        # Count objects
        object_counts = {}
        for d in detections:
            object_counts[d['label']] = object_counts.get(d['label'], 0) + 1
        
        return {
            'detections': detections,
            'object_counts': object_counts,
            'rooms': rooms,
            'image_size': {'width': img.shape[1], 'height': img.shape[0]}
        }
        
    except Exception as e:
        raise HTTPException