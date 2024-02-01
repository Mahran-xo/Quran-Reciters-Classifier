import torchaudio
import torch

def preprocess_audio_file(audio_file_path,target_sample_rate, num_samples, duration ,device):
    # Load the audio file
    signal, sr = torchaudio.load(audio_file_path)

    # Convert to the target device
    signal = signal.to(device)

    # Resample if necessary
    if sr != target_sample_rate:
        resampler = torchaudio.transforms.Resample(sr, target_sample_rate).to(device)
        signal = resampler(signal)

    # Mix down if necessary
    if signal.shape[0] > 1:
        signal = torch.mean(signal, dim=0, keepdim=True)

    # Cut if necessary
    if signal.shape[1] > num_samples:
        signal = signal[:, :num_samples]

    # Right pad if necessary
    length_signal = signal.shape[1]
    if length_signal < num_samples:
        num_missing_samples = num_samples - length_signal
        last_dim_padding = (0, num_missing_samples)
        signal = torch.nn.functional.pad(signal, last_dim_padding)


    return signal
