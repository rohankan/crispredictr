from matplotlib import pyplot as plt
import numpy as np

with open('asdfasdf.txt', 'r') as f:
    print('starting')
    distances = eval(f.read())
print('done')

print(len([x for x in distances if x > 40.7482683304266]))
raise yo


counts = [4630082, 6982786, 4317972, 1667816, 129654]
counts = [x for x in counts]
bins = [0, 24.02294375, 48.0458875, 72.06883125, 96.09177501, 120.11471876]

distances = [
    *(0 for _ in range(counts[0])),
    *(25 for _ in range(counts[1])),
    *(49 for _ in range(counts[2])),
    *(73 for _ in range(counts[3])),
    *(120 for _ in range(counts[4]))
]


plt.xlabel('DNA Edit Difference (Euclidean Distance)')
plt.ylabel('Number of Occurrences (in millions)')
xticks = np.linspace(0, int(120.11471876), 6)


counts, bins, patches = plt.hist(distances, bins=5)
print(counts, bins, patches)
# plt.axes().set_xlim(0, max(distances))
plt.xticks(xticks)
plt.axes().set_xmargin(10)
import matplotlib.ticker as mtick
def div_10(x, *args):
    """
    The function that will you be applied to your y-axis ticks.
    """
    x = float(x)/1000000
    return "{:.1f}".format(x)
# Apply to the major ticks of the y-axis the function that you defined.
ax = plt.gca()
ax.yaxis.set_major_formatter(mtick.FuncFormatter(div_10))


plt.axvline(x=40.7482683304266,  linestyle='dashed', color = 'black')
plt.text(42.5, 3500000, 'Average Distance', rotation=90, verticalalignment='center')

plt.savefig('asdf.png')
