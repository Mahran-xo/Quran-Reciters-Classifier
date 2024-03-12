import os
import subprocess
from pytube import YouTube
from .conf import colored_tqdm ,rprint
from .apiUtils import choose_random_segment
import subprocess
import random
import shutil
import uuid
import subprocess
import os

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
            output_filename = f"{prefix}_segment_%03d.{export_format}"
            ffmpeg_cmd = [
                "ffmpeg",
                "-i", input_path,
                "-vn",
                "-ar", "44100",
                "-ac", "2",
                "-c:a", "pcm_s16le",
                "-segment_time", str(segment_length),
                "-f", "segment",
                os.path.join(output_path, output_filename)
            ]

            # Run FFmpeg command
            subprocess.run(ffmpeg_cmd)

    except Exception as e:
        # Handle exceptions and print an informative message
        rprint(f"Error processing audio: {e}")


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



def on_progress(stream, chunk, bytes_remaining):
    """Callback function"""
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    pct_completed = bytes_downloaded / total_size * 100
    print(f"Status: {round(pct_completed, 2)} %")

def download_youtube_audio(url, output_path):
    yt = YouTube(url,on_progress_callback=on_progress)

    audio_stream = yt.streams.filter(only_audio=True).order_by("abr").first()
    rprint(yt.streams.filter(only_audio=True).order_by("abr"))

    unique_id = str(uuid.uuid4())
    video_file_name = f"video_{unique_id}.mp4"
    output_path = 'output_folder'
    wav_out = 'segmented_long_audio'
    audio_stream.download(output_path, filename=video_file_name)

    input_video = os.path.join(output_path, video_file_name)
    output_audio=os.path.join(wav_out,f"{str(uuid.uuid4())[:-10]}_LONG.wav")

    subprocess.run(['ffmpeg', 
                    '-i', input_video,
                    "-vn",
                    "-ar", "22050",
                    "-ac", "2",
                    "-c:a", "pcm_s16le",
                    '-ss', '150',
                    '-t', '600', 
                     output_audio])
    
    audio_path_list = [file for file in os.listdir(wav_out) if file.endswith(".wav")]

    for file in audio_path_list:
        split_audio(os.path.join(wav_out,file), f"{str(uuid.uuid4())[:-10]}_LONG2SHORT", output_path,segment_length=1, export_format='wav') 
