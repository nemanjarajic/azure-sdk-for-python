# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from azure.identity import DefaultAzureCredential
from azure.mgmt.sql import SqlManagementClient

"""
# PREREQUISITES
    pip install azure-identity
    pip install azure-mgmt-sql
# USAGE
    python update_managed_instance_with_all_properties.py

    Before run the sample, please set the values of the client ID, tenant ID and client secret
    of the AAD application as environment variables: AZURE_CLIENT_ID, AZURE_TENANT_ID,
    AZURE_CLIENT_SECRET. For more info about how to get the value, please see:
    https://docs.microsoft.com/azure/active-directory/develop/howto-create-service-principal-portal
"""


def main():
    client = SqlManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id="20D7082A-0FC7-4468-82BD-542694D5042B",
    )

    response = client.managed_instances.begin_update(
        resource_group_name="testrg",
        managed_instance_name="testinstance",
        parameters={
            "properties": {
                "administratorLogin": "dummylogin",
                "administratorLoginPassword": "PLACEHOLDER",
                "collation": "SQL_Latin1_General_CP1_CI_AS",
                "licenseType": "BasePrice",
                "maintenanceConfigurationId": "/subscriptions/20D7082A-0FC7-4468-82BD-542694D5042B/providers/Microsoft.Maintenance/publicMaintenanceConfigurations/SQL_JapanEast_MI_1",
                "minimalTlsVersion": "1.2",
                "proxyOverride": "Redirect",
                "publicDataEndpointEnabled": False,
                "requestedBackupStorageRedundancy": "Geo",
                "storageSizeInGB": 448,
                "vCores": 8,
            },
            "sku": {"capacity": 8, "name": "GP_Gen4", "tier": "GeneralPurpose"},
            "tags": {"tagKey1": "TagValue1"},
        },
    ).result()
    print(response)


# x-ms-original-file: specification/sql/resource-manager/Microsoft.Sql/preview/2021-05-01-preview/examples/ManagedInstanceUpdateMax.json
if __name__ == "__main__":
    main()