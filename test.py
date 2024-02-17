import numpy as np
import tensorflow as tf
import arabic_reshaper
from vals import download_youtube_audio,segment_and_extract,remove_all_content
from bidi.algorithm import get_display
import shutil
import os

# Remove __pycache__ folder after execution
current_dir = os.path.dirname(os.path.abspath(__file__))
cache_folder = os.path.join(current_dir, "vals", "__pycache__")

try:
    shutil.rmtree(cache_folder)
except OSError as e:
    print(f"Error removing __pycache__ folder: {e}")

    
output_path = 'output_folder'
imported = tf.saved_model.load("saved")


def predict(link):
    input_video = download_youtube_audio(link, output_path,return_path=True)
    one_second_path = segment_and_extract(input_video, output_path)
    print(one_second_path)
    pred = imported(one_second_path)
    class_names=pred['class_names']
    class_id=np.argmax(pred['class_ids'])
    final_pred=class_names[class_id]

    label =final_pred.numpy().decode('utf-8')
    remove_all_content('output_folder')
    return label

if __name__ == "__main__":
    label=predict("https://www.youtube.com/watch?v=PWCPbTHj-vY")
    print(f"\033[92m{get_display(arabic_reshaper.reshape(label))}\033[0m")

    
