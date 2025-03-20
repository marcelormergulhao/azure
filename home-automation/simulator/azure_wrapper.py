from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient

# Load properties to be used in the app
STORAGE_ACCOUNT_URL = "https://homeautomationstorageacc.blob.core.windows.net"

class AzureWrapper:

    def __init__(self, storage_account_url):
        # must connect to CosmosDB
        # must connect to Redis Cache (and underlying Blob Storage)
        self.credentials = DefaultAzureCredential()
        self.blob_service_client = BlobServiceClient(storage_account_url, credential=self.credentials)
        self.create_map_container()

    def create_map_container(self):
        self.container_name = "maps"
        print("Retrieve map container client")
        self.container_client = self.blob_service_client.get_container_client(self.container_name)
    
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


azure_wrapper = AzureWrapper(STORAGE_ACCOUNT_URL)