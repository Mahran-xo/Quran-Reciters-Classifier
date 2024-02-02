import torch
import torchaudio
from utils import preprocess_audio_file
import os
import math
from model import M5

class_mapping = sorted(os.listdir("data"))


def predict(model, input,class_mapping,device):
    model.eval()
    with torch.no_grad():
        print(class_mapping)   
        predictions = model(input.unsqueeze(0).to(device))
        predicted_index = predictions.argmax(dim=-1)
        print(abs(predictions))
        predicted = class_mapping[predicted_index.squeeze()]
    return predicted


if __name__ == "__main__":
    audio_file_path = "test_examples/ismail.mp3"
    TARGET_SAMPLE_RATE = 8000
    NUM_SAMPLES = 8000
    DURATION = 60  # Specify the desired duration in seconds
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'


    cnn = M5(n_input=1, n_output=4).to(DEVICE)
    state_dict = torch.load("M5_best.pth.tar")
    
    cnn.load_state_dict(state_dict["state_dict"])

    preprocessed_signal = preprocess_audio_file(audio_file_path, TARGET_SAMPLE_RATE, NUM_SAMPLES, DURATION, DEVICE)

    # make an inference
    predicted = predict(cnn, preprocessed_signal,class_mapping,DEVICE)
    print(f"Predicted: {predicted}")