import numpy as np
from tensorflow import keras

# Preparing data:
TRAINING_CASES = 45000
(x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()
x_val = x_train[TRAINING_CASES:] / 255
y_val = keras.utils.to_categorical(y_train[TRAINING_CASES:], num_classes=10)
x_train = x_train[:TRAINING_CASES] / 255
y_train = keras.utils.to_categorical(y_train[:TRAINING_CASES], num_classes=10)
x_test = x_test / 255


def get_training_data() -> (np.ndarray, np.ndarray):
    return x_train, y_train


def get_validation_data() -> (np.ndarray, np.ndarray):
    return x_val, y_val


def get_test_data() -> (np.ndarray, np.ndarray):
    return x_test, y_test


