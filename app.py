from fastapi import FastAPI,File, UploadFile, HTTPException
import uvicorn
from fastapi.responses import StreamingResponse
import os
from bidi.algorithm import get_display
import arabic_reshaper
import shutil
import random 
import time
import pandas as pd
import uuid
from tqdm import tqdm
import tensorflow as tf
from statistics import mode
from vals import (download_youtube_audio,
                  remove_all_content)
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI( title="Quran Reciters Classifier",
    description="مُصنف قُرأ القرآن الكريم",
    version="1.0.0",
    timeout=400  )

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


@app.get("/get_names")
def get_names():
    return {"reciters": classes}

@app.post("/predict/")
async def predict(link:str):

    random.seed(42)

    
    start_time = time.time()
    download_youtube_audio(link, output_path) 
    
    # List all files in the output folder
    files_list = [file for file in os.listdir(output_path) if file.endswith(".wav")]
    
    # Take 40% of the files randomly
    num_files_to_use = int(len(files_list)*0.5)
    files_to_use = files_list[:num_files_to_use]
    preds = []
    for file in tqdm(files_to_use):
        pred = imported(os.path.join(output_path, file))
        preds.append(pred['class_ids'].numpy()[0])

    
    remove_all_content(output_path)
    remove_all_content(wav_out)

    final_pred = classes[int(mode(preds))]
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Print the elapsed time
    print(f"Elapsed time: {elapsed_time} seconds")

    return {"prediction": final_pred}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)



    
