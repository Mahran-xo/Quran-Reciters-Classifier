import librosa
import os
import json
from audiomentations import Compose, AddGaussianNoise, TimeStretch, PitchShift, Shift

# Constants
DATASET_PATH = "data"
JSON_PATH = "TF_CNN/data.json"
SAMPLES_TO_CONSIDER = 48000  # 5 seconds at 22.05 kHz

# Augmentations
# augmentations = Compose([
#     AddGaussianNoise(),
#     TimeStretch(),
#     PitchShift(),
#     Shift(),
# ])

def preprocess_dataset(dataset_path, json_path, num_mfcc=13, n_fft=2048, hop_length=512):
    """Extracts MFCCs from the music dataset and saves them into a json file.

    :param dataset_path (str): Path to the dataset
    :param json_path (str): Path to the json file used to save MFCCs
    :param num_mfcc (int): Number of coefficients to extract
    :param n_fft (int): Interval we consider to apply FFT. Measured in # of samples
    :param hop_length (int): Sliding window for FFT. Measured in # of samples
    :return:
    """
    # dictionary where we'll store mapping, labels, MFCCs, and filenames
    data = {
        "mapping": [],
        "labels": [],
        "MFCCs": [],
        "files": []
    }

    # loop through all sub-dirs
    for i, (dirpath, dirnames, filenames) in enumerate(os.walk(dataset_path)):

        # ensure we're at the sub-folder level
        if dirpath is not dataset_path:

            # save label (i.e., sub-folder name) in the mapping
            label = dirpath.split("/")[-1]
            data["mapping"].append(label)
            print("\nProcessing: '{}'".format(label))

            # process all audio files in sub-dir and store MFCCs
            for f in filenames:
                file_path = os.path.join(dirpath, f)

                # load audio file and slice it to ensure length consistency among different files
                signal, sample_rate = librosa.load(file_path)

                # drop audio files with less than pre-decided number of samples
                if len(signal) >= SAMPLES_TO_CONSIDER:

                    # ensure consistency of the length of the signal
                    signal = signal[:SAMPLES_TO_CONSIDER]

                    # apply augmentations
                    # augmented_signal = augmentations(samples=signal, sample_rate=sample_rate)

                    # extract MFCCs from the augmented signal
                    MFCCs = librosa.feature.mfcc(y=signal, sr=sample_rate, n_mfcc=num_mfcc, n_fft=n_fft, hop_length=hop_length)

                    # store data for the analyzed track
                    data["MFCCs"].append(MFCCs.T.tolist())
                    data["labels"].append(i - 1)
                    data["files"].append(file_path)
                    print("{}: {}".format(file_path, i - 1))

    # save data in json file
    with open(json_path, "w") as fp:
        json.dump(data, fp, indent=4)


if __name__ == "__main__":
    preprocess_dataset(DATASET_PATH, JSON_PATH)