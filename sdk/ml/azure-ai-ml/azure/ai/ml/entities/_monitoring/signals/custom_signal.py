@experimental
class WorkspaceConnection(RestTranslatableMixin):
    """Monitoring Workspace Connection

    :keyword environment_variables: A dictionary of environment variables to set for the workspace.
    :paramtype environment_variables: Optional[dict[str, str]]
    :keyword secret_config: A dictionary of secrets to set for the workspace.
    :paramtype secret_config: Optional[dict[str, str]]
    """

    def __init__(
        self,
        *,
        environment_variables: Optional[Dict[str, str]] = None,
        secret_config: Optional[Dict[str, str]] = None,
    ):
        self.environment_variables = environment_variables
        self.secret_config = secret_config

    def _to_rest_object(self) -> RestMonitoringWorkspaceConnection:
        return RestMonitoringWorkspaceConnection(
            environment_variables=self.environment_variables,
            secrets=self.secret_config,
        )

    @classmethod
    def _from_rest_object(cls, obj: RestMonitoringWorkspaceConnection) -> "WorkspaceConnection":
        return cls(
            environment_variables=obj.environment_variables,
            secret_config=obj.secrets,
        )


@experimental
class CustomMonitoringSignal(RestTranslatableMixin):
    """Custom monitoring signal.

    :ivar type: The type of the signal. Set to "custom" for this class.
    :vartype type: str
    :keyword input_data: A dictionary of input datasets for monitoring.
        Each key is the component input port name, and its value is the data asset.
    :paramtype input_data: Optional[dict[str, ~azure.ai.ml.entities.ReferenceData]]
    :keyword metric_thresholds: A list of metrics to calculate and their
        associated thresholds.
    :paramtype metric_thresholds: list[~azure.ai.ml.entities.CustomMonitoringMetricThreshold]
    :keyword inputs:
    :paramtype inputs: Optional[dict[str, ~azure.ai.ml.entities.Input]]
    :keyword component_id: The ARM (Azure Resource Manager) ID of the component resource used to
        calculate the custom metrics.
    :paramtype component_id: str
    :keyword workspace_connection: Specify workspace connection with environment variables and secret configs.
    :paramtype workspace_connection: Optional[~azure.ai.ml.entities.WorkspaceConnection]
    :keyword alert_enabled: Whether or not to enable alerts for the signal. Defaults to True.
    :paramtype alert_enabled: bool
    :keyword properties: A dictionary of custom properties for the signal.
    :paramtype properties: Optional[dict[str, str]]
    """

    def __init__(
        self,
        *,
        inputs: Optional[Dict[str, Input]] = None,
        metric_thresholds: List[CustomMonitoringMetricThreshold],
        component_id: str,
        workspace_connection: Optional[WorkspaceConnection] = None,
        input_data: Optional[Dict[str, ReferenceData]] = None,
        alert_enabled: bool = True,
        properties: Optional[Dict[str, str]] = None,
    ):
        self.type = MonitorSignalType.CUSTOM
        self.inputs = inputs
        self.metric_thresholds = metric_thresholds
        self.component_id = component_id
        self.alert_enabled = alert_enabled
        self.input_data = input_data
        self.properties = properties
        self.workspace_connection = workspace_connection

    def _to_rest_object(self, **kwargs) -> RestCustomMonitoringSignal:  # pylint:disable=unused-argument
        if self.workspace_connection is None:
            self.workspace_connection = WorkspaceConnection()
        return RestCustomMonitoringSignal(
            component_id=self.component_id,
            metric_thresholds=[threshold._to_rest_object() for threshold in self.metric_thresholds],
            inputs=to_rest_dataset_literal_inputs(self.inputs, job_type=None) if self.inputs else None,
            input_assets={
                asset_name: asset_value._to_rest_object() for asset_name, asset_value in self.input_data.items()
            }
            if self.input_data
            else None,
            workspace_connection=self.workspace_connection._to_rest_object(),
            mode=MonitoringNotificationMode.ENABLED if self.alert_enabled else MonitoringNotificationMode.DISABLED,
            properties=self.properties,
        )

    @classmethod
    def _from_rest_object(cls, obj: RestCustomMonitoringSignal) -> "CustomMonitoringSignal":
        return cls(
            inputs=from_rest_inputs_to_dataset_literal(obj.inputs) if obj.inputs else None,
            input_data={key: ReferenceData._from_rest_object(data) for key, data in obj.input_assets.items()},
            metric_thresholds=[
                CustomMonitoringMetricThreshold._from_rest_object(metric) for metric in obj.metric_thresholds
            ],
            component_id=obj.component_id,
            alert_enabled=False
            if not obj.mode or (obj.mode and obj.mode == MonitoringNotificationMode.DISABLED)
            else MonitoringNotificationMode.ENABLED,
            properties=obj.properties,
            workspace_connection=WorkspaceConnection._from_rest_object(obj.workspace_connection),
        )