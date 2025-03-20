from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient
from azure.cosmos import CosmosClient, ContainerProxy, DatabaseProxy

# Load properties to be used in the app
STORAGE_ACCOUNT_URL = "https://homeautomationstorageacc.blob.core.windows.net"
COSMOS_URL = "https://home-automation-cosmos-acc.documents.azure.com"
COSMOS_DATABASE = "home_automation"
COSMOS_CONTAINER = "device_profile"


class AzureWrapper:

    def __init__(self, storage_account_url, cosmos_url):
        self.credentials = DefaultAzureCredential()

        # Storage Account (Blob Storage)
        self.blob_service_client = BlobServiceClient(
            storage_account_url, credential=self.credentials)
        self.create_map_container()

        # CosmosDB
        self.cosmos_client = CosmosClient(
            url=cosmos_url, credential=self.credentials)
        self.create_device_database()
        # must connect to Redis Cache (and underlying Blob Storage)

    def create_device_database(self):
        self.database_proxy = self.cosmos_client.get_database_client(
            COSMOS_DATABASE)
        self.profile_container_proxy = self.database_proxy.get_container_client(
            COSMOS_CONTAINER)

    def upsert_new_device(self, item):
        return self.profile_container_proxy.upsert_item(item)

    def get_device_profile(self, item_id):
        query = f"SELECT * FROM {COSMOS_CONTAINER} c WHERE c.id = @id"
        results = self.profile_container_proxy.query_items(
            query=query,
            enable_cross_partition_query=True,
            parameters=[
                {
                    "name": "@id",
                    "value": item_id
                }
            ])
        return [result for result in results]

    def create_map_container(self):
        self.container_name = "maps"
        print("Retrieve map container client")
        self.container_client = self.blob_service_client.get_container_client(
            self.container_name)

    def upload_blob(self, filename, data):
        blob_client = self.container_client.get_blob_client(filename)
        response = blob_client.upload_blob(data)
        print(f"Blob upload response: {response}")

    def list_blobs(self):
        blobs = self.container_client.list_blob_names()
        print("Blob names:")
        map_names = []
        for blob in blobs:
            print(f"blob: {blob}")
            map_names.append(blob)
        return map_names

    def get_blob(self, filename):
        blob = self.container_client.get_blob_client(filename)
        payload = blob.download_blob().readall()
        return payload


azure_wrapper = AzureWrapper(STORAGE_ACCOUNT_URL, COSMOS_URL)