## Home Automation

Simple app to train for the Azure developer certification.

TODO:

0 - Prepare storage infrastructure
    Resource Group = home-automation-mm
    Storage Account = homeautomationstorageacc
    CosmosDB  = home-automation-cosmos-acc
    Account permissions:
        Storage Blob Data Contributor - read and write blob data

Permissions for Writing on Cosmo Container have to be given using Azure CLI, currently there is no way for a simple account to show the "Cosmos DB Built-in Data Contributor" role, for some shady reason. So run:

```
export RESOURCE_GROUP="home-automation-mm"
export ACCOUNT_NAME="home-automation-cosmos-acc"
export SIGNED_USER_ID=$(az ad signed-in-user show -o json | jq .id)
export COSMOS_ROLE=$(az cosmosdb sql role definition list --resource-group $RESOURCE_GROUP --account-name $ACCOUNT_NAME -o json | jq '.[] | select(.roleName == "Cosmos DB Built-in Data Contributor") .id')
export COSMOS_SCOPE=$(az cosmosdb show --resource-group $RESOURCE_GROUP --name $ACCOUNT_NAME -o json | jq .id)
az cosmosdb sql role assignment create --resource-group $RESOURCE_GROUP --account-name $ACCOUNT_NAME --role-definition-id $COSMOS_ROLE --principal-id $SIGNED_USER_ID --scope $COSMOS_SCOPE
az cosmosdb sql role assignment list --resource-group $RESOURCE_GROUP --account-name $ACCOUNT_NAME
```

If everything went ok the last command should output the role assignment.

1 - Create CRUD application that can write and read from CosmosDB and StorageAccount - currently the app with the azure_wrapper