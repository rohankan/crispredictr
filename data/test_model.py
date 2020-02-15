from constants import INDEL_RANGE, SEQUENCE_MAPPER
from matplotlib import pyplot as plt
from pprint import pprint
import numpy as np
import pickle
import os

# Bugs in decodr (gata cleaned files folder) with gRNA: CCTCGCAGGTTAATCCCCAG.

IS_MULTI_OUTPUT = True
MODELS_DIR = 'models'
MODELS_DATE = '2020_02_13-23_48_12'
SEQUENCE = 'AGAGGTGGAGGAAGACCTGGGCCGTGCTCTACCCGGCCAGTCCCCACGGCGTAGCGCGGC'  # 60 bp long, 33-35 bp inclusive is PAM

MODEL_NAME = next(x for x in os.listdir(os.path.join(MODELS_DIR, MODELS_DATE)) if x.endswith('.pickle'))

if len(SEQUENCE) != 60:
    raise ValueError('SEQUENCE has to be of length 60 base pairs!')

MODELS_DIR = os.path.join(MODELS_DIR, MODELS_DATE)
model_path = os.path.join(MODELS_DIR, MODEL_NAME)

with open(model_path, mode='rb') as f:
    model = pickle.load(f)

pam_first_nucleotide = SEQUENCE_MAPPER(SEQUENCE[33])
neighborhood = SEQUENCE_MAPPER(SEQUENCE)
initial_input = [*pam_first_nucleotide, *neighborhood]

if IS_MULTI_OUTPUT:
    predictions = {
        indel: prediction
        for indel, prediction in zip(INDEL_RANGE, model.predict(np.array(initial_input).reshape((1, -1)))[0])
    }
else:
    predictions = {
        indel: model.predict(np.array(initial_input + [indel]).reshape((1, -1)))[0]
        for indel in INDEL_RANGE
    }

print('Predicted:')
pprint(predictions)

xs = list(predictions.keys())
plt.bar(xs, [predictions[x] for x in xs])
plt.show()
