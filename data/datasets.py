from processing import sequence_to_one_hots, sequence_to_ordinals
from typing import Union, Tuple
import pandas as pd
import numpy as np
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
