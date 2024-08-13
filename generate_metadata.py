import os
import json

def create_metadata_from_folder(folder_path, output_file):
    metadata = {}
    
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith('.mp4'):
            # Create metadata entry for the file
            metadata[file_name] = {
                "label": "FAKE",
                "split": "train",
                "original": "null"
            }
    
    with open(output_file, 'w') as f:
        json.dump(metadata, f, indent=4)
    
    print(f'Metadata has been created and saved to {output_file}')

def main():
    converted_folder = './converted_folder'
    metadata_file = './metadata.json'

    create_metadata_from_folder(converted_folder, metadata_file)


main()
