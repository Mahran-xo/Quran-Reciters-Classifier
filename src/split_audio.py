import os
import subprocess

def split_video(input_file, output_pattern, segment_time):
    command = [
        'ffmpeg',
        '-i', input_file,
        '-c', 'copy',
        '-map', '0',
        '-segment_time', str(segment_time),
        '-f', 'segment',
        output_pattern
    ]
    subprocess.run(command)

def split_all_videos(input_directory, output_directory, segment_time):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for file_name in os.listdir(input_directory):
        if file_name.endswith('.mp4'):
            input_file = os.path.join(input_directory, file_name)
            output_pattern = os.path.join(output_directory, f'output_%03d_{file_name}')
            split_video(input_file, output_pattern, segment_time)

# Set your input directory, output directory, and segment time
name = 'ismail al kady'
dst_name = 'ISMAIL-ALKADY'
input_directory = f'/mnt/c/FOLDERSSSSSSSSSSSSSSSSSS/Projects/QuranReaderClf/downloads/{name}'
output_directory = f'/mnt/c/FOLDERSSSSSSSSSSSSSSSSSS/Projects/QuranReaderClf/downloads/{dst_name}'
segment_time = 60  # 30 minutes in seconds

split_all_videos(input_directory, output_directory, segment_time)
