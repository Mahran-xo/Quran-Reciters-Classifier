from bidi.algorithm import get_display
from pydub import AudioSegment
import arabic_reshaper
import random
import os
import shutil
import pandas as pd
from .conf import rprint,gprint
import subprocess
import json

global_seed = 42
random.seed(global_seed)

def remove_all_content(directory_path):
    try:
        # Iterate over all items in the directory
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)

            # Check if it's a file or directory
            if os.path.isfile(item_path):
                # Remove file
                os.remove(item_path)
            elif os.path.isdir(item_path):
                # Remove directory and its contents recursively
                shutil.rmtree(item_path)

        gprint(f"All content in {directory_path} has been removed.")
    except Exception as e:
        rprint(f"Error: {e}")



# def get_audio_duration(audio_path):
#     audio = AudioSegment.from_file(audio_path)
#     return len(audio) / 1000  # Convert milliseconds to seconds


def choose_random_segment(output_folder, num_segments):
    wav_files = [file for file in os.listdir(output_folder) if file.endswith(".wav")]

    if wav_files:
        random_segments = random.sample(wav_files, min(num_segments, len(wav_files)))
        return random_segments
    else:
        rprint("No .wav files found in the directory.")
        return None
    