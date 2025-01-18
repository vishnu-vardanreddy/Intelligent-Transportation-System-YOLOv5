import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_random_filename():
    # Generate realistic image filenames
    prefixes = ['IMG_', 'DSC_', 'DCIM_', 'CAM_']
    return f"{random.choice(prefixes)}{random.randint(1000, 9999)}.jpg"

def generate_random_bbox():
    # Generate random bounding box coordinates in YOLO format (normalized)
    x = round(random.uniform(0.1, 0.9), 3)
    y = round(random.uniform(0.1, 0.9), 3)
    w = round(random.uniform(0.1, 0.3), 3)
    h = round(random.uniform(0.1, 0.3), 3)
    return x, y, w, h

def generate_random_metadata():
    # Generate random metadata for each image
    resolutions = [(1920, 1080), (3840, 2160), (2560, 1440), (1280, 720)]
    file_sizes = [round(random.uniform(2, 10), 2) for _ in range(4)]  # MB
    return random.choice(resolutions), random.choice(file_sizes)

def create_object_detection_dataset():
    # Common objects in detection datasets
    object_classes = ['person', 'car', 'truck', 'bicycle', 'motorcycle', 'dog', 'cat', 
                     'bus', 'traffic_light', 'stop_sign']
    
    # Initialize lists to store data
    data = []
    
    # Generate 50 random entries
    for i in range(50):
        # Basic image information
        image_file = generate_random_filename()
        resolution, file_size = generate_random_metadata()
        
        # Generate 1-4 objects per image
        num_objects = random.randint(1, 4)
        
        # Generate detection information for each object
        for j in range(num_objects):
            object_class = random.choice(object_classes)
            confidence = round(random.uniform(0.75, 0.99), 3)
            x, y, w, h = generate_random_bbox()
            
            # Calculate timestamp within last month
            timestamp = datetime.now() - timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            # Compile row data
            row_data = {
                'image_id': i + 1,
                'filename': image_file,
                'timestamp': timestamp,
                'resolution_width': resolution[0],
                'resolution_height': resolution[1],
                'file_size_mb': file_size,
                'object_class': object_class,
                'confidence': confidence,
                'bbox_x': x,
                'bbox_y': y,
                'bbox_width': w,
                'bbox_height': h,
                'annotation_verified': random.choice([True, False]),
                'lighting_condition': random.choice(['daylight', 'night', 'evening', 'morning']),
                'weather': random.choice(['clear', 'cloudy', 'rainy', 'sunny']),
                'scene_type': random.choice(['urban', 'rural', 'indoor', 'highway'])
            }
            data.append(row_data)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Sort by image_id and timestamp
    df = df.sort_values(['image_id', 'timestamp'])
    
    # Export to Excel
    output_file = 'object_detection_dataset.xlsx'
    df.to_excel(output_file, index=False)
    print(f"Dataset has been generated and saved to {output_file}")
    
    return df

# Generate the dataset
dataset = create_object_detection_dataset()