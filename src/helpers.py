import random

from src.buildingblocks.ops.convolution import Conv3x3, Conv5x5
from src.buildingblocks.ops.dense import (
    DenseS as DenseSmall,
    DenseM as DenseMedium,
    DenseL as DenseLarge
)
from src.buildingblocks.ops.pooling import MaxPooling2x2, AvgPooling2x2


def system_short_name():
    try:
        import os
        sysname, nodename, release, version, machine = os.uname()
        return nodename.split(".")[0] if "." in nodename else nodename
    except Exception:
        return "?"

def random_sample(collection: list) -> object:
    # Selecting a random operation and creating an instance of it.
    if len(collection) == 1:
        return collection[0]
    return collection[random.randint(0, len(collection) - 1)]


def random_sample_remove(collection: list) -> object:
    # Selecting a random operation and creating an instance of it.
    # Then deletes the sample
    if len(collection) == 1:
        return collection.pop(0)
    index = random.randint(0, len(collection) - 1)
    elem = collection.pop(index)
    return elem


def shuffle(li):
    return [li[i] for i in randomized_index(li)]


def randomized_index(li: [], index_size: int = 0):
    import numpy as np
    index_size = len(li) if index_size == 0 else index_size
    draw = np.arange(len(li))
    np.random.shuffle(draw)
    return draw[:index_size]


def generate_votes(weights: [(object, int)]) -> list:
    """
        Converts a list of (<object>, <votes>)
        :param weights: A list of tuples containing (<object>, <votes>)
    """
    votes = []
    for operation, weight in weights:
        votes += [operation] * weight
    return votes


operators2D = [Conv3x3, Conv5x5, MaxPooling2x2, AvgPooling2x2]
operators1D = [DenseSmall, DenseMedium, DenseLarge]
OPERATORS_2D_WEIGHTS = [
    (Conv3x3, 10),
    (Conv5x5, 10),
    (MaxPooling2x2, 3),
    (AvgPooling2x2, 3),
]

OPERATORS_1D_WEIGHTS = [
    (DenseSmall, 3),
    (DenseMedium, 5),
    (DenseLarge, 7),
    # (Dropout, 5),
]

operators2D_votes = generate_votes(OPERATORS_2D_WEIGHTS)
operators1D_votes = generate_votes(OPERATORS_1D_WEIGHTS)
operators_votes = operators2D_votes # operators1D_votes
registered_modules = []
