import torch
import torchaudio
from torch import nn
from torch.utils.data import DataLoader
from tqdm import tqdm
from dataset import UrbanSoundDataset
from model import CNNNetwork

BATCH_SIZE = 128
EPOCHS = 10
LEARNING_RATE = 0.001

ANNOTATIONS_FILE = "data.csv"
AUDIO_DIR = "data"
SAMPLE_RATE = 22050
NUM_SAMPLES = 22050


def create_data_loader(train_data, batch_size):
    train_dataloader = DataLoader(train_data, batch_size=batch_size)
    return train_dataloader


def train_single_epoch(model, data_loader, loss_fn, optimiser, device):
    prog_bar = tqdm(
        data_loader,
        total=len(data_loader),
        bar_format='{l_bar}{bar:20}{r_bar}{bar:-20b}')
    train_loss = 0.0
    train_correct = 0
    cnt = 0

    for idx, (input, target) in enumerate(prog_bar):
        # Unpack elements from the tuple
        # print(f'Type of input: {input}')
        # print(f'Type of target: {target}')
        input, target = input.to(device), target.to(device)

        # calculate loss
        prediction = model(input)
        loss = loss_fn(prediction, target)

        # backpropagate error and update weights
        optimiser.zero_grad()
        loss.backward()
        optimiser.step()

        _, predicted = torch.max(prediction, 1)
        train_loss += loss.item()
        train_correct += (predicted == target).sum().item()

        cnt += 1  # Increment the counter for each batch processed

    train_loss /= cnt  # Normalize the loss by the total number of batches
    train_accuracy = 100 * (train_correct / len(data_loader.dataset))
    print('Train Loss: {:.4f}, Train Accuracy: {:.2f}%'.format(train_loss, train_accuracy))



def train(model, data_loader, loss_fn, optimiser, device, epochs):
    for i in range(epochs):
        print(f"Epoch {i + 1}")
        train_single_epoch(model, data_loader, loss_fn, optimiser, device)
        print("---------------------------")
    print("Finished training")


if __name__ == "__main__":
    if torch.cuda.is_available():
        device = "cuda"
        print(f"Using {device}")
    else:
        device = "cpu"
    print(f"Using {device}")

    # instantiating our dataset object and create data loader
    mel_spectrogram = torchaudio.transforms.MelSpectrogram(
        sample_rate=SAMPLE_RATE,
        n_fft=1024,
        hop_length=512,
        n_mels=64
    )

    usd = UrbanSoundDataset(ANNOTATIONS_FILE,
                            AUDIO_DIR,
                            mel_spectrogram,
                            SAMPLE_RATE,
                            NUM_SAMPLES,
                            device)

    train_dataloader = create_data_loader(usd, BATCH_SIZE)

    # construct model and assign it to device
    cnn = CNNNetwork().to(device)
    print(cnn)

    # initialise loss funtion + optimiser
    loss_fn = nn.CrossEntropyLoss()
    optimiser = torch.optim.Adam(cnn.parameters(),
                                 lr=LEARNING_RATE)

    # train model
    train(cnn, train_dataloader, loss_fn, optimiser, device, EPOCHS)

    # save model
    torch.save(cnn.state_dict(), "feedforwardnet.pth")
    print("Trained feed forward net saved at feedforwardnet.pth")