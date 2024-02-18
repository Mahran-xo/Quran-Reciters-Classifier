import autokeras as ak
import tensorflow as tf
import train_utils as cb
from train_utils import (
    stereo_to_mono_converter,
    squeeze,
    get_spectrogram
)




class SoundClf(ak.AutoModel):
    def build(self,inputs):
        # Apply your data processing pipeline to the inputs
        x, y = inputs
        x = stereo_to_mono_converter(x, y)
        x = squeeze(x, y)
        x = get_spectrogram(x)
        input = ak.ImageInput()
        resize = cb.ResizingBlock()(input)
        norm_layer = ak.Normalization()(resize)
        conv1 = ak.ConvBlock()(norm_layer)
        conv2 = ak.ConvBlock()(conv1)
        conv3 = ak.ConvBlock()(conv2)
        res = ak.ResNetBlock(version="v2")(norm_layer)
        merge = ak.Merge()[conv3,res]
        conv4 = ak.ConvBlock()(merge)
        output = ak.ClassificationHead(num_classes=len(y))(conv4)
        #TODO: use __assemble__ method
        auto_model = ak.AutoModel(
            inputs=input, outputs=output, overwrite=True, max_trials=1
        )
        return auto_model(x)

train_ds, val_ds = tf.keras.utils.audio_dataset_from_directory(
    directory="quran",
    batch_size=128,
    output_sequence_length=16000,
    validation_split=0.2,
    seed=0,
    subset='both')

train_ds = train_ds.map(stereo_to_mono_converter, tf.data.AUTOTUNE)
val_ds = val_ds.map(stereo_to_mono_converter, tf.data.AUTOTUNE)
train_ds = train_ds.map(squeeze, tf.data.AUTOTUNE)
val_ds = val_ds.map(squeeze, tf.data.AUTOTUNE)

clf = SoundClf()

clf.fit(
    inputs=spectrogram_module,
    outputs=ak.ClassificationHead(num_classes=len(np.unique(y)), loss_function='sparse_categorical_crossentropy'),
    overwrite=True,  # Set to True if you want to re-initialize the model architecture
    max_trials=3,  # Adjust as needed
)

def model():
    """
    input_shape = example_spectrograms.shape[1:]
    print('Input shape:', input_shape)
    num_labels = len(label_names)

    norm_layer = layers.Normalization()
    norm_layer.adapt(data=train_spectrogram_ds.map(map_func=lambda spec, label: spec))

    model = models.Sequential([
    layers.Input(shape=input_shape),
    layers.Resizing(64, 64),
    norm_layer,
    layers.Conv2D(64, 3, activation='relu'),
    layers.Conv2D(64, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Dropout(0.25),
    
    layers.Conv2D(128, 3, activation='relu'),
    layers.Conv2D(128, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Dropout(0.25),
    
    layers.Conv2D(256, 3, activation='relu'),
    layers.Conv2D(256, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Dropout(0.25),
    
    layers.Flatten(),
    layers.Dense(512, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(num_labels),
])
    """


def prep():
    """
import autokeras as ak
import tensorflow as tf
import numpy as np

# Your data loading and preprocessing functions
def stereo_to_mono_converter(example, labels):
    audio = example
    audio = tf.reduce_mean(audio, axis=-1, keepdims=True)
    return audio, labels

def squeeze(audio, labels):
    audio = tf.squeeze(audio, axis=-1)
    return audio, labels

def get_spectrogram(waveform):
    spectrogram = tf.signal.stft(
        waveform, frame_length=255, frame_step=128)
    spectrogram = tf.abs(spectrogram)
    spectrogram = spectrogram[..., tf.newaxis]
    return spectrogram

def make_spec_ds(ds):
    return ds.map(
        map_func=lambda audio, label: (get_spectrogram(audio), label),
        num_parallel_calls=tf.data.AUTOTUNE)

# Define the AutoKeras module
class SpectrogramModule(ak.Module):
    def build(self, hp, inputs):
        # Apply your data processing pipeline to the inputs
        x, y = inputs
        x = stereo_to_mono_converter(x, y)
        x = squeeze(x, y)
        x = get_spectrogram(x)

        # Build the AutoKeras model
        clf = ak.ImageClassifier(
            num_classes=len(np.unique(y)),
            input_shape=x.shape[1:],  # Shape of the spectrogram
            **hp
        )

        # Return the AutoKeras model
        return clf(x)

# Your data loading
train_ds, val_ds = tf.keras.utils.audio_dataset_from_directory(
    directory="quran",
    batch_size=128,
    output_sequence_length=16000,
    validation_split=0.2,
    seed=0,
    subset='both')

# Your data preprocessing
train_ds = train_ds.map(stereo_to_mono_converter, tf.data.AUTOTUNE)
val_ds = val_ds.map(stereo_to_mono_converter, tf.data.AUTOTUNE)
train_ds = train_ds.map(squeeze, tf.data.AUTOTUNE)
val_ds = val_ds.map(squeeze, tf.data.AUTOTUNE)

# Create the AutoKeras module instance
spectrogram_module = SpectrogramModule()

# Use the module in AutoKeras
clf = ak.AutoModel(
    inputs=spectrogram_module,
    outputs=ak.ClassificationHead(num_classes=len(np.unique(y)), loss_function='sparse_categorical_crossentropy'),
    overwrite=True,  # Set to True if you want to re-initialize the model architecture
    max_trials=3,  # Adjust as needed
)

# Fit the AutoKeras model
clf.fit(
    train_ds,
    epochs=10,  # Adjust as needed
    validation_data=val_ds,
)

# Evaluate the model
results = clf.evaluate(val_ds)
print(results)

    """