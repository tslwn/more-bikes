"""Stacking regressor with the default final estimator."""

from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline

from more_bikes.experiments.experiment import Model, TaskExperiment
from more_bikes.experiments.params.stacking import stacking_fixed
from more_bikes.experiments.task_2.stacking_regressor import StackingRegressor
from more_bikes.feature_selection.drop import feature_selection_drop
from more_bikes.feature_selection.variance_threshold import (
    feature_selection_variance_threshold,
)
from more_bikes.preprocessing.ordinal_transformer import preprocessing_ordinal


def stacking():
    """Stacking regressor with the default final estimator."""
    return TaskExperiment(
        task="2",
        model=Model(
            name="stacking",
            pipeline=make_pipeline(
                # preprocessing
                preprocessing_ordinal,
                SimpleImputer(keep_empty_features=True),
                # feature selection
                feature_selection_variance_threshold,
                feature_selection_drop(["wind_speed_avg"]),
                # regression
                StackingRegressor(),
            ),
            params=[stacking_fixed],
        ),
    )
