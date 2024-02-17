from fastapi import FastAPI
import numpy as np
import os
import shutil
import tensorflow as tf
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from vals import download_youtube_audio,segment_and_extract,remove_all_content

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

# Remove __pycache__ folder after execution
current_dir = os.path.dirname(os.path.abspath(__file__))
cache_folder = os.path.join(current_dir, "vals", "__pycache__")

try:
    shutil.rmtree(cache_folder)
except OSError as e:
    print(f"Error removing __pycache__ folder: {e}")


output_path = 'output_folder'
imported = tf.saved_model.load("saved")

@app.post("/predict/")
async def predict(link:str):
    input_video = download_youtube_audio(link, output_path,return_path=True)
    one_second_path = segment_and_extract(input_video, output_path)
    print(one_second_path)
    pred = imported(one_second_path)
    class_names=pred['class_names']
    class_id=np.argmax(pred['class_ids'])
    final_pred=class_names[class_id]

    label =final_pred.numpy().decode('utf-8')
    remove_all_content('output_folder')
    return {"prediction": label}

if __name__ == "__main__":
    
    uvicorn.run(app, host="127.0.0.1", port=8000)



    
