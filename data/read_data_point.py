from data_point import DataPoint
from typing import Optional, Iterable
import pandas as pd
import pickle
import sys
import os


def read_data_point_from_file(*,
                              full_path: Optional[str] = None,
                              file_name: Optional[str] = None) -> DataPoint:
    if (full_path is None) == (file_name is None):
        raise ValueError('Either full_path or file_name have to be filled!')

    file = os.path.join('data_points', file_name) if (full_path is None) else full_path

    with open(file, 'rb') as f:
        data_point = pickle.load(f)  # Data Point

    return data_point


def get_data_points() -> Iterable[DataPoint]:
    return (read_data_point_from_file(file_name=x) for x in os.listdir('data_points') if x.endswith('.pickle'))


if __name__ == '__main__':
    args = sys.argv[1:]
    query = args[0] if len(args) > 0 else 'RL384-00024_F14.pickle'
    file = next(x for x in os.listdir('data_points') if x.endswith('.pickle') and query in x)

    dp = read_data_point_from_file(file_name=file)

    os.system(f'open ../data/SPROUT/pdfs/{dp.file_name}.pdf')
    os.system(f'open ../data/SPROUT/counts/counts-{dp.file_name}.txt')

    print('Name:', dp.name)
    print('General File Name:', dp.file_name)

    print('Guide RNA:', dp.guide_rna)
    print('PAM Site:', dp.pam_site)
    print('Neighborhood:', dp.neighborhood)
    print('Cut Site:', dp.cut_site)

    print('Total Reads:', dp.total_reads)
    print('Events:')

    df = pd.DataFrame(
        data={
            'Indel Start': [x.indel_start for x in dp.events],
            'Indel': [x.indel for x in dp.events],
            'Number of Reads': [x.num_reads for x in dp.events],
            'Percentage': [x.percentage * 100 for x in dp.events]
        }
    )

    print(df.to_string())
