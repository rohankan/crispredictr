from sklearn.model_selection import train_test_split
from constants import RANDOM_STATE, MODEL
from datasets import load_sprout, load_sprout_multi_output
from datetime import datetime
import pickle
import os

print(f'Training with {MODEL.name} model!')

sprout_data, sprout_target = load_sprout_multi_output(as_numpy=True)

print('Finished loading SPROUT!')

X_train, X_test, y_train, y_test = train_test_split(
    sprout_data, sprout_target, train_size=0.9, test_size=0.1, random_state=RANDOM_STATE
)

# bases = {0: 'A', 1: 'T', 2: 'C', 3: 'G'}
#
# for row, output in zip(X_test, y_test):
#     # print(row[-1], output)
#     if row[-1] == 0 or output < 30:
#         continue
#
#     seq = row[1:-1]
#     print(len(seq))
#     letters = ''.join(bases[x] for x in seq)
#
#     print(letters)
#     if letters == 'CAGGCCCAGATGAAGTGCGTGCATGGACCATCAGGGTAAGATTCATACTTATTCATCAGC':
#         raise yo
# print("did it")
# raise yo



print('Split into training and validation sets.')

if MODEL.preprocess_X is not None:
    print('Preprocessing X_train.')
    X_train = MODEL.preprocess_X(X_train)

model = MODEL.model
print('Training model.')
model.fit(X_train, y_train)

print('Finished fitting and training!')

folder = datetime.now().strftime('./models/%Y_%m_%d-%H_%M_%S/')
os.mkdir(folder)

filename = folder + f'{MODEL.shorthand}_model.pickle'

with open(filename, mode='wb') as f:
    pickle.dump(model, f)
    print('Saved model!')


filename = folder + f'{MODEL.shorthand}_data.txt'
training = f'Training R^2: {model.score(X_train, y_train)}'
testing = f'Test R^2: {model.score(X_test, y_test)}'

with open(filename, mode='w') as f:
    f.write(training + '\n')
    f.write(testing)

print(training)
print(testing)
