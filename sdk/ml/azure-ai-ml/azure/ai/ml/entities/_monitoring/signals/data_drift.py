# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

# pylint: disable=protected-access, too-many-lines

from typing import Any, Dict, List, Optional, Union
from typing_extensions import Literal
from azure.ai.ml._utils.utils import snake_to_camel
from azure.ai.ml._utils._experimental import experimental
from azure.ai.ml._restclient.v2023_08_01_preview.models import MonitoringNotificationMode
from azure.ai.ml.entities._mixins import RestTranslatableMixin
from azure.ai.ml._restclient.v2023_08_01_preview.models import (
    DataDriftMonitoringSignal as RestMonitoringDataDriftSignal,
    DataDriftMetricThresholdBase,
)
from azure.ai.ml.entities.signals import (
    DataSegment,
    DataSignal,
    MonitorFeatureFilter,
    MonitorFeatureDataType,
    ALL_FEATURES,
    ProductionData,
    ReferenceData,
    _to_rest_features,
    _from_rest_features,
)
from azure.ai.ml.entities._monitoring.thresholds import (
    CategoricalDriftMetrics,
    NumericalDriftMetrics,
    NumericalDataDriftMetricThreshold,
    CategoricalDataDriftMetricThreshold,
)
from azure.ai.ml.constants._monitoring import (
    ALL_FEATURES,
    MonitorFeatureDataType,
    MonitorSignalType,
)

@experimental
class DataDriftMetricThreshold(RestTranslatableMixin):
    """Data drift metric threshold

    :param applicable_feature_type: The feature type of the metric threshold
    :type applicable_feature_type: Literal[
        ~azure.ai.ml.constants.MonitorFeatureType.CATEGORICAL
        , ~azure.ai.ml.constants.MonitorFeatureType.MonitorFeatureType.NUMERICAL]
    :param metric_name: The metric to calculate
    :type metric_name: Literal[
        MonitorMetricName.JENSEN_SHANNON_DISTANCE
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

    def _to_rest_object(self) -> DataDriftMetricThresholdBase:
        thresholds = []
        if self.numerical:
            num_metric_name, num_threshold = self.numerical.get_name_and_threshold()
            thresholds.append(
                NumericalDataDriftMetricThreshold(
                    metric=snake_to_camel(num_metric_name),
                    threshold=num_threshold,
                )
            )
        if self.categorical:
            cat_metric_name, cat_threshold = self.categorical.get_name_and_threshold()
            thresholds.append(
                CategoricalDataDriftMetricThreshold(
                    metric=snake_to_camel(cat_metric_name),
                    threshold=cat_threshold,
                )
            )

        return thresholds

    @classmethod
    def _from_rest_object(cls, obj: DataDriftMetricThresholdBase) -> "DataDriftMetricThreshold":
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
    def _get_default_thresholds(cls) -> "DataDriftMetricThreshold":
        return cls(
            numerical=NumericalDriftMetrics.defaults(),
            categorical=CategoricalDriftMetrics.defaults(),
        )

    def __eq__(self, other: Any):
        if not isinstance(other, DataDriftMetricThreshold):
            return NotImplemented
        return self.numerical == other.numerical and self.categorical == other.categorical

@experimental
class DataDriftSignal(DataSignal):
    """Data drift signal.

    :ivar type: The type of the signal
    :vartype type: str
    :param production_data: The data for which drift will be calculated
    :type production_data: ~azure.ai.ml.entities.ProductionData
    :param reference_data: The data to calculate drift against
    :type reference_data: ~azure.ai.ml.entities.ReferenceData
    :param metric_thresholds :A list of metrics to calculate and their
        associated thresholds
    :type metric_thresholds: List[~azure.ai.ml.entities.DataDriftMetricThreshold]
    :param alert_enabled: The current notification mode for this signal
    :type alert_enabled: bool
    :keyword data_segment: The data segment used for scoping on a subset of the data population.
    :paramtype data_segment: ~azure.ai.ml.entities.DataSegment
    :keyword features: The feature filter identifying which feature(s) to
        calculate drift over.
    :paramtype features: Union[list[str], ~azure.ai.ml.entities.MonitorFeatureFilter, Literal['all_features']]
    """

    def __init__(
        self,
        *,
        production_data: ProductionData = None,
        reference_data: ReferenceData = None,
        features: Optional[Union[List[str], MonitorFeatureFilter, Literal[ALL_FEATURES]]] = None,
        feature_type_override: Optional[Dict[str, Union[str, MonitorFeatureDataType]]] = None,
        metric_thresholds: DataDriftMetricThreshold = None,
        alert_enabled: bool = True,
        data_segment: Optional[DataSegment] = None,
        properties: Optional[Dict[str, str]] = None,
    ):
        super().__init__(
            production_data=production_data,
            reference_data=reference_data,
            metric_thresholds=metric_thresholds,
            features=features,
            feature_type_override=feature_type_override,
            alert_enabled=alert_enabled,
            properties=properties,
        )
        self.type = MonitorSignalType.DATA_DRIFT
        self.data_segment = data_segment

    def _to_rest_object(self, **kwargs) -> RestMonitoringDataDriftSignal:
        default_data_window_size = kwargs.get("default_data_window_size")
        if self.production_data.data_window_size is None:
            self.production_data.data_window_size = default_data_window_size
        rest_features = _to_rest_features(self.features) if self.features else None
        return RestMonitoringDataDriftSignal(
            production_data=self.production_data._to_rest_object(),
            reference_data=self.reference_data._to_rest_object(),
            features=rest_features,
            feature_data_type_override=self.feature_type_override,
            metric_thresholds=self.metric_thresholds._to_rest_object(),
            mode=MonitoringNotificationMode.ENABLED if self.alert_enabled else MonitoringNotificationMode.DISABLED,
            data_segment=self.data_segment._to_rest_object() if self.data_segment else None,
            properties=self.properties,
        )

    @classmethod
    def _from_rest_object(cls, obj: RestMonitoringDataDriftSignal) -> "DataDriftSignal":
        return cls(
            production_data=ProductionData._from_rest_object(obj.production_data),
            reference_data=ReferenceData._from_rest_object(obj.reference_data),
            features=_from_rest_features(obj.features),
            feature_type_override=obj.feature_data_type_override,
            metric_thresholds=DataDriftMetricThreshold._from_rest_object(obj.metric_thresholds),
            alert_enabled=False
            if not obj.mode or (obj.mode and obj.mode == MonitoringNotificationMode.DISABLED)
            else MonitoringNotificationMode.ENABLED,
            data_segment=DataSegment._from_rest_object(obj.data_segment) if obj.data_segment else None,
            properties=obj.properties,
        )

    @classmethod
    def _get_default_data_drift_signal(cls) -> "DataDriftSignal":
        return cls(
            features=ALL_FEATURES,
            metric_thresholds=DataDriftMetricThreshold._get_default_thresholds(),
        )
