from fastapi import FastAPI
import uvicorn
import os
import shutil
import random 
import uuid
from tqdm import tqdm
import tensorflow as tf
from statistics import mode
from vals import (download_youtube_audio,
                  choose_random_segment,
                  remove_all_content,
                  split_audio,
                  rprint,
                  get_audio_duration)
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI( title="Quran Reciters Classifier",
    description="مُصنف قُرأ القرآن الكريم",
    version="1.0.0",
    timeout=120  )

# Allow all origins, methods, and headers. Adjust these ssettings based on your requirements.
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8000/docs#",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

current_dir = os.path.dirname(os.path.abspath(__file__))
cache_folder = os.path.join(current_dir, "vals", "__pycache__")

try:
    shutil.rmtree(cache_folder)
except OSError as e:
    print(f"Error removing __pycache__ folder: {e}")

    

output_path = 'output_folder'
wav_out = 'segmented_long_audio'
imported = tf.saved_model.load("saved")
classes = ['ابراهيم عبد المنعم ',
            'احمد الشلبي',
            'اسماعيل القاضي  ',
            'اوريانتو',
            'ايوب مصعب  ',
            'حسين عبد الضاهر  ',
            'خالد طوالبة  ',
            'زين ابو الكوثر  ',
            'طارق محمد  ',
            'علاء عقل  ',
            'علاء ياسر  ',
            'محمد حجازي  ',
            'مختار الحاج  ']

@app.post("/predict/")
async def predict(link:str):
    random.seed(42)
    preds = []
    max_duration=600
    input_video = download_youtube_audio(link, output_path, return_path=True)
    audio_duration = get_audio_duration(input_video)
    if audio_duration > max_duration:
        rprint('audio is too long')
        split_audio(input_video, f"{str(uuid.uuid4())[:-10]}_LONG", wav_out ,segment_length=3*60*1000 ,export_format='wav')
        audio_path_list = choose_random_segment(wav_out,4)
        for file in audio_path_list:
            split_audio(os.path.join(wav_out,file), f"{str(uuid.uuid4())[:-10]}_LONG2SHORT", output_path,segment_length=1000, export_format='wav') 
        
    else:
        split_audio(input_video, f"{str(uuid.uuid4())[:-10]}_SHORT", output_path,segment_length=1000, export_format='wav')

    
    
    # List all files in the output folder
    files_list = [file for file in os.listdir(output_path) if file.endswith(".wav")]
    
    # Take 40% of the files randomly
    num_files_to_use = int(len(files_list)*0.4)
    files_to_use = files_list[:num_files_to_use]
    
    for file in tqdm(files_to_use):
        pred = imported(os.path.join(output_path, file))
        preds.append(pred['class_ids'].numpy()[0])


    
    remove_all_content('output_folder')
    remove_all_content(wav_out)
    final_label = mode(preds)
    final_pred = classes[int(final_label)]
    
    return {"prediction": final_pred}

if __name__ == "__main__":
    
    uvicorn.run(app, host="127.0.0.1", port=8000)



    
