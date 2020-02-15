from processing import sequence_to_one_hots, sequence_to_ordinals
from typing import Union, Tuple
import pandas as pd
import numpy as np
from constants import INDEL_RANGE
import itertools

SPROUT_PATH = './cleaned_data_points.csv'


def csv_events_to_numpy_array(csv_events):
    return np.array([float(x) for x in csv_events.split('|')])


def load_sprout(one_hot_atcg: bool = False,
                as_numpy: bool = True) -> Union[Tuple[np.ndarray, np.ndarray], Tuple[pd.DataFrame, pd.DataFrame]]:
    df = pd.read_csv(SPROUT_PATH)

    atcg_mapping = sequence_to_one_hots if one_hot_atcg else sequence_to_ordinals
    df['PAM First Nucleotide'] = df['PAM First Nucleotide'].apply(atcg_mapping)
    df['Neighborhood'] = df['Neighborhood'].apply(atcg_mapping)

    features = df[['PAM First Nucleotide', 'Neighborhood', 'Indel']]
    output = df['Percentage']

    if as_numpy:
        flat_features = [
            [*x['PAM First Nucleotide'], *x['Neighborhood'], x['Indel']]
            for i, x in features.iterrows()
        ]
        return np.array(flat_features), np.array(output)
    else:

        return features, output


Output = Union[Tuple[np.ndarray, np.ndarray], Tuple[pd.DataFrame, pd.DataFrame]]


def load_sprout_multi_output(one_hot_atcg: bool = False,
                             as_numpy: bool = True) -> Output:
    df = pd.read_csv(SPROUT_PATH)

    atcg_mapping = sequence_to_one_hots if one_hot_atcg else sequence_to_ordinals

    from collections import defaultdict
    indels = defaultdict(dict)

    for i, x in df.iterrows():
        indels[x['Neighborhood']][x['Indel']] = x['Percentage']

    features = []
    outputs = []

    for neighborhood, indel_dict in indels.items():
        features.append([*atcg_mapping(neighborhood[33]), *atcg_mapping(neighborhood)])
        outputs.append([indel_dict[x] for x in INDEL_RANGE])

    if as_numpy:
        return np.array(features), np.array(outputs)
    else:
        return features, outputs
