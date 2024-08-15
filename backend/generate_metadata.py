import os
import json

def extract_original_name(file_name):
    parts = file_name.split('_')
    if len(parts) > 2:
        return f"{parts[0]}_{parts[2]}"
    return "null"

def create_metadata_from_dataset(dataset_folder, output_file):
    metadata = {}
    real_folder = os.path.join(dataset_folder, 'real')
    fake_folder = os.path.join(dataset_folder, 'fake')

    # Process 'real' videos
    if os.path.exists(real_folder):
        for file_name in os.listdir(real_folder):
            if file_name.lower().endswith('.mp4'):
                metadata[file_name] = {
                    "label": "REAL",
                    "split": "train",
                    "original": "null"
                }

    # Process fake videos
    if os.path.exists(fake_folder):
        for file_name in os.listdir(fake_folder):
            if file_name.lower().endswith('.mp4'):
                metadata[file_name] = {
                    "label": "FAKE",
                    "split": "train",
                    "original": extract_original_name(file_name)
                }

    with open(output_file, 'w') as f:
        json.dump(metadata, f, indent=4)
    
    print(f'Metadata has been created and saved to {output_file}')

def main():
    dataset_folder = './dataset'
    metadata_file = './metadata.json'

    create_metadata_from_dataset(dataset_folder, metadata_file)


main()
