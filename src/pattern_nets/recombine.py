import sys

import copy
import random

from src.buildingblocks.module import Module
from src.helpers import randomized_index, shuffle


def combine(patterns, num_nets, min_size, max_size, include_optimal=False):

    all_patterns_used = False
    nets = []
    if include_optimal:
        optimal = combine_optimal(patterns, size=random.randint(min_size, max_size))
        if optimal:
            nets += [optimal]
            draw = shuffle([
                i
                for i, p in enumerate(patterns)
                if not any(p.ID == q.predecessor.ID for q in optimal.patterns)
            ])
        else:
            draw = randomized_index(patterns)
    else:
        draw = randomized_index(patterns)

    for i in range(num_nets):
        # Setup:
        net = Module()

        for _ in range(random.randint(min_size, max_size)):
            # Selecting random patterns:
            pattern, draw = patterns[draw[0]], draw[1:]

            # Adding to net:
            net.children += [copy.deepcopy(pattern)]
            if len(draw) == 0:
                draw = randomized_index(patterns)
                all_patterns_used = True
                break  # --> Cannot use same pattern twice in a network...

        # Placing 2D layers first:
        net.children.sort(key=lambda x: 0 if x.type == "2D" else 1)

        # Connecting patterns together:
        ops = net.connect_all_sub_modules_sequential()

        net.patterns = net.children
        net.children = ops

        # Done
        nets += [net]

    if not all_patterns_used:
        nets += combine([patterns[x] for x in draw], 1, min_size, max_size)

    # Checking for duplicated networks:
    remove_duplicates(nets)
    return nets


def combine_optimal(patterns, size):
    if not all(p.optimal_result() for p in patterns):
        return None

    optimal = Module()
    sorted_patterns = [pattern for pattern in patterns]
    sorted_patterns.sort(
        key=lambda p: p.optimal_result().score(),
        reverse=True
    )

    for i in range(size):
        optimal.children += [copy.deepcopy(sorted_patterns.pop(0))]

    dim2 = [p for p in optimal.children if p.type == "2D"]
    dim2.sort(key=lambda p: p.optimal_result().distance)
    dim1 = [p for p in optimal.children if p.type == "1D"]
    dim1.sort(key=lambda p: p.optimal_result().distance)

    optimal.children = dim2 + dim1
    optimal.patterns = optimal.children
    optimal.children = optimal.connect_all_sub_modules_sequential()

    return optimal


def remove_duplicates(nets):
    duplicates = []
    for net in nets:
        for other_net in nets:
            if net == other_net \
                    or len(net.patterns) != len(other_net.patterns) \
                    or len(net.children) != len(other_net.children):
                continue
            elif all(
                    net.patterns[i].predecessor.ID == other_net.patterns[i].predecessor.ID
                    for i in range(len(net.patterns))
            ):
                duplicates += [net]
    if duplicates:
        duplicates = list(set(duplicates))
        print(f"--> Found {len(duplicates)} duplicates... Deleting...")
        for element in duplicates:
            nets.remove(element)

