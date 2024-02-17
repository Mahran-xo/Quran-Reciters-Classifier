from pydub import AudioSegment
import random
import os
import shutil
from pydub import AudioSegment
from .utilss import split_audio , convert_mp3_to_wav
from .conf import rprint,gprint

global_seed = 42
random.seed(global_seed)

def choose_random_file_with_prefix(folder_path, prefix):
    files_with_prefix = [file for file in os.listdir(folder_path) if file.startswith(prefix)]

    if files_with_prefix:
        random_file = random.choice(files_with_prefix)
        return os.path.join(folder_path, random_file)
    else:
        rprint(f"No files found with the prefix '{prefix}'.")
        return None

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


def segment_long_audio(input_file_path, output_folder_path):
    # Load the audio file
    audio = AudioSegment.from_file(input_file_path)

    # Define the segment duration in milliseconds (3 minutes)
    segment_duration = 3 * 60 * 1000

    # Calculate the number of segments
    num_segments = len(audio) // segment_duration

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # Segment the audio and save each segment
    for i in range(num_segments):
        start_time = i * segment_duration
        end_time = (i + 1) * segment_duration
        segment = audio[start_time:end_time]

        # Save the segment to the output folder
        segment.export(f"{output_folder_path}/segment_{i + 1}.mp3", format="mp3")

    gprint(f"Audio segmented into {num_segments} segments of 3 minutes each.")



def get_audio_duration(audio_path):
    audio = AudioSegment.from_file(audio_path)
    return len(audio) / 1000  # Convert milliseconds to seconds


def segment_and_extract(input_audio_path, output_folder, max_duration=3600):
    try:
        audio_duration = get_audio_duration(input_audio_path)

        if audio_duration > max_duration:
            rprint('audio is too long')
            segment_long_audio(input_audio_path, output_folder)
            audio_path = choose_random_segment(output_folder)
            return str(audio_path)

        else:
            gprint('audio is not long')
            split_audio(input_path=input_audio_path, output_path=output_folder,prefix='not_long', export_format='mp3')

            mp3_files = [file for file in os.listdir(output_folder) if file.endswith(".mp3")]

            if mp3_files:
                random_mp3 = random.choice(mp3_files)
                audio_wav = convert_mp3_to_wav(os.path.join(output_folder, str(random_mp3)) ,os.path.join(output_folder, str(random_mp3).removesuffix('.mp3')))
                return audio_wav
            else:
                print("No .mp3 files found in the directory.")
                return None

    except Exception as e:
        rprint(f"Error processing audio segment: {e}")
        return None

def choose_random_segment(output_folder):
    mp3_files = [file for file in os.listdir(output_folder) if file.endswith(".mp3")]

    if mp3_files:
        random_mp3 = random.choice(mp3_files)
        split_audio(input_path=os.path.join(output_folder, str(random_mp3)), output_path=output_folder,prefix="long_audio", export_format='mp3')
        rand_one_sec = choose_random_file_with_prefix(output_folder,"long_audio")
        audio_wav = convert_mp3_to_wav(str(rand_one_sec) ,str(rand_one_sec).removesuffix('.mp3'))
        return audio_wav
    else:
        rprint("No .mp3 files found in the directory.")
        return None