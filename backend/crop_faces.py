import cv2
from mtcnn import MTCNN
import sys
import os
import json
import tensorflow as tf

# Set TensorFlow logging level
tf.get_logger().setLevel('ERROR')

# Configure GPU memory growth
physical_devices = tf.config.list_physical_devices('GPU')
for physical_device in physical_devices:
    tf.config.experimental.set_memory_growth(physical_device, True)

base_path = '.\\dataset\\'

def get_filename_only(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]

try:
    with open(os.path.join(base_path, 'metadata.json')) as metadata_json:
        metadata = json.load(metadata_json)
        print(f'Loaded metadata with {len(metadata)} entries.')
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error loading metadata: {e}")
    sys.exit()

detector = MTCNN()

for filename in metadata.keys():
    tmp_path = os.path.join(base_path, get_filename_only(filename))
    print(f'Processing Directory: {tmp_path}')
    
    if not os.path.isdir(tmp_path):
        print(f"Directory not found: {tmp_path}")
        continue

    frame_images = [x for x in os.listdir(tmp_path) if os.path.isfile(os.path.join(tmp_path, x))]
    faces_path = os.path.join(tmp_path, 'faces')
    os.makedirs(faces_path, exist_ok=True)
    print(f'Creating Directory: {faces_path}')
    print('Cropping Faces from Images...')

    for frame in frame_images:
        frame_path = os.path.join(tmp_path, frame)
        print(f'Processing {frame}')
        
        image = cv2.cvtColor(cv2.imread(frame_path), cv2.COLOR_BGR2RGB)
        results = detector.detect_faces(image)
        print(f'Faces Detected: {len(results)}')
        
        count = 0
        for result in results:
            bounding_box = result['box']
            confidence = result['confidence']
            
            if len(results) < 2 or confidence > 0.95:
                margin_x = bounding_box[2] * 0.3
                margin_y = bounding_box[3] * 0.3
                x1 = max(int(bounding_box[0] - margin_x), 0)
                x2 = min(int(bounding_box[0] + bounding_box[2] + margin_x), image.shape[1])
                y1 = max(int(bounding_box[1] - margin_y), 0)
                y2 = min(int(bounding_box[1] + bounding_box[3] + margin_y), image.shape[0])
                
                crop_image = image[y1:y2, x1:x2]
                new_filename = os.path.join(faces_path, f'{get_filename_only(frame)}-{count:02d}.png')
                count += 1
                cv2.imwrite(new_filename, cv2.cvtColor(crop_image, cv2.COLOR_RGB2BGR))
            else:
                print('Skipped a face due to low confidence.')
