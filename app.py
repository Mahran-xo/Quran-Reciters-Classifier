from pydub import AudioSegment
from fastapi import FastAPI
import random
import numpy as np
import os
import shutil
import tensorflow as tf
from pytube import YouTube
from pydub import AudioSegment
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all origins, methods, and headers. Adjust these ssettings based on your requirements.
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8000/docs#",
    "http://localhost:3000",  # Example for a React app
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


output_path = './output_folder'
imported = tf.saved_model.load("saved")

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

        print(f"All content in {directory_path} has been removed.")
    except Exception as e:
        print(f"Error: {e}")


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


@app.post("/predict/")
async def predict(link:str):
    INPUT = download_youtube_audio(link, output_path)
    extract_random_second(INPUT, INPUT)
    pred = imported(INPUT)
    class_names=pred['class_names']
    class_id=np.argmax(pred['class_ids'])
    final_pred=class_names[class_id]

    label =final_pred.numpy().decode('utf-8')

    remove_all_content(output_path)
    return {"prediction": label}

if __name__ == "__main__":
    

    uvicorn.run(app, host="127.0.0.1", port=8000)
