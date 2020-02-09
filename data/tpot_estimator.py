from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from datasets import load_sprout
from datetime import datetime
import pickle

RANDOM_STATE = 42

sprout_data, sprout_target = load_sprout(as_numpy=True)

print('Finished loading SPROUT!')

X_train, X_test, y_train, y_test = train_test_split(
    sprout_data, sprout_target, train_size=0.9, test_size=0.1, random_state=RANDOM_STATE
)

print('Split into training and validation sets.')

model = RandomForestRegressor(n_jobs=-1, bootstrap=True, random_state=RANDOM_STATE, verbose=1)
model.fit(X_train, y_train)

filename = datetime.now().strftime('./models/%Y_%m_%d-%H_%M_%S-rf_model.pickle')
with open(filename, mode='wb') as f:
    pickle.dump(model, f)
    print('Saved model!')

print(f'Training R^2: {model.score(X_train, y_train)}')
print(f'Test R^2: {model.score(X_test, y_test)}')
