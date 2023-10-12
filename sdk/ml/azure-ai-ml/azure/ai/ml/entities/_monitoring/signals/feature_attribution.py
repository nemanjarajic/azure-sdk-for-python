# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

# pylint: disable=protected-access, too-many-lines

from typing import Any, Dict, List, Optional
import isodate

from azure.ai.ml._utils.utils import snake_to_camel
from azure.ai.ml._utils._experimental import experimental
from azure.ai.ml.entities._inputs_outputs import Input
from azure.ai.ml._restclient.v2023_08_01_preview.models import MonitoringInputDataBase as RestMonitoringInputData
from azure.ai.ml._restclient.v2023_08_01_preview.models import MonitoringNotificationMode
from azure.ai.ml.entities._mixins import RestTranslatableMixin
from azure.ai.ml._restclient.v2023_08_01_preview.models import (
    FeatureAttributionDriftMonitoringSignal as RestFeatureAttributionDriftMonitoringSignal,
    MonitoringThreshold,
    FeatureAttributionMetricThreshold,
)
from azure.ai.ml.entities.signals import (
    ReferenceData,
)
from azure.ai.ml.entities._monitoring.thresholds import (
    CategoricalDriftMetrics,
    NumericalDriftMetrics,
)
from azure.ai.ml.entities._monitoring.input_data import (
    TrailingInputData,
)
from azure.ai.ml.constants._monitoring import (
    MonitorSignalType,
    MonitorDatasetContext,
)

@experimental
class FeatureAttributionDriftMetricThreshold(RestTranslatableMixin):
    """Feature attribution drift metric threshold

    :param normalized_discounted_cumulative_gain: The threshold value for metric.
    :type normalized_discounted_cumulative_gain: float
    """

    def __init__(self, *, normalized_discounted_cumulative_gain: float = None):
        self.normalized_discounted_cumulative_gain = normalized_discounted_cumulative_gain

    def _to_rest_object(self) -> FeatureAttributionMetricThreshold:
        return FeatureAttributionMetricThreshold(
            metric=snake_to_camel(self.metric_name),
            threshold=MonitoringThreshold(value=self.normalized_discounted_cumulative_gain)
            if self.normalized_discounted_cumulative_gain
            else None,
        )

    @classmethod
    def _from_rest_object(cls, obj: FeatureAttributionMetricThreshold) -> "FeatureAttributionDriftMetricThreshold":
        return cls(normalized_discounted_cumulative_gain=obj.threshold.value if obj.threshold else None)


@experimental
class FADProductionData(RestTranslatableMixin):
    """Feature Attribution Production Data

    :keyword input_data: Input data used by the monitor.
    :paramtype input_data: ~azure.ai.ml.Input
    :keyword data_context: The context of the input dataset. Accepted values are "model_inputs",
        "model_outputs", "training", "test", "validation", and "ground_truth".
    :paramtype data_context: ~azure.ai.ml.constants._monitoring
    :keyword data_column_names: The names of the columns in the input data.
    :paramtype data_column_names: Dict[str, str]
    :keyword pre_processing_component : The ARM (Azure Resource Manager) resource ID of the component resource used to
        preprocess the data.
    :paramtype pre_processing_component: string
    :param data_window_size: The number of days a single monitor looks back over the target.
    :type data_window_size: string
    """

    def __init__(
        self,
        *,
        input_data: Input,
        data_context: MonitorDatasetContext = None,
        data_column_names: Dict = None,
        pre_processing_component: str = None,
        data_window_size: str = None,
    ):
        self.input_data = input_data
        self.data_context = data_context
        self.data_column_names = data_column_names
        self.pre_processing_component = pre_processing_component
        self.data_window_size = data_window_size

    def _to_rest_object(self, **kwargs) -> RestMonitoringInputData:
        default_data_window_size = kwargs.get("default")
        if self.data_window_size is None:
            self.data_window_size = default_data_window_size
        uri = self.input_data.path
        job_type = self.input_data.type
        monitoring_input_data = TrailingInputData(
            data_context=self.data_context,
            target_columns=self.data_column_names,
            job_type=job_type,
            uri=uri,
            pre_processing_component_id=self.pre_processing_component,
            window_size=self.data_window_size,
            window_offset=self.data_window_size,
        )
        return monitoring_input_data._to_rest_object()

    @classmethod
    def _from_rest_object(cls, obj: RestMonitoringInputData) -> "FADProductionData":
        return cls(
            input_data=Input(
                path=obj.uri,
                type=obj.job_input_type,
            ),
            data_context=obj.data_context,
            data_column_names=obj.columns,
            pre_processing_component=obj.preprocessing_component_id,
            data_window_size=isodate.duration_isoformat(obj.window_size),
        )


@experimental
class FeatureAttributionDriftSignal(RestTranslatableMixin):
    """Feature attribution drift signal

    :ivar type: The type of the signal. Set to "feature_attribution_drift" for this class.
    :vartype type: str
    :keyword production_data: The data for which drift will be calculated.
    :paratype production_data: ~azure.ai.ml.entities.FADProductionData
    :keyword reference_data: The data to calculate drift against.
    :paramtype reference_data: ~azure.ai.ml.entities.ReferenceData
    :keyword metric_thresholds: A list of metrics to calculate and their
        associated thresholds.
    :paramtype metric_thresholds: ~azure.ai.ml.entities.FeatureAttributionDriftMetricThreshold
    :keyword alert_enabled: Whether or not to enable alerts for the signal. Defaults to True.
    :paramtype alert_enabled: bool
    """

    def __init__(
        self,
        *,
        production_data: Optional[List[FADProductionData]] = None,
        reference_data: ReferenceData,
        metric_thresholds: FeatureAttributionDriftMetricThreshold,
        alert_enabled: bool = True,
        properties: Optional[Dict[str, str]] = None,
    ):
        self.production_data = production_data
        self.reference_data = reference_data
        self.metric_thresholds = metric_thresholds
        self.alert_enabled = alert_enabled
        self.properties = properties
        self.type = MonitorSignalType.FEATURE_ATTRIBUTION_DRIFT

    def _to_rest_object(
        self, **kwargs  # pylint: disable=unused-argument
    ) -> RestFeatureAttributionDriftMonitoringSignal:
        default_window_size = kwargs.get("default_data_window_size")
        return RestFeatureAttributionDriftMonitoringSignal(
            production_data=[data._to_rest_object(default=default_window_size) for data in self.production_data],
            reference_data=self.reference_data._to_rest_object(),
            metric_threshold=self.metric_thresholds._to_rest_object(),
            mode=MonitoringNotificationMode.ENABLED if self.alert_enabled else MonitoringNotificationMode.DISABLED,
            properties=self.properties,
        )

    @classmethod
    def _from_rest_object(cls, obj: RestFeatureAttributionDriftMonitoringSignal) -> "FeatureAttributionDriftSignal":
        return cls(
            production_data=[FADProductionData._from_rest_object(data) for data in obj.production_data],
            reference_data=ReferenceData._from_rest_object(obj.reference_data),
            metric_thresholds=FeatureAttributionDriftMetricThreshold._from_rest_object(obj.metric_threshold),
            alert_enabled=False
            if not obj.mode or (obj.mode and obj.mode == MonitoringNotificationMode.DISABLED)
            else MonitoringNotificationMode.ENABLED,
            properties=obj.properties,
        )