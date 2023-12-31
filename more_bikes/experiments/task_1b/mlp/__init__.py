"""Task 1B: Multi-layer perceptron."""

from numpy import nan
from sklearn.discriminant_analysis import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline

from more_bikes.experiments.experiment import Model, TaskExperiment
from more_bikes.feature_selection.drop import feature_selection_drop
from more_bikes.feature_selection.variance_threshold import (
    feature_selection_variance_threshold,
)
from more_bikes.preprocessing.bikes_fraction_transformer import BikesFractionTransformer
from more_bikes.preprocessing.ordinal_transformer import preprocessing_ordinal
from more_bikes.preprocessing.transformed_target_regressor import (
    TransformedTargetRegressor,
)


def mlp():
    """Multi-layer perceptron."""
    return TaskExperiment(
        task="1b",
        model=Model(
            name="mlp",
            pipeline=TransformedTargetRegressor(
                make_pipeline(
                    # preprocessing
                    preprocessing_ordinal,
                    SimpleImputer(strategy="constant", fill_value=0),
                    StandardScaler(),
                    # feature selection
                    feature_selection_variance_threshold,
                    feature_selection_drop(
                        [
                            "bikes_3h_diff_avg_short",
                            "bikes_avg_short",
                            "wind_speed_avg",
                        ]
                    ),
                    # regression
                    MLPRegressor(random_state=42),
                ),
                transformer=BikesFractionTransformer(),
            ),
            params=[
                {
                    "regressor__mlpregressor__hidden_layer_sizes": [
                        (16, 16, 16),
                        (32, 32, 32),
                        (64, 64, 64),
                    ],
                    "regressor__mlpregressor__activation": [
                        "logistic",
                        "tanh",
                        "relu",
                    ],
                    "regressor__mlpregressor__learning_rate": [
                        "constant",
                        "invscaling",
                        "adaptive",
                    ],
                }
            ],
        ),
        search="halving",
    )
