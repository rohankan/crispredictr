import pandas as pd
import pickle
import sys
import os


args = sys.argv[1:]
query = args[0] if len(args) > 0 else 'RL384-00024_F14.pickle'


file = next(
    os.path.join('data_points', x)
    for x in os.listdir('data_points')
    if x.endswith('.pickle') and query in x
)


with open(file, 'rb') as f:
    dp = pickle.load(f)  # Data Point


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
