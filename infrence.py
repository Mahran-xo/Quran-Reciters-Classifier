import torch
import torchaudio
from utils import preprocess_audio_file
import os
from model import M5
from train import  SAMPLE_RATE, NUM_SAMPLES

class_mapping = sorted(os.listdir("data"))


def predict(model, input,class_mapping):
    model.eval()
    with torch.no_grad():
        input.unsqueeze_(0)
        predictions = model(input)
        # Tensor (1, 10) -> [ [0.1, 0.01, ..., 0.6] ]
        predicted_index = predictions.argmax(dim=-1)
        predicted = class_mapping[predicted_index]
    return predicted


if __name__ == "__main__":
    print(class_mapping)
    # load back the model
    cnn = M5(n_input=1, n_output=4)
    state_dict = torch.load("M5.pth",map_location=torch.device('cpu'))
    cnn.load_state_dict(state_dict)

    # load urban sound dataset dataset
    # mel_spectrogram = torchaudio.transforms.MelSpectrogram(
    #     sample_rate=SAMPLE_RATE,
    #     n_fft=1024,
    #     hop_length=512,
    #     n_mels=64
    # )
    audio_file_path = "Qari Alaa Aqil Surah Al Fatiha  Best Quran Voice   سورة الفاتحة القارئ علاء عقل.mp3"
    TARGET_SAMPLE_RATE = 8000
    NUM_SAMPLES = 8000
    DURATION = 30  # Specify the desired duration in seconds
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

    preprocessed_signal = preprocess_audio_file(audio_file_path, TARGET_SAMPLE_RATE, NUM_SAMPLES, DURATION, DEVICE)

    

    # make an inference
    predicted = predict(cnn, preprocessed_signal,class_mapping)
    print(f"Predicted: {predicted}")