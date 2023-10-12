@experimental
class LlmData(RestTranslatableMixin):
    """LLM Request Response Data

    :keyword input_data: Input data used by the monitor.
    :paramtype input_data: ~azure.ai.ml.entities.Input
    :keyword data_column_names: The names of columns in the input data.
    :paramtype data_column_names: Dict[str, str]
    :keyword data_window_size: The number of days a single monitor looks back
        over the target
    :paramtype data_window_size: Optional[int]
    """

    def __init__(
        self,
        *,
        input_data: Input,
        data_column_names: Optional[Dict[str, str]] = None,
        data_window_size: Optional[str] = None,
    ):
        self.input_data = input_data
        self.data_column_names = data_column_names
        self.data_window_size = data_window_size

    def _to_rest_object(self, **kwargs) -> RestMonitoringInputData:
        if self.data_window_size is None:
            self.data_window_size = kwargs.get("default")
        return TrailingInputData(
            target_columns=self.data_column_names,
            job_type=self.input_data.type,
            uri=self.input_data.path,
            window_size=self.data_window_size,
            window_offset=self.data_window_size,
        )._to_rest_object()

    @classmethod
    def _from_rest_object(cls, obj: RestMonitoringInputData) -> "LlmData":
        return cls(
            input_data=Input(
                path=obj.uri,
                type=obj.job_input_type,
            ),
            data_column_names=obj.columns,
            data_window_size=isodate.duration_isoformat(obj.window_size),
        )


@experimental
class GenerationSafetyQualitySignal(RestTranslatableMixin):
    """Generation Safety Quality monitoring signal.

    :ivar type: The type of the signal. Set to "generationsafetyquality" for this class.
    :vartype type: str
    :keyword production_data: A list of input datasets for monitoring.
    :paramtype input_datasets: Optional[dict[str, ~azure.ai.ml.entities.LlmData]]
    :keyword metric_thresholds: Metrics to calculate and their associated thresholds.
    :paramtype metric_thresholds: ~azure.ai.ml.entities.GenerationSafetyQualityMonitoringMetricThreshold
    :keyword alert_enabled: Whether or not to enable alerts for the signal. Defaults to True.
    :paramtype alert_enabled: bool
    :keyword workspace_connection_id: Gets or sets the workspace connection ID used to connect to the
        content generation endpoint.
    :paramtype workspace_connection_id: str
    :keyword properties: The properties of the signal
    :paramtype properties: Dict[str, str]
    :keyword sampling_rate: The sample rate of the target data, should be greater
        than 0 and at most 1.
    :paramtype sampling_rate: float
    """

    def __init__(
        self,
        *,
        production_data: List[LlmData] = None,
        workspace_connection_id: Optional[str] = None,
        metric_thresholds: GenerationSafetyQualityMonitoringMetricThreshold,
        alert_enabled: bool = True,
        properties: Optional[Dict[str, str]] = None,
        sampling_rate: float = None,
    ):
        self.type = MonitorSignalType.GENERATION_SAFETY_QUALITY
        self.production_data = production_data
        self.workspace_connection_id = workspace_connection_id
        self.metric_thresholds = metric_thresholds
        self.alert_enabled = alert_enabled
        self.properties = properties
        self.sampling_rate = sampling_rate

    def _to_rest_object(self, **kwargs) -> RestGenerationSafetyQualityMonitoringSignal:
        data_window_size = kwargs.get("default_data_window_size")
        return RestGenerationSafetyQualityMonitoringSignal(
            production_data=[data._to_rest_object(default=data_window_size) for data in self.production_data],
            workspace_connection_id=self.workspace_connection_id,
            metric_thresholds=self.metric_thresholds._to_rest_object(),
            mode=MonitoringNotificationMode.ENABLED if self.alert_enabled else MonitoringNotificationMode.DISABLED,
            properties=self.properties,
            sampling_rate=self.sampling_rate,
        )

    @classmethod
    def _from_rest_object(cls, obj: RestGenerationSafetyQualityMonitoringSignal) -> "GenerationSafetyQualitySignal":
        return cls(
            production_data=[LlmData._from_rest_object(data) for data in obj.production_data],
            workspace_connection_id=obj.workspace_connection_id,
            metric_thresholds=GenerationSafetyQualityMonitoringMetricThreshold._from_rest_object(obj.metric_thresholds),
            alert_enabled=False
            if not obj.mode or (obj.mode and obj.mode == MonitoringNotificationMode.DISABLED)
            else MonitoringNotificationMode.ENABLED,
            properties=obj.properties,
            sampling_rate=obj.sampling_rate,
        )