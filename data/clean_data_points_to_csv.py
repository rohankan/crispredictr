from read_data_point import get_data_points
from constants import MIN_INDEL, MAX_INDEL
from data_point import DataPoint
from typing import List
from collections import defaultdict
import csv

MIN_INDEL = -30
MAX_INDEL = +5

INDEL_RANGE = list(range(MIN_INDEL, MAX_INDEL+1))

DATA_POINTS_DIR = '../data/data_points/'
CSV_FILE = 'named_cleanedf_data_points.csv'
MIN_TOTAL_READS = 500

data_points: List[DataPoint] = list(get_data_points())

# This adds together all the percentages of each indel in a data point.

with open(CSV_FILE, mode='w') as csv_file:
    # writer = csv.writer(csv_file)
    # writer.writerow(['Name', 'PAM First Nucleotide', 'Neighborhood', 'Indel', 'Percentage'])

    cleaned_data_points = (x for x in data_points if x.total_reads >= MIN_TOTAL_READS)
    for dp in cleaned_data_points:
        pam_first_nucleotide: str = dp.pam_site[0]
        neighborhood: str = dp.neighborhood

        indels = defaultdict(int)
        cleaned_events = (x for x in dp.events if MIN_INDEL <= x.indel <= MAX_INDEL)
        for event in cleaned_events:
            indels[event.indel] += event.percentage * 100

        # for indel, percentage in indels.items():
        #     writer.writerow([pam_first_nucleotide, neighborhood, indel, percentage])

        # for indel in INDEL_RANGE:
        #     writer.writerow([dp.name, pam_first_nucleotide, neighborhood, indel, indels[indel]])

        if neighborhood == 'AGAGGTGGAGGAAGACCTGGGCCGTGCTCTACCCGGCCAGTCCCCACGGCGTAGCGCGGC':
            print([indels[indel] for indel in INDEL_RANGE])
            raise yo
