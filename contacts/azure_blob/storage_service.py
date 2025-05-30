from azure.identity import ClientSecretCredential
from storages.backends.azure_storage import AzureStorage
from azure.storage.blob import BlobServiceClient
from decouple import config
from django.conf import settings


# class AzureBlobService: #manual file upload
#     def __init__(self):
#         self.tenant_id = config("AZURE_TENANT_ID")
#         self.client_id = config("AZURE_CLIENT_ID")
#         self.client_secret = config("AZURE_CLIENT_SECRET")
#         self.storage_account = config("AZURE_STORAGE_ACCOUNT")
#         self.container_name = config("AZURE_CONTAINER_NAME")

#         self.credential = ClientSecretCredential(
#             tenant_id=self.tenant_id,
#             client_id=self.client_id,
#             client_secret=self.client_secret
#         )

#         self.blob_service_client = BlobServiceClient(
#             account_url=f"https://{self.storage_account}.blob.core.windows.net",
#             credential=self.credential
#         )

#         self.container_client = self.blob_service_client.get_container_client(
#             self.container_name)

#     # contacts/azure_blob/storage_service.py
#     def upload_file(self, file_obj, blob_name):
        
        
#         blob_client = self.container_client.get_blob_client(blob_name)
#         blob_client.upload_blob(file_obj, overwrite=True)

#     def download_file(self, blob_name):
#         blob_client = self.container_client.get_blob_client(blob_name)
#         downloader = blob_client.download_blob()
#         return downloader.readall()

class AzureMediaStorage(AzureStorage):    
    print("DEBUG: AzureMediaStorage init called")
    account_name = settings.AZURE_STORAGE_ACCOUNT
    container_name = settings.AZURE_CONTAINER_NAME
    expiration_secs = None  # public URLs; set to a number if you want signed URLs

    def __init__(self, *args, **kwargs):
        print("DEBUG: AzureMediaStorage init called")
        credential = ClientSecretCredential(
            tenant_id=settings.AZURE_TENANT_ID,
            client_id=settings.AZURE_CLIENT_ID,
            client_secret=settings.AZURE_CLIENT_SECRET
        )
        kwargs["credential"] = credential
        super().__init__(*args, **kwargs)
