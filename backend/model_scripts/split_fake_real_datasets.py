import json
import os
import shutil
import numpy as np
import splitfolders
import sys

base_path = '.\\dataset\\'
dataset_path = '.\\prepared_dataset\\'
tmp_fake_path = '.\\tmp_fake_faces'

# Create necessary directories
print(f'Creating Directory: {dataset_path}')
os.makedirs(dataset_path, exist_ok=True)

print(f'Creating Directory: {tmp_fake_path}')
os.makedirs(tmp_fake_path, exist_ok=True)

def get_filename_only(file_path):
    """Extract filename without extension from the file path."""
    return os.path.splitext(os.path.basename(file_path))[0]

# Load metadata
try:
    with open(os.path.join(base_path, 'metadata.json')) as metadata_json:
        metadata = json.load(metadata_json)
        print(f'Loaded metadata with {len(metadata)} entries.')
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error loading metadata: {e}")
    sys.exit()

real_path = os.path.join(dataset_path, 'real')
print(f'Creating Directory: {real_path}')
os.makedirs(real_path, exist_ok=True)

fake_path = os.path.join(dataset_path, 'fake')
print(f'Creating Directory: {fake_path}')
os.makedirs(fake_path, exist_ok=True)

# Copy faces based on labels
for filename, info in metadata.items():
    print(f'Processing file: {filename}')
    label = info.get('label')
    tmp_path = os.path.join(base_path, get_filename_only(filename), 'faces')
    
    if os.path.exists(tmp_path):
        if label == 'REAL':
            print(f'Copying to: {real_path}')
            shutil.copytree(tmp_path, real_path, dirs_exist_ok=True)
        elif label == 'FAKE':
            print(f'Copying to: {tmp_fake_path}')
            shutil.copytree(tmp_path, tmp_fake_path, dirs_exist_ok=True)
        else:
            print('Label not recognized, ignored.')

all_real_faces = [f for f in os.listdir(real_path) if os.path.isfile(os.path.join(real_path, f))]
print(f'Total Number of Real faces: {len(all_real_faces)}')

all_fake_faces = [f for f in os.listdir(tmp_fake_path) if os.path.isfile(os.path.join(tmp_fake_path, f))]
print(f'Total Number of Fake faces: {len(all_fake_faces)}')

# Down-sample fake faces to match the number of real faces
if len(all_fake_faces) > len(all_real_faces):
    random_faces = np.random.choice(all_fake_faces, len(all_real_faces), replace=False)
    for fname in random_faces:
        src = os.path.join(tmp_fake_path, fname)
        dst = os.path.join(fake_path, fname)
        shutil.copyfile(src, dst)
    print('Down-sampling Done!')
else:
    print('Not enough fake faces to down-sample.')

# Split dataset into Train/Val/Test sets
try:
    splitfolders.ratio(dataset_path, output='split_dataset', seed=1377, ratio=(.8, .1, .1))
    print('Train/Val/Test Split Done!')
except ModuleNotFoundError:
    print("Error: The 'splitfolders' module is not installed. Install it with 'pip install split-folders'")
