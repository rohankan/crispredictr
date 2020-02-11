from processing import sequence_to_one_hots, sequence_to_ordinals
from typing import List, Callable, Any, NamedTuple, Dict
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, BayesianRidge
from sklearn import svm


MIN_INDEL: int = -30
MAX_INDEL: int = +5


INDEL_RANGE: List[int] = list(range(MIN_INDEL, MAX_INDEL+1))


SEQUENCE_MAPPER: Callable[[str], Any] = sequence_to_ordinals


RANDOM_STATE: int = 42


# Model with method 'fit(X, y)'
Model = NamedTuple('Model', [('name', str), ('model', Any), ('shorthand', str)])


MODELS: Dict[str, Model] = {
    'RandomForest': Model(
        name='Random Forest',
        model=RandomForestRegressor(n_jobs=-1, bootstrap=True, random_state=RANDOM_STATE, verbose=1),
        shorthand='rf'
    ),
    'LinearRegression': Model(
        name='Linear Regression',
        model=LinearRegression(n_jobs=-1),
        shorthand='lr'
    ),
    'BayesianRidge': Model(
        name='Bayesian Ridge',
        model=BayesianRidge(),
        shorthand='br'
    ),
    'SupportVectorMachine': Model(
        name='Support Vector Machine',
        model=svm.SVR(),
        shorthand='svm'
    )
}


CURRENT_MODEL_KEY: str = 'SupportVectorMachine'
MODEL: Model = MODELS[CURRENT_MODEL_KEY]
