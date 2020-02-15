from constants import INDEL_RANGE, SEQUENCE_MAPPER
from matplotlib import pyplot as plt
from pprint import pprint
import numpy as np
import pickle
import os

import matplotlib.gridspec as gridspec

y_correct = np.array([0, 0, 0.4628156547395216, 0.11425761476381939, 0.3630210291863122, 0, 0, 0, 0, 0.7462902432674785, 0, 0, 0, 0.49318793208180267, 6.6385120476700115, 4.207283561366463, 0.4237655838708745, 0, 0, 1.15125394116456, 1.42460443724509, 0.0896705331057823, 0.12872060397442944, 0.07231494605305025, 0.5235602094240838, 2.017586994880102, 1.9091145758005266, 2.743629053252726, 4.178357582945243, 9.667061988371758, 5.024442451765931, 47.33591738740563, 1.1469150444013767, 0, 0, 0])

gs1 = gridspec.GridSpec(4, 4)
gs1.update(wspace=0.1, hspace=0.15)

# Bugs in decodr (gata cleaned files folder) with gRNA: CCTCGCAGGTTAATCCCCAG.

MODELS_DIR = 'models'
MODELS_DATE = '2020_02_13-18_39_40'
SEQUENCE = 'AGAGGTGGAGGAAGACCTGGGCCGTGCTCTACCCGGCCAGTCCCCACGGCGTAGCGCGGC'  # 60 bp long, 33-35 bp inclusive is PAM

TESTS = [
    ('/Users/rohankanchana/Programming/Crispredictr/data/models/2020_02_09-18_01_38/2020_02_09-18_01_38-rf_model.pickle',
     'Random Forest', False),
    ('/Users/rohankanchana/Programming/Crispredictr/data/models/2020_02_13-18_14_33/mlp_model.pickle',
     'Multilayer Perceptron', False),
    ('/Users/rohankanchana/Programming/Crispredictr/data/models/2020_02_13-17_40_22/knn_model.pickle',
     'k-Nearest Neighbors', False),
    ('/Users/rohankanchana/Programming/Crispredictr/data/models/2020_02_13-23_38_08/lr_model.pickle',
     'Linear Regression', True),
    ('/Users/rohankanchana/Programming/Crispredictr/data/models/2020_02_13-23_48_12/svm_model.pickle',
     'Support Vector Machine', True),
    ('/Users/rohankanchana/Programming/Crispredictr/data/models/2020_02_13-18_39_40/gbr_model.pickle',
     'Gradient Boosting', False),
]

pam_first_nucleotide = SEQUENCE_MAPPER(SEQUENCE[33])
neighborhood = SEQUENCE_MAPPER(SEQUENCE)
initial_input = [*pam_first_nucleotide, *neighborhood]


fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, sharex=True, sharey=True,
                                                       gridspec_kw={'wspace': 0.085, 'hspace': 0.15})
axes = [ax1, ax2, ax3, ax4, ax5, ax6]
TESTS = [(*x, ax) for x, ax in zip(TESTS, axes)]

import matplotlib.patches as mpatches
correct_patch = mpatches.Patch(color='orange', label='Correct output')
model_patch = mpatches.Patch(color=(73/255, 139/255, 189/255), label='Model prediction')
# plt.legend(handles=[correct_patch, model_patch], loc='lower center', bbox_to_anchor=(0, 0), shadow=True, ncol=2)

for ax in fig.get_axes():
    ax.label_outer()

for model_path, model_name, is_multi_output, axis in TESTS:
    with open(model_path, mode='rb') as f:
        model = pickle.load(f)

    ii = list(initial_input)
    if is_multi_output:
        predictions = {
            indel: prediction
            for indel, prediction in zip(INDEL_RANGE, model.predict(np.array(initial_input).reshape((1, -1)))[0])
        }

        r_squared = model.score(np.array(ii).reshape((1, -1)), y_correct.reshape((1, -1)))

        print(str(r_squared))
        if str(r_squared) == 'nan':
            from scipy import stats

            r, _ = stats.pearsonr(np.array([predictions[x] for x in INDEL_RANGE]), y_correct)
            print(r)
            r_squared = r ** 2
    else:
        predictions = {
            indel: model.predict(np.array(initial_input + [indel]).reshape((1, -1)))[0]
            for indel in INDEL_RANGE
        }
        X_input = np.array([
            ii + [indel] for indel in INDEL_RANGE
        ])
        r_squared = model.score(X_input, y_correct)

    print(f'R-squared: {r_squared}')

    print('Predicted:')
    pprint(predictions)

    xs = INDEL_RANGE
    axis.bar(xs, [predictions[x] for x in xs])
    axis.bar(xs, y_correct, color='orange', alpha=0.5)

    print([predictions[x] for x in xs], y_correct)

    spacing = 0.06
    props = dict(boxstyle='Square', facecolor='white', linewidth=0.5)
    axis.text(spacing, 1.07, r'{}, $R^2$ = {}'.format(model_name, round(r_squared, 3)), fontsize=7,
              horizontalalignment='left', verticalalignment='top', bbox=props,
              transform=axis.transAxes)

    if 'Neighbors' in model_name:
        axis.legend(handles=[correct_patch, model_patch], loc='right', bbox_to_anchor=(1, 1.22),  ncol=2)
    # axis.set_title(r'{}, $R^2$ = {}'.format(model_name, round(r_squared, 3)))

fig.add_subplot(111, frameon=False)
# hide tick and tick label of the big axis
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
plt.xlabel('Indel Size (bp)')
plt.ylabel('Indel Abundance (%)')
plt.show()
