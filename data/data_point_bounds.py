from read_data_point import get_data_points
from data_point import DataPoint
from collections import defaultdict
from typing import List
from pprint import pprint
from matplotlib import pyplot as plt
import csv

DATA_POINTS_DIR = '../data/data_points/'
CSV_FILE = 'cleaned_data_points.csv'
MIN_TOTAL_READS = 500

data_points: List[DataPoint] = list(get_data_points())

min_indel = 100000
max_indel = -100000

# This adds together all the percentages of each indel in a data point.

with open(CSV_FILE, mode='w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['PAM First Nucleotide', 'Neighborhood', 'Events'])

    counts = defaultdict(int)

    cleaned_data_points = (x for x in data_points if x.total_reads >= MIN_TOTAL_READS)
    for dp in cleaned_data_points:
        for x in dp.events:
            counts[x.indel] += int(x.percentage * 100)
        min_indel = min(min_indel, min(x.indel for x in dp.events))
        max_indel = max(max_indel, max(x.indel for x in dp.events))

print(f'Min indel: {min_indel}')
print(f'Max indel: {max_indel}')
pprint(counts)

plt.bar(list(counts.keys()), list(counts.values()))
plt.show()

