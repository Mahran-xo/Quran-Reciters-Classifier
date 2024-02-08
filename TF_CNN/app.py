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

# instantiate FastAPI app
app = FastAPI()



def download_youtube_video(url, output_path, filename, itag):
    try:
        # Download the YouTube video with a specific ITAG
        yt = YouTube(url)
        ys = yt.streams.get_by_itag(itag)

        if ys:
            # Download the video stream
            ys.download(output_path, filename)
            print(f"Video saved to: {output_path}/{filename}")
        else:
            print(f"No stream found for ITAG {itag}.")

    except Exception as e:
        print(f"Error: {e}")


def cut_video_and_convert_audio(input_video_path, output_audio_path, cut_duration=60):
    try:
        # Get the original video duration
        original_duration = float(subprocess.check_output(['ffprobe', '-i', input_video_path, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=%s' % ("p=0")]).decode('utf-8').strip())

        # Calculate the start time for the middle cut
        start_time = (original_duration - cut_duration) / 2

        # Use ffmpeg to cut the video segment
        modified_path = input_video_path.replace('.mp4', '60.mp4')
        subprocess.call(['ffmpeg', '-i', input_video_path, '-ss', str(start_time), '-t', str(cut_duration), '-q:a', '0', modified_path])

        # Convert the cut video segment to mp3
        subprocess.call(['ffmpeg', '-i', modified_path, '-q:a', '0', '-map', 'a', '-ar', '22050', output_audio_path])

        print(f"Audio saved to: {output_audio_path}")

    except Exception as e:
        print(f"Error: {e}")


@app.post("/predict")
async def predict(link: str):


    file_name_mp4 = f"vid.mp4"
    file_name_mp3 = f"TF_CNN/aud.mp3"
    download_youtube_video(link, output_path="TF_CNN",filename=file_name_mp4,itag="137")
    cut_video_and_convert_audio(f'TF_CNN/{file_name_mp4}', "file_name_mp3", cut_duration=60)

    # instantiate keyword spotting service singleton and get prediction
    kss = Keyword_Spotting_Service()
    predicted_keyword = kss.predict(file_name_mp3)

    # we don't need the audio file anymore - let's delete it!
    # os.remove(file_name_mp3)
    # os.remove(f'TF_CNN/{file_name_mp4}')
    # os.remove(f'TF_CNN/{file_name_mp4}'.replace('.mp4', '60.mp4'))

    # send back result as a JSON response
    result = {
        "name": predicted_keyword
        }
    return JSONResponse(content=result)

if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=8000)
