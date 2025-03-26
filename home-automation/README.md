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
export COSMOS_ROLE=$(az cosmosdb sql role definition list --resource-group $RESOURCE_GROUP --account-name $ACCOUNT_NAME -o json | jq -r '.[] | select(.roleName == "Cosmos DB Built-in Data Contributor") .id')
export COSMOS_SCOPE=$(az cosmosdb show --resource-group $RESOURCE_GROUP --name $ACCOUNT_NAME -o json | jq -r .id)
az cosmosdb sql role assignment create --resource-group $RESOURCE_GROUP --account-name $ACCOUNT_NAME --role-definition-id $COSMOS_ROLE --principal-id $SIGNED_USER_ID --scope $COSMOS_SCOPE
az cosmosdb sql role assignment list --resource-group $RESOURCE_GROUP --account-name $ACCOUNT_NAME
```

If everything went ok the last command should output the role assignment.

1 - Create CRUD application that can write and read from CosmosDB and StorageAccount - currently the app with the azure_wrapper

2 - Deploy application to Azure Web App
-> Create Web App (console or azure CLI)
-> Enable BUILD_DURING_DEPLOYMENT (to install pip packages for example)

az webapp config appsettings set --resource-group home-automation-mm --name home-automation-mm --settings SCM_DO_BUILD_DURING_DEPLOYMENT=true

-> Create zip file with application. From simulator folder run:
zip -r simulator.zip . -x '.??*'

-> Deploy
az webapp deploy -g home-automation-mm --name home-automation-mm --src-path simulator.zip

3 - Validate webapp can write to Cosmos and Blob Storage
This requires enabling a Managed Identity (option "Identity" in the portal settings) and then setting the roles/permissions accordingly
To give the cosmos permission you will need the principal and then execute the CLI commands (use it as SIGNED_USER_ID)

4 - Set up a container registry

5 - Upload image to be used by container app
  * Login to acr with `az acr login --name REGISTRY_NAME`

6 - Deploy container app
To test the container locally, you need to create an App Registration and then fill up the env vars 
AZURE_TENANT_ID, AZURE_CLIENT_ID and AZURE_CLIENT_SECRET with the information from the App Reg.

You also need to fetch the Object ID(not the application, the instance object ID from the "Managed Application in local directory" part) and assign the appropriate permissions.

7 - When deploying the same to Container Instances you need to activate the admin user in the ACR repo. Also need to create the managed identity and assign the permissions.