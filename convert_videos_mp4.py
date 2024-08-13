import os
import shutil
from moviepy.editor import VideoFileClip

def copy_avi_files(src_root, dst_folder):
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)
    
    for root, dirs, files in os.walk(src_root):
        for file in files:
            if file.lower().endswith('.avi'):
                src_file = os.path.join(root, file)
                dst_file = os.path.join(dst_folder, file)
                
                if not os.path.exists(dst_file):
                    shutil.copy2(src_file, dst_file)
                    print(f'Copied {src_file} to {dst_file}')
                else:
                    print(f'Skipped {src_file}, already exists in destination.')


def convert_avi_to_mp4(src_folder, dst_folder):
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)
    
    for file in os.listdir(src_folder):
        if file.lower().endswith('.avi'):
            src_file = os.path.join(src_folder, file)
            dst_file = os.path.join(dst_folder, os.path.splitext(file)[0] + '.mp4')
            
            # Convert .avi to .mp4
            try:
                with VideoFileClip(src_file) as video:
                    video.write_videofile(dst_file, codec='libx264')
                    print(f'Converted {src_file} to {dst_file}')
            except Exception as e:
                print(f'Failed to convert {src_file}: {e}')


def main():
    higher_quality_folder = './higher_quality'
    lower_quality_folder = './lower_quality'
    combined_folder = './combined_folder'
    converted_folder = './converted_folder'

    # Copy .avi files from both file paths to a combined folder
    copy_avi_files(higher_quality_folder, combined_folder)
    copy_avi_files(lower_quality_folder, combined_folder)

    # Convert .avi files to .mp4
    convert_avi_to_mp4(combined_folder, converted_folder)

    print('All .avi files have been copied and converted to .mp4.')

main()
