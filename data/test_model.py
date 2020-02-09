from constants import INDEL_RANGE, SEQUENCE_MAPPER
from matplotlib import pyplot as plt
from pprint import pprint
import numpy as np
import pickle
import os

MODELS_DIR = 'models'
MODEL_NAME = '2020_02_09-18_01_38-rf_model.pickle'
SEQUENCE = 'GATAAGTAGCTGATACTGCCAGCATCTGTTTACTGGCAGGCAAGGAAGAATAAATCCAAC'  # 60 bp long, 33-35 bp inclusive is PAM

if len(SEQUENCE) != 60:
    raise ValueError('SEQUENCE has to be of length 60 base pairs!')

model_path = os.path.join(MODELS_DIR, MODEL_NAME)

with open(model_path, mode='rb') as f:
    model = pickle.load(f)

pam_first_nucleotide = SEQUENCE_MAPPER(SEQUENCE[33])
neighborhood = SEQUENCE_MAPPER(SEQUENCE)
initial_input = [*pam_first_nucleotide, *neighborhood]

predictions = {
    indel: model.predict(np.array(initial_input + [indel]).reshape((1, -1)))[0]
    for indel in INDEL_RANGE
}

print('Predicted:')
pprint(predictions)

xs = list(predictions.keys())
plt.bar(xs, [predictions[x] for x in xs])
plt.show()
