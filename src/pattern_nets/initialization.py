from random import randint

from src.buildingblocks.pattern import Pattern
from src import helpers as common


def initialize_patterns(count: int) -> [Pattern]:
    """ Creates patterns randomly.
        Note that the probability distribution for generating
        patterns are:
          - Average number of layers: 3.02
          - Average number of connections: 1.04
    """
    patterns = []

    for i in range(count):
        # Creating pattern randomly, starting with settings:
        dimension = "1D" if i < int((count-1)/2) else "2D"
        layer_count = randint(2, 4)
        pattern = Pattern(type=dimension, layers=layer_count)

        # Randomly create operations for pattern:
        ops = common.operators1D_votes if pattern.type == "1D" else common.operators2D_votes
        pattern.children += [ops[randint(0, len(ops) - 1)]() for _ in range(pattern.layers)]

        # Randomly connect the operations selected above
        set_random_connections(pattern)

        patterns += [pattern]
    return patterns


def set_random_connections(pattern):
    # Setting internal connections:
    chosen_connections = randint(0, pattern.layers - 1)
    for _ in range(chosen_connections):
        pool = [c for c in pattern.children]
        op1 = pool.pop(randint(0, len(pool) - 1))
        op2 = pool[0] if len(pool) == 1 else pool[randint(0, len(pool) - 2)]
        op1.connect_to(op2)
