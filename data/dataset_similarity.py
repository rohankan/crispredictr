from data_point import data_point_to_read_vector
from matplotlib import pyplot as plt
import numpy as np
import random
from read_data_point import get_data_points
from data_point import DataPoint
from typing import List
from collections import defaultdict
import csv


def heatmap(data, row_labels, col_labels, ax=None, cbar_kw={}, cbarlabel="", **kwargs):
    # https://matplotlib.org/3.1.1/gallery/images_contours_and_fields/image_annotated_heatmap.html
    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    print(kwargs)
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # We want to show all ticks...
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-55, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=0)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


MIN_INDEL = -30
MAX_INDEL = +5

INDEL_RANGE = list(range(MIN_INDEL, MAX_INDEL+1))

DATA_POINTS_DIR = '../data/data_points/'
MIN_TOTAL_READS = 500

# print(np.linalg.norm(np.array([1, 2,3 ,4 ,3,3,3,3,3,3,3,3,3,3,])))

data_points = list(get_data_points())
cleaned_data_points = (x for x in data_points if x.total_reads >= MIN_TOTAL_READS)
full_heatmap_points = []

for dp in cleaned_data_points:
    pam_first_nucleotide: str = dp.pam_site[0]
    neighborhood: str = dp.neighborhood

    indels = defaultdict(int)
    cleaned_events = (x for x in dp.events if MIN_INDEL <= x.indel <= MAX_INDEL)
    for event in cleaned_events:
        indels[event.indel] += event.percentage * 100

    full_heatmap_points.append((dp.file_name, np.array([indels[x] for x in INDEL_RANGE])))


# for _, x in full_heatmap_points:
#     for _, y in full_heatmap_points:
#         val = np.linalg.norm(x - y)
#
#         if val > 50:
#             print(list(x))
#             print(list(y))
#             raise yo

heatmap_points = random.sample(full_heatmap_points, k=20)

euclidean_distances = np.array([
    [np.linalg.norm(x - y) for _, y in heatmap_points]
    for _, x in heatmap_points
])

distances = [y for x in euclidean_distances for y in x]

names = [name for name, _ in heatmap_points]
num_points = len(heatmap_points)

fig, ax = plt.subplots()

heatmap(euclidean_distances, names, names, ax=ax, cmap="viridis", cbarlabel="DNA Edit Difference (Euclidean Distance)",
        interpolation='nearest')
# ax.imshow(euclidean_distances, cmap='viridis', interpolation='nearest')

ax.set_xticks(np.arange(num_points))
ax.set_yticks(np.arange(num_points))
ax.set_xticklabels(names)
ax.set_yticklabels(names)

# plt.show(bbox_inches='tight')
plt.savefig('testing.png', bbox_inches='tight')

from scipy import stats

print(f'Max: {max(distances)}')
print(f'Average: {sum(distances) / len(distances)}')
print(stats.describe(distances))
print()
# print([])

plt.figure()
#
# distances = []
# for i, (_, x) in enumerate(full_heatmap_points):
#     for j, (_, y) in enumerate(full_heatmap_points):
#         if i == j:
#             continue
#
#         distances.append(np.linalg.norm(x - y))
#
# with open('asdfasdf.txt', 'w') as f:
#     f.write(str(distances))
#
#     # print(f'{i} / {len(full_heatmap_points)}')
#
# # We can set the number of bins with the `bins` kwarg
# plt.hist(distances, bins=5)
# plt.axes().set_xlim(0, max(distances))
# plt.axes().set_xmargin(10)
#
# vlines = [sum(distances) / len(distances)]
# plt.axvline(x=vlines,  linestyle='dashed', color = 'black')
# plt.text(vlines[0], 100, 'Average Distance', rotation=90, verticalalignment='center')
#
#
# plt.savefig('asdf.png')
