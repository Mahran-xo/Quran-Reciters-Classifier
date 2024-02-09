from pydub import AudioSegment
import random
import numpy as np
import tensorflow as tf
from pytube import YouTube
from pydub import AudioSegment
import arabic_reshaper
from bidi.algorithm import get_display

# Example usage
video_url = 'https://www.youtube.com/watch?v=K7dz7JaPtoo'
output_path = './output_folder'

def download_youtube_audio(video_url, output_path, output_format='wav'):
    # Download the YouTube video
    youtube_video = YouTube(video_url)
    video_stream = youtube_video.streams.filter(only_audio=True).first()
    video_stream.download(output_path)

    # Convert the downloaded audio to WAV format
    audio_path = f"{output_path}/{youtube_video.title}.{output_format}"
    audio = AudioSegment.from_file(f"{output_path}/{video_stream.default_filename}")
    audio.export(audio_path, format=output_format)

    return audio_path


INPUT = download_youtube_audio(video_url, output_path)

def extract_random_second(input_audio_path, output_audio_path):
    # Load the audio file
    audio = AudioSegment.from_file(input_audio_path)

    # Get the duration of the audio in milliseconds
    audio_duration = len(audio)

    # Choose a random starting point within the audio
    start_time = random.randint(0, audio_duration - 1000)  # 1000 milliseconds = 1 second

    # Extract one second of audio from the randomly chosen starting point
    one_second_audio = audio[start_time:start_time + 1000]

    # Save the one-second audio segment to a new file
    one_second_audio.export(output_audio_path, format="wav")



extract_random_second(INPUT, INPUT)


imported = tf.saved_model.load("saved")
pred = imported(INPUT)
class_names=pred['class_names']
class_id=np.argmax(pred['class_ids'])
final_pred=class_names[class_id]

label =final_pred.numpy().decode('utf-8')


print(f"\033[92m{get_display(arabic_reshaper.reshape(label))}\033[0m")
