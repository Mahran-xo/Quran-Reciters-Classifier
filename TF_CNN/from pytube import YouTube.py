import random
import os
import uvicorn
from pytube import YouTube
from pydub import AudioSegment
from pydub.silence import detect_silence
import subprocess
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from predict import Keyword_Spotting_Service




def cut_video_and_convert_audio(input_video_path, output_audio_path, cut_duration=30):
    try:
        # Get the original video duration
        original_duration = float(subprocess.check_output(['ffprobe', '-i', input_video_path, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=%s' % ("p=0")]).decode('utf-8').strip())

        # Calculate the start time for the middle cut
        start_time = (original_duration - cut_duration) / 2

        # Use ffmpeg to cut the video segment
        modified_path = input_video_path.replace('.mp4', '_cut.mp4')
        subprocess.call(['ffmpeg', '-i', input_video_path, '-ss', str(start_time), '-t', str(cut_duration), '-q:a', '0', modified_path])

        # Convert the cut video segment to mp3 with improved settings
        subprocess.call(['ffmpeg', '-i', modified_path, '-q:a', '0', '-map', 'a', '-ar', '44100', '-b:a', '192k', '-c:a', 'libmp3lame', output_audio_path])

        print(f"Audio saved to: {output_audio_path}")

    except Exception as e:
        print(f"Error: {e}")





file_name_mp4 = f"vid.mp4"
file_name_mp3 = f"TF_CNN/aud.mp3"
cut_video_and_convert_audio(f'TF_CNN/{file_name_mp4}', file_name_mp3, cut_duration=120)

# instantiate keyword spotting service singleton and get prediction
kss = Keyword_Spotting_Service()
predicted_keyword = kss.predict(file_name_mp3)
print(predicted_keyword)