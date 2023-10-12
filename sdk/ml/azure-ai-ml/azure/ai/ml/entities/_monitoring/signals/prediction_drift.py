# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

# pylint: disable=protected-access, too-many-lines

from typing import Any, Dict, Optional
from azure.ai.ml._utils.utils import snake_to_camel
from azure.ai.ml._utils._experimental import experimental
from azure.ai.ml._restclient.v2023_08_01_preview.models import MonitoringNotificationMode
from azure.ai.ml.entities._mixins import RestTranslatableMixin
from azure.ai.ml._restclient.v2023_08_01_preview.models import (
    PredictionDriftMonitoringSignal as RestPredictionDriftMonitoringSignal,
    PredictionDriftMetricThresholdBase,
    NumericalPredictionDriftMetricThreshold,
    CategoricalPredictionDriftMetricThreshold,
)
from azure.ai.ml.entities.signals import (
    MonitoringSignal,
    ProductionData,
    ReferenceData,
)
from azure.ai.ml.entities._monitoring.thresholds import (
    CategoricalDriftMetrics,
    NumericalDriftMetrics,
)
from azure.ai.ml.constants._monitoring import (
    MonitorSignalType,
)

@experimental
class PredictionDriftMetricThreshold(RestTranslatableMixin):
    """Prediction drift metric threshold

    :param applicable_feature_type: The feature type of the metric threshold
    :type applicable_feature_type: Literal[
        ~azure.ai.ml.constants.MonitorFeatureType.CATEGORICAL
        , ~azure.ai.ml.constants.MonitorFeatureType.MonitorFeatureType.NUMERICAL]
    :param metric_name: The metric to calculate
    :type metric_name: Literal[
        ~azure.ai.ml.constants.MonitorMetricName.JENSEN_SHANNON_DISTANCE
        , ~azure.ai.ml.constants.MonitorMetricName.NORMALIZED_WASSERSTEIN_DISTANCE
        , ~azure.ai.ml.constants.MonitorMetricName.POPULATION_STABILITY_INDEX
        , ~azure.ai.ml.constants.MonitorMetricName.TWO_SAMPLE_KOLMOGOROV_SMIRNOV_TEST
        , ~azure.ai.ml.constants.MonitorMetricName.PEARSONS_CHI_SQUARED_TEST]
    :param threshold: The threshold value. If None, a default value will be set
        depending on the selected metric.
    :type threshold: float
    """

    def __init__(
        self,
        *,
        numerical: NumericalDriftMetrics = None,
        categorical: CategoricalDriftMetrics = None,
    ):
        self.numerical = numerical
        self.categorical = categorical

    def _to_rest_object(self) -> PredictionDriftMetricThresholdBase:
        thresholds = []
        if self.numerical:
            num_metric_name, num_threshold = self.numerical.get_name_and_threshold()
            thresholds.append(
                NumericalPredictionDriftMetricThreshold(
                    metric=snake_to_camel(num_metric_name),
                    threshold=num_threshold,
                )
            )
        if self.categorical:
            cat_metric_name, cat_threshold = self.categorical.get_name_and_threshold()
            thresholds.append(
                CategoricalPredictionDriftMetricThreshold(
                    metric=snake_to_camel(cat_metric_name),
                    threshold=cat_threshold,
                )
            )

        return thresholds

    @classmethod
    def _from_rest_object(cls, obj: PredictionDriftMetricThresholdBase) -> "PredictionDriftMetricThreshold":
        num = None
        cat = None
        for threshold in obj:
            if threshold.data_type == "Numerical":
                num = NumericalDriftMetrics()._from_rest_object(  # pylint: disable=protected-access
                    threshold.metric, threshold.threshold.value if threshold.threshold else None
                )
            elif threshold.data_type == "Categorical":
                cat = CategoricalDriftMetrics()._from_rest_object(  # pylint: disable=protected-access
                    threshold.metric, threshold.threshold.value if threshold.threshold else None
                )

        return cls(
            numerical=num,
            categorical=cat,
        )

    @classmethod
    def _get_default_thresholds(cls) -> "PredictionDriftMetricThreshold":
        return cls(
            numerical=NumericalDriftMetrics.defaults(),
            categorical=CategoricalDriftMetrics.defaults(),
        )

    def __eq__(self, other: Any):
        if not isinstance(other, PredictionDriftMetricThreshold):
            return NotImplemented
        return self.numerical == other.numerical and self.categorical == other.categorical


@experimental
class PredictionDriftSignal(MonitoringSignal):
    """Prediction drift signal.

    :ivar type: The type of the signal. Set to "prediction_drift" for this class.
    :vartype type: str
    :keyword baseline_dataset: The dataset to calculate drift against.
    :paramtype baseline_dataset: ~azure.ai.ml.entities.MonitorInputData
    :keyword metric_thresholds: A list of metrics to calculate and their associated thresholds
    :paramtype metric_thresholds: list[~azure.ai.ml.entities.PredictionDriftMetricThreshold]
    :keyword alert_enabled: Whether or not to enable alerts for the signal. Defaults to True.
    :paramtype alert_enabled: bool
    """

    def __init__(
        self,
        *,
        production_data: ProductionData = None,
        reference_data: ReferenceData = None,
        metric_thresholds: PredictionDriftMetricThreshold,
        alert_enabled: bool = True,
        properties: Optional[Dict[str, str]] = None,
    ):
        super().__init__(
            production_data=production_data,
            reference_data=reference_data,
            metric_thresholds=metric_thresholds,
            alert_enabled=alert_enabled,
            properties=properties,
        )
        self.type = MonitorSignalType.PREDICTION_DRIFT

    def _to_rest_object(self, **kwargs) -> RestPredictionDriftMonitoringSignal:
        default_data_window_size = kwargs.get("default_data_window_size")
        if self.production_data.data_window_size is None:
            self.production_data.data_window_size = default_data_window_size
        return RestPredictionDriftMonitoringSignal(
            production_data=self.production_data._to_rest_object(),
            reference_data=self.reference_data._to_rest_object(),
            metric_thresholds=self.metric_thresholds._to_rest_object(),
            properties=self.properties,
            mode=MonitoringNotificationMode.ENABLED if self.alert_enabled else MonitoringNotificationMode.DISABLED,
            model_type="classification",
        )

    @classmethod
    def _from_rest_object(cls, obj: RestPredictionDriftMonitoringSignal) -> "PredictionDriftSignal":
        return cls(
            production_data=ProductionData._from_rest_object(obj.production_data),
            reference_data=ReferenceData._from_rest_object(obj.reference_data),
            metric_thresholds=PredictionDriftMetricThreshold._from_rest_object(obj.metric_thresholds),
            alert_enabled=False
            if not obj.mode or (obj.mode and obj.mode == MonitoringNotificationMode.DISABLED)
            else MonitoringNotificationMode.ENABLED,
            properties=obj.properties,
        )

    @classmethod
    def _get_default_prediction_drift_signal(cls) -> "PredictionDriftSignal":
        return cls(
            metric_thresholds=PredictionDriftMetricThreshold._get_default_thresholds(),
        )