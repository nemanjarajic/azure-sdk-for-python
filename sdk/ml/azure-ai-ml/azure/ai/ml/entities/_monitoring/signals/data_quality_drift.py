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
    DataQualityMonitoringSignal as RestMonitoringDataQualitySignal,
    MonitoringThreshold,
    DataQualityMetricThresholdBase,
    NumericalDataQualityMetricThreshold,
    CategoricalDataQualityMetricThreshold,
)
from azure.ai.ml.entities.signals import (
    DataSignal,
    MonitorFeatureFilter,
    MonitorFeatureDataType,
    ALL_FEATURES,
    ProductionData,
    ReferenceData,
    _to_rest_features,
    _from_rest_features,
)
from azure.ai.ml.constants._monitoring import (
    ALL_FEATURES,
    MonitorFeatureDataType,
    MonitorSignalType,
    MonitorMetricName
)

@experimental
class DataQualityMetricsNumerical(RestTranslatableMixin):
    def __init__(
        self,
        *,
        null_value_rate: float = None,
        data_type_error_rate: float = None,
        out_of_bounds_rate: float = None
    ):
        self.null_value_rate = null_value_rate
        self.data_type_error_rate = data_type_error_rate
        self.out_of_bounds_rate = out_of_bounds_rate

    def _to_rest_object(self) -> List[NumericalDataQualityMetricThreshold]:
        metric_thresholds = []
        if self.null_value_rate is not None:
            metric_name = MonitorMetricName.NULL_VALUE_RATE
            threshold = MonitoringThreshold(value=self.null_value_rate)
            metric_thresholds.append(
                NumericalDataQualityMetricThreshold(metric=snake_to_camel(metric_name), threshold=threshold)
            )
        if self.data_type_error_rate is not None:
            metric_name = MonitorMetricName.DATA_TYPE_ERROR_RATE
            threshold = MonitoringThreshold(value=self.data_type_error_rate)
            metric_thresholds.append(
                NumericalDataQualityMetricThreshold(metric=snake_to_camel(metric_name), threshold=threshold)
            )
        if self.out_of_bounds_rate is not None:
            metric_name = MonitorMetricName.OUT_OF_BOUND_RATE
            threshold = MonitoringThreshold(value=self.out_of_bounds_rate)
            metric_thresholds.append(
                NumericalDataQualityMetricThreshold(metric=snake_to_camel(metric_name), threshold=threshold)
            )

        return metric_thresholds

    @classmethod
    def _from_rest_object(cls, obj: List) -> "DataQualityMetricsNumerical":
        null_value_rate_val = None
        data_type_error_rate_val = None
        out_of_bounds_rate_val = None
        for thresholds in obj:
            if thresholds.metric == "nullValueRate":
                null_value_rate_val = thresholds.threshold.value
            if thresholds.metric == "dataTypeErrorRate":
                data_type_error_rate_val = thresholds.threshold.value
            if thresholds.metric == "outOfBoundsRate":
                out_of_bounds_rate_val = thresholds.threshold.value
        return cls(
            null_value_rate=null_value_rate_val,
            data_type_error_rate=data_type_error_rate_val,
            out_of_bounds_rate=out_of_bounds_rate_val,
        )

    @classmethod
    def _get_default_thresholds(cls) -> "DataQualityMetricsNumerical":
        return cls(
            null_value_rate=0.0,
            data_type_error_rate=0.0,
            out_of_bounds_rate=0.0,
        )

    @classmethod
    def defaults(cls) -> "DataQualityMetricsNumerical":
        return cls._get_default_thresholds()


