from typing import List, Dict
import numpy as np


# Resources:
# https://www.kaggle.com/thomasnelson/working-with-dna-sequence-data-for-ml


# DNA sequence encoding methods:
def atcg_to_one_hot(base: str) -> List[int]:
    if base == 'A':
        return [1, 0, 0, 0]
    elif base == 'T':
        return [0, 1, 0, 0]
    elif base == 'C':
        return [0, 0, 1, 0]
    elif base == 'G':
        return [0, 0, 0, 1]

    return [0, 0, 0, 0]


def sequence_to_one_hots(sequence: str) -> np.ndarray:
    return np.array([y for x in sequence for y in atcg_to_one_hot(x)])


ATCG_TO_NUMBER: Dict[str, int] = {'A': 0, 'T': 1, 'C': 2, 'G': 3}


def sequence_to_ordinals(sequence: str) -> np.ndarray:
    return np.array([ATCG_TO_NUMBER[x] for x in sequence])
