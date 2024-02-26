from pydub import AudioSegment
import os
from pytube import YouTube
import time
from .validators import is_silent 
from .conf import colored_tqdm ,rprint
import subprocess
import random
import shutil
import uuid
import sys

global_seed = 42
random.seed(global_seed)

def split_audio(input_path:str, prefix:str, output_path:str, segment_length=3 * 60 * 1000, export_format="mp3", bitrate="192k"):
    """
    takes in a long audio and splits in into multiple segmets\n
    `input_path`: path of the input audio file\n
    `prefix`: prefix of the output audio file (`e.g.` : `f"{NAME}_URL({i + 1})"`) \n
    `output_path`: output directory\n
    `segment_length`: length of the segment `default 3 mins` `1000 for one second` \n
    `export_format`: export format (`e.g`: `mp3` , `wav`)\n
    `bitrate`: bitrate\n
    """
    try:
        audio = AudioSegment.from_file(input_path)

        # Calculate the number of segments
        # segment_duration = 3 * 60 * 1000
        num_segments = len(audio) // segment_length

        # Split the audio into segments
        progress_bar = colored_tqdm(range(num_segments), color_code="\033[92m", desc=f"Processing {prefix}", unit="segment")    
        for i in progress_bar:
            start_time = i * segment_length
            end_time = (i + 1) * segment_length
            segment = audio[start_time:end_time]

            # Check if the segment is silent using the is_silent function
            if is_silent(segment):
                sys.stdout.write("\r" + f"\033[91m{prefix}: Silent segment skipped\033[0m")
                sys.stdout.flush()
                continue

            # Save each non-silent segment
            output_filename = f"{prefix}_segment_{i + 1}.{export_format}"
            segment.export(os.path.join(output_path, output_filename), format=export_format, bitrate=bitrate)

    except Exception as e:
        # Handle exceptions and print an informative message
        rprint(f"Error processing audio: {e}")

def convert_mp3_to_wav(input_file:str, output_file:str):
    """
    convert from `mp3` to `wav`
    """
    subprocess.run(['ffmpeg','-y', '-loglevel', 'panic', '-i', input_file, '-acodec', 'pcm_s16le', '-ar', '44100', f"{output_file}.wav"])
    return f"{output_file}.wav"

def shuffle_and_copy_data(input_dir:str, output_dir:str, num_files:int):
    """
    shuffles and copies files from a directory to another
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Walk through the input directory
    for root, dirs, files in os.walk(input_dir):
        # Create corresponding subdirectories in the output directory
        relative_path = os.path.relpath(input_dir, input_dir)
        output_subdir = os.path.join(output_dir, relative_path)
        if not os.path.exists(output_subdir):
            os.makedirs(output_subdir)

        # Shuffle the list of files
        random.shuffle(files)

        # Copy and convert the first 'num_files' to the output directory
        for file in files[:num_files]:
            src_path = os.path.join(input_dir, file)
            dest_path = os.path.join(output_subdir, file)
            shutil.copy(src_path, dest_path)


def download_youtube_audio(url, output_path, progress_callback=None, return_path=False):
    yt = YouTube(url)
    audio_stream = yt.streams.get_audio_only("mp4")

    # Generate a unique identifier
    unique_id = str(uuid.uuid4())

    # Append the unique identifier to the file name
    video_file_name = f"video_{unique_id}.mp4"

    # Download the audio stream with the modified file name
    audio_stream.download(output_path, filename=video_file_name)

    # Simulate a total of 10 steps for the progress
    total_steps = 10

    for step in range(1, total_steps + 1):
        # Simulate downloading progress
        time.sleep(0.1)

        # If a progress callback is provided, update the progress
        if progress_callback:
            progress_callback(step / total_steps)

    if return_path:
        return str(os.path.join(output_path, video_file_name))