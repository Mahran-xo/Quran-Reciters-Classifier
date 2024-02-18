import autokeras as ak
import tensorflow as tf
import keras

class ResizingBlock(ak.Block):
    """
    Resizing Block implemented from keras.layers.Resizing
    """
    def build(self, hp, inputs=None):
        # Get the input_node from inputs.
        input_node = inputs[0]
        layer = keras.layers.Resizing(
            target_height=hp.Int("height", min_value=32, max_value=1024, step=16),
            target_width=hp.Int("width", min_value=32, max_value=1024, step=16)
        )
        output_node = layer(input_node)
        return output_node