@experimental
class DataQualityMetricsCategorical(RestTranslatableMixin):
    def __init__(
        self,
        *,
        null_value_rate: float = None,
        data_type_error_rate: float = None,
        out_of_bounds_rate: float = None
    ):
        self.null_value_rate = null_value_rate
        self.data_type_error_rate = data_type_error_rate
        self.out_of_bounds_rate = out_of_bounds_rate

    def _to_rest_object(self) -> List[CategoricalDataQualityMetricThreshold]:
        metric_thresholds = []
        if self.null_value_rate is not None:
            metric_name = MonitorMetricName.NULL_VALUE_RATE
            threshold = MonitoringThreshold(value=self.null_value_rate)
            metric_thresholds.append(
                CategoricalDataQualityMetricThreshold(metric=snake_to_camel(metric_name), threshold=threshold)
            )
        if self.data_type_error_rate is not None:
            metric_name = MonitorMetricName.DATA_TYPE_ERROR_RATE
            threshold = MonitoringThreshold(value=self.data_type_error_rate)
            metric_thresholds.append(
                CategoricalDataQualityMetricThreshold(metric=snake_to_camel(metric_name), threshold=threshold)
            )
        if self.out_of_bounds_rate is not None:
            metric_name = MonitorMetricName.OUT_OF_BOUND_RATE
            threshold = MonitoringThreshold(value=self.out_of_bounds_rate)
            metric_thresholds.append(
                CategoricalDataQualityMetricThreshold(metric=snake_to_camel(metric_name), threshold=threshold)
            )

        return metric_thresholds

    @classmethod
    def _from_rest_object(cls, obj: List) -> "DataQualityMetricsCategorical":
        null_value_rate_val = None
        data_type_error_rate_val = None
        out_of_bounds_rate_val = None
        for thresholds in obj:
            if thresholds.metric == "nullValueRate":
                null_value_rate_val = thresholds.threshold.value
            if thresholds.metric == "dataTypeErrorRate":
                data_type_error_rate_val = thresholds.threshold.value
            if thresholds.metric == "outOfBoundsRate":
                out_of_bounds_rate_val = thresholds.threshold.value
        return cls(
            null_value_rate=null_value_rate_val,
            data_type_error_rate=data_type_error_rate_val,
            out_of_bounds_rate=out_of_bounds_rate_val,
        )

    @classmethod
    def _get_default_thresholds(cls) -> "DataQualityMetricsCategorical":
        return cls(
            null_value_rate=0.0,
            data_type_error_rate=0.0,
            out_of_bounds_rate=0.0,
        )

    @classmethod
    def defaults(cls) -> "DataQualityMetricsCategorical":
        return cls._get_default_thresholds()


@experimental
class DataQualityMetricThreshold(RestTranslatableMixin):
    """Data quality metric threshold

    :param applicable_feature_type: The feature type of the metric threshold
    :type applicable_feature_type: Literal[
        ~azure.ai.ml.constants.MonitorFeatureType.CATEGORICAL
        , ~azure.ai.ml.constants.MonitorFeatureType.MonitorFeatureType.NUMERICAL]
    :param metric_name: The metric to calculate
    :type metric_name: Literal[
        ~azure.ai.ml.constants.MonitorMetricName.JENSEN_SHANNON_DISTANCE
        , ~azure.ai.ml.constants.MonitorMetricName.NULL_VALUE_RATE
        , ~azure.ai.ml.constants.MonitorMetricName.DATA_TYPE_ERROR_RATE
        , ~azure.ai.ml.constants.MonitorMetricName.OUT_OF_BOUND_RATE]
    :param threshold: The threshold value. If None, a default value will be set
        depending on the selected metric.
    :type threshold: float
    """

    def __init__(
        self,
        *,
        numerical: Optional[DataQualityMetricsNumerical] = None,
        categorical: Optional[DataQualityMetricsCategorical] = None,
    ):
        self.numerical = numerical
        self.categorical = categorical

    def _to_rest_object(self) -> DataQualityMetricThresholdBase:
        thresholds = []
        if self.numerical:
            thresholds = thresholds + (
                DataQualityMetricsNumerical(  # pylint: disable=protected-access
                    null_value_rate=self.numerical.null_value_rate,
                    data_type_error_rate=self.numerical.data_type_error_rate,
                    out_of_bounds_rate=self.numerical.out_of_bounds_rate,
                )._to_rest_object()
            )
        if self.categorical:
            thresholds = thresholds + (
                DataQualityMetricsCategorical(  # pylint: disable=protected-access
                    null_value_rate=self.numerical.null_value_rate,
                    data_type_error_rate=self.numerical.data_type_error_rate,
                    out_of_bounds_rate=self.numerical.out_of_bounds_rate,
                )._to_rest_object()
            )
        return thresholds

    @classmethod
    def _from_rest_object(cls, obj: DataQualityMetricThresholdBase) -> "DataQualityMetricThreshold":
        num = []
        cat = []
        for threshold in obj:
            if threshold.data_type == "Numerical":
                num.append(threshold)
            elif threshold.data_type == "Categorical":
                cat.append(threshold)

        num_from_rest = DataQualityMetricsNumerical()._from_rest_object(num)  # pylint: disable=protected-access
        cat_from_rest = DataQualityMetricsCategorical()._from_rest_object(cat)  # pylint: disable=protected-access
        return cls(
            numerical=num_from_rest,
            categorical=cat_from_rest,
        )

    @classmethod
    def _get_default_thresholds(cls) -> "DataQualityMetricThreshold":
        return cls(
            numerical=DataQualityMetricsNumerical()._get_default_thresholds(),  # pylint: disable=protected-access
            categorical=DataQualityMetricsCategorical()._get_default_thresholds(),  # pylint: disable=protected-access
        )

    def __eq__(self, other: Any):
        if not isinstance(other, DataQualityMetricThreshold):
            return NotImplemented
        return (
            self.data_type == other.data_type
            and self.metric_name == other.metric_name
            and self.threshold == other.threshold
        )

