from read_data_point import get_data_points
from data_point import DataPoint
from typing import List
from collections import defaultdict
import csv

MIN_INDEL = -30
MAX_INDEL = +5

INDEL_RANGE = list(range(MIN_INDEL, MAX_INDEL+1))

DATA_POINTS_DIR = '../data/data_points/'
CSV_FILE = 'cleaned_data_points.csv'
MIN_TOTAL_READS = 500

data_points: List[DataPoint] = list(get_data_points())

# This adds together all the percentages of each indel in a data point.

with open(CSV_FILE, mode='w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['PAM First Nucleotide', 'Neighborhood', 'Events'])

    cleaned_data_points = (x for x in data_points if x.total_reads >= MIN_TOTAL_READS)
    for dp in cleaned_data_points:
        pam_first_nucleotide: str = dp.pam_site[0]
        neighborhood: str = dp.neighborhood

        indels = defaultdict(int)
        for event in dp.events:
            indels[event.indel] += event.percentage * 100

        delimited_indel_values = '|'.join(str(round(indels[x], 2)) for x in INDEL_RANGE)

        writer.writerow([pam_first_nucleotide, neighborhood, delimited_indel_values])
