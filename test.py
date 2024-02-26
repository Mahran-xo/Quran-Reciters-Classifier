import os
import shutil
import random 
import uuid
import arabic_reshaper
from tqdm import tqdm
import tensorflow as tf
from statistics import mode
from bidi.algorithm import get_display
from vals import (download_youtube_audio,
                  choose_random_segment,
                  remove_all_content,
                  gprint,
                  split_audio,
                  rprint,
                  get_audio_duration)

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
            'احمد الشلبي  ',
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


def predict(link):
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
    
    # Take 20% of the files randomly
    num_files_to_use = int(len(files_list)*0.4)
    files_to_use = files_list[:num_files_to_use]
    
    for file in tqdm(files_to_use):
        pred = imported(os.path.join(output_path, file))
        preds.append(pred['class_ids'].numpy()[0])


    
    remove_all_content('output_folder')
    remove_all_content(wav_out)
    # Don't clear preds, files_to_use, and files_list here

    return preds, pred['class_ids'].numpy()[0]

if __name__ == "__main__":
    preds,class_id=predict("https://www.youtube.com/watch?v=VZ-W8pLuCDU&t=863s")
    final_label = mode(preds)
    final_pred = classes[int(final_label)]
    label = final_pred
    gprint(get_display(arabic_reshaper.reshape(label)))

    