@experimental
class DataQualitySignal(DataSignal):
    """Data quality signal

    :ivar type: The type of the signal. Set to "data_quality" for this class.
    :vartype type: str
    :keyword baseline_dataset: The data to calculate quality against.
    :paramtype baseline_dataset: ~azure.ai.ml.entities.MonitorInputData
    :keyword metric_thresholds: A list of metrics to calculate and their
        associated thresholds.
    :paramtype metric_thresholds: list[~azure.ai.ml.entities.DataQualityMetricThreshold]
    :keyword alert_enabled: Whether or not to enable alerts for the signal. Defaults to True.
    :paramtype alert_enabled: bool
    :keyword features: The feature filter identifying which feature(s) to
        calculate quality over.
    :paramtype features: Union[list[str], ~azure.ai.ml.entities.MonitorFeatureFilter, Literal['all_features']]
    """

    def __init__(
        self,
        *,
        production_data: ProductionData = None,
        reference_data: ReferenceData = None,
        features: Optional[Union[List[str], MonitorFeatureFilter, Literal[ALL_FEATURES]]] = None,
        feature_type_override: Optional[Dict[str, Union[str, MonitorFeatureDataType]]] = None,
        metric_thresholds: [DataQualityMetricThreshold] = None,
        alert_enabled: bool = True,
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
        self.type = MonitorSignalType.DATA_QUALITY

    def _to_rest_object(self, **kwargs) -> RestMonitoringDataQualitySignal:
        default_data_window_size = kwargs.get("default_data_window_size")
        if self.production_data.data_window_size is None:
            self.production_data.data_window_size = default_data_window_size
        rest_features = _to_rest_features(self.features) if self.features else None
        rest_metrics = _to_rest_data_quality_metrics(
            self.metric_thresholds.numerical, self.metric_thresholds.categorical
        )
        return RestMonitoringDataQualitySignal(
            production_data=self.production_data._to_rest_object(),
            reference_data=self.reference_data._to_rest_object(),
            features=rest_features,
            feature_data_type_override=self.feature_type_override,
            metric_thresholds=rest_metrics,
            mode=MonitoringNotificationMode.ENABLED if self.alert_enabled else MonitoringNotificationMode.DISABLED,
            properties=self.properties,
        )

    @classmethod
    def _from_rest_object(cls, obj: RestMonitoringDataQualitySignal) -> "DataQualitySignal":
        return cls(
            production_data=ProductionData._from_rest_object(obj.production_data),
            reference_data=ReferenceData._from_rest_object(obj.reference_data),
            features=_from_rest_features(obj.features),
            feature_type_override=obj.feature_data_type_override,
            metric_thresholds=DataQualityMetricThreshold._from_rest_object(obj.metric_thresholds),
            alert_enabled=False
            if not obj.mode or (obj.mode and obj.mode == MonitoringNotificationMode.DISABLED)
            else MonitoringNotificationMode.ENABLED,
            properties=obj.properties,
        )

    @classmethod
    def _get_default_data_quality_signal(
        cls,
    ) -> "DataQualitySignal":
        return cls(
            features=ALL_FEATURES,
            metric_thresholds=DataQualityMetricThreshold._get_default_thresholds(),
        )


def _to_rest_data_quality_metrics(numerical_metrics, categorical_metrics):
    metric_thresholds = []
    if numerical_metrics is not None:
        metric_thresholds = metric_thresholds + numerical_metrics._to_rest_object()

    if categorical_metrics is not None:
        metric_thresholds = metric_thresholds + categorical_metrics._to_rest_object()

    return metric_thresholds