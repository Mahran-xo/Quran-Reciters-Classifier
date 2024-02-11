from pydub import AudioSegment
from fastapi import FastAPI,File,UploadFile
import random
import numpy as np
import tensorflow as tf
from pytube import YouTube
from pydub import AudioSegment
import uvicorn
# import arabic_reshaper
# from bidi.algorithm import get_display

app = FastAPI()
# Example usage
# video_url = 'https://www.youtube.com/watch?v=K7dz7JaPtoo'
output_path = './output_folder'
imported = tf.saved_model.load("saved")


def download_youtube_audio(video_url, output_path, output_format='wav'):
    # Download the YouTube video
    url = video_url
    output_dir = output_path
    youtube_video = YouTube(url)
    video_stream = youtube_video.streams.filter(only_audio=True).first()
    video_stream.download(output_dir)

    # Convert the downloaded audio to WAV format
    audio_path = f"{output_path}/{youtube_video.title}.{output_format}"
    audio = AudioSegment.from_file(f"{output_path}/{video_stream.default_filename}")
    audio.export(audio_path, format=output_format)

    return audio_path


def extract_random_second(input_audio_path, output_audio_path):
    audio_path_in=input_audio_path
    audio_path_out=output_audio_path
    audio = AudioSegment.from_file(audio_path_in)
    audio_duration = len(audio)

    # Choose a random starting point within the audio
    start_time = random.randint(0, audio_duration - 1000)  # 1000 milliseconds = 1 second
    one_second_audio = audio[start_time:start_time + 1000]
    one_second_audio.export(audio_path_out, format="wav")


@app.post("predict/")
async def predict(url:str):

    INPUT = download_youtube_audio(url, output_path)
    extract_random_second(INPUT, INPUT)

    
    pred = imported(INPUT)
    class_names=pred['class_names']
    class_id=np.argmax(pred['class_ids'])
    final_pred=class_names[class_id]

    label =final_pred.numpy().decode('utf-8')


    return {"prediction": label}

if __name__ == "__main__":
    

    uvicorn.run(app, host="127.0.0.1", port=8000)
