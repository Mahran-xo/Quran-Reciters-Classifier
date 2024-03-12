from fastapi import (FastAPI,
                     File, 
                     UploadFile, 
                     HTTPException, 
                     BackgroundTasks)
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse,JSONResponse
import os
import json
from typing import List
import aiohttp
from datetime import datetime
import asyncio
import shutil
import random 
import time
import pandas as pd
from tqdm import tqdm
import tensorflow as tf
from statistics import mode
from vals import (download_youtube_audio,
                  RECITERS as classes,
                  remove_all_content)
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI( title="Quran Reciters Classifier",
    description="مُصنف قُرأ القرآن الكريم",
    version="1.0.0",
    timeout=40000  )

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

# Mount a directory to serve static files (uploaded Excel files)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

current_dir = os.path.dirname(os.path.abspath(__file__))
cache_folder = os.path.join(current_dir, "vals", "__pycache__")

try:
    shutil.rmtree(cache_folder)
except OSError as e:
    print(f"Error removing __pycache__ folder: {e}")

    
is_process_running = False
output_path = 'output_folder'
wav_out = 'segmented_long_audio'
imported = tf.saved_model.load("saved")
progress = None
total_rows=None


@app.get("/get_names")
def get_names():
    # Assuming 'classes' is a list of strings
    # You can replace 'classes' with your actual data structure
    reciters_with_keys = [{"reciter_id": idx, "reciter_name": reciter} for idx, reciter in enumerate(classes)]
    return {"reciters": reciters_with_keys}


@app.get("/progress/")
async def check_progress():
    global progress
    global total_rows

    if is_process_running:
        if progress is not None and total_rows is not None:
            return JSONResponse(content={"progress": progress, "total_rows": total_rows})
        else:
            return JSONResponse(content={"message": "Progress information not available yet"})
    else:
        return JSONResponse(content={"message": "No process is currently running"})


@app.post("/predict/")
async def process_excel(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    global is_process_running

    if is_process_running:
        raise HTTPException(status_code=409, detail="Another process is currently running, please try again later.")

    # remove_all_content("uploads")
    excel_path = os.path.join("uploads", file.filename)
    with open(excel_path, "wb") as f:
        f.write(file.file.read())

    # Start background task for processing and prediction
    background_tasks.add_task(process_and_predict_background, excel_path)

    # Return an immediate response indicating file received
    return JSONResponse(content={"message": "File received for processing and prediction"})


@app.get("/files/")
async def list_available_excel_files():
    # Specify the directory where the files are stored
    base_directory = "uploads"

    # List all files in the directory with .xlsx extension
    xlsx_files = [filename for filename in os.listdir(base_directory) if filename.lower().endswith(".xlsx")]

    # Get creation time and status for each file
    file_info = []
    for file_name in xlsx_files:
        file_path = os.path.join(base_directory, file_name)
        creation_time = datetime.fromtimestamp(os.path.getctime(file_path)).strftime("%I:%M %p %d/%m/%Y")
        
        # Check if the file name contains "modified_"
        if "modified_" in file_name:
            status_flag = '1'  # Processed
        else:
            status_flag = '0'  # Not processed

        file_info.append({"file": file_name, "time_created": creation_time, "status": status_flag})

    # Return the list of dictionaries
    return file_info



@app.get("/download_excel/{filename}")
async def download_processed_excel(filename: str):
    # Specify the directory where the files are stored
    base_directory = "uploads"

    # Check if the requested file is an .xlsx file
    if not filename.lower().endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Invalid file format. Only .xlsx files are allowed.")

    # Construct the path for the requested file
    requested_file_path = os.path.join(base_directory, filename)

    # Check if the file exists
    if os.path.exists(requested_file_path):
        # Return the Excel file as a FileResponse
        return FileResponse(path=requested_file_path, filename=filename, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    else:
        # Return a 404 Not Found response if the file does not exist
        raise HTTPException(status_code=404, detail="File not found")


@app.get("/download/{filename}")
async def download_processed_excel_as_json(filename: str):
    # Specify the directory where the files are stored
    base_directory = "uploads"

    # Check if the requested file is an .xlsx file
    if not filename.lower().endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Invalid file format. Only .xlsx files are allowed.")

    # Construct the path for the requested file
    requested_file_path = os.path.join(base_directory, filename)

    # Check if the file exists
    if os.path.exists(requested_file_path):
        # Read the Excel file into a DataFrame
        df = pd.read_excel(requested_file_path)

        # Convert the DataFrame to a JSON dict, handling float conversion
        json_dict = json.loads(df.to_json(orient='records', date_format='iso', default_handler=str))

        # Return the JSON dict as the response
        return JSONResponse(content=json_dict)
    else:
        # Return a 404 Not Found response if the file does not exist
        raise HTTPException(status_code=404, detail="File not found")




def predict(link:str):

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

    return final_pred
def process_and_predict(df: pd.DataFrame) -> pd.DataFrame:
    global progress
    global total_rows
    progress = 0
    total_rows = len(df)
    for index, row in df.iterrows():
        link = row["الإجمالي"]
        link = f"https://www.youtube.com/watch?v={link}"
        final_pred = predict(link)
        df.at[index, "اسم القارئ"] = final_pred
        progress = index + 1
    progress = None
    total_rows = None
    return df


def process_and_predict_background(excel_path: str):
    global is_process_running
    # Read Excel file and process predictions
    is_process_running = True
    df = pd.read_excel(excel_path, skiprows=[0])
    modified_df = process_and_predict(df)

    # Save the modified DataFrame back to Excel
    modified_excel_path = os.path.join("uploads", "modified_" + os.path.basename(excel_path))
    modified_df.to_excel(modified_excel_path, index=False)
    is_process_running = False


async def download_excel(url: str) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.read()
            else:
                raise HTTPException(status_code=response.status, detail="Failed to download Excel file")



async def simulate_excel_generation(background_tasks: BackgroundTasks, url: str) -> None:
    # Simulate some async process (e.g., Excel generation)
    await asyncio.sleep(5)
    background_tasks.add_task(download_excel, url)
    
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)



    
