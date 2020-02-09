from processing import sequence_to_one_hots, sequence_to_ordinals
import pandas as pd
import numpy as np


SPROUT_PATH = './cleaned_data_points.csv'


def csv_events_to_numpy_array(csv_events):
    return np.array([float(x) for x in csv_events.split('|')])


def load_sprout(one_hot_atcg: bool = False) -> pd.DataFrame:
    df = pd.read_csv(SPROUT_PATH)
    df['Events'] = df['Events'].apply(csv_events_to_numpy_array)

    atcg_mapping = sequence_to_one_hots if one_hot_atcg else sequence_to_ordinals
    df['PAM First Nucleotide'] = df['PAM First Nucleotide'].apply(lambda x: atcg_mapping(x)[0])
    df['Neighborhood'] = df['Neighborhood'].apply(atcg_mapping)

