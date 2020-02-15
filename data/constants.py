from processing import sequence_to_one_hots, sequence_to_ordinals
<<<<<<< HEAD
from typing import List, Callable, Any, NamedTuple, Dict, Optional
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, BayesianRidge
from sklearn.kernel_approximation import Nystroem
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.multioutput import MultiOutputRegressor
=======
from typing import List, Callable, Any, NamedTuple, Dict
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, BayesianRidge
>>>>>>> 62e20d9f88eb1bcd497e60ecef9c8c0beb73207e
from sklearn import svm


MIN_INDEL: int = -30
MAX_INDEL: int = +5


INDEL_RANGE: List[int] = list(range(MIN_INDEL, MAX_INDEL+1))


SEQUENCE_MAPPER: Callable[[str], Any] = sequence_to_ordinals


RANDOM_STATE: int = 42


# Model with method 'fit(X, y)'
<<<<<<< HEAD
Model = NamedTuple('Model', [('name', str), ('model', Any), ('shorthand', str), ('preprocess_X', Optional[Callable])])

mlp = MLPRegressor(hidden_layer_sizes=(100, 100, 100, 100, 100, 100), solver='lbfgs', max_iter=50, verbose=True)
mlp.n_layers_ = 8


# feature_map_nystroem = Nystroem(gamma=.2, random_state=1, n_components=10000)
=======
Model = NamedTuple('Model', [('name', str), ('model', Any), ('shorthand', str)])
>>>>>>> 62e20d9f88eb1bcd497e60ecef9c8c0beb73207e


MODELS: Dict[str, Model] = {
    'RandomForest': Model(
        name='Random Forest',
        model=RandomForestRegressor(n_jobs=-1, bootstrap=True, random_state=RANDOM_STATE, verbose=1),
<<<<<<< HEAD
        shorthand='rf',
        preprocess_X=None
    ),
    'LinearRegression': Model(
        name='Linear Regression',
        model=MultiOutputRegressor(LinearRegression(), n_jobs=-1),
        shorthand='lr',
        preprocess_X=None
=======
        shorthand='rf'
    ),
    'LinearRegression': Model(
        name='Linear Regression',
        model=LinearRegression(n_jobs=-1),
        shorthand='lr'
>>>>>>> 62e20d9f88eb1bcd497e60ecef9c8c0beb73207e
    ),
    'BayesianRidge': Model(
        name='Bayesian Ridge',
        model=BayesianRidge(),
<<<<<<< HEAD
        shorthand='br',
        preprocess_X=None
    ),
    'SupportVectorMachine': Model(
        name='Support Vector Machine',
        model=MultiOutputRegressor(svm.SVR(verbose=True), n_jobs=-1),
        shorthand='svm',
        preprocess_X=None#lambda x: feature_map_nystroem.fit_transform(x)
    ),
    'KNeighborsRegressor': Model(
        name='K-Nearest Neighbors Regressor',
        model=KNeighborsRegressor(n_jobs=-1),
        shorthand='knn',
        preprocess_X=None
    ),
    'MLPRegressor': Model(
        name='Multi-Layer Perceptron Regressor',
        model=mlp,
        shorthand='mlp',
        preprocess_X=None
    ),
    'GradientBoostingRegressor': Model(
        name='Gradient Boosting Regressor',
        model=GradientBoostingRegressor(),
        shorthand='gbr',
        preprocess_X=None
=======
        shorthand='br'
    ),
    'SupportVectorMachine': Model(
        name='Support Vector Machine',
        model=svm.SVR(),
        shorthand='svm'
>>>>>>> 62e20d9f88eb1bcd497e60ecef9c8c0beb73207e
    )
}


CURRENT_MODEL_KEY: str = 'SupportVectorMachine'
MODEL: Model = MODELS[CURRENT_MODEL_KEY]
