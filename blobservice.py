from flask import Flask, request, render_template
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os

app = Flask(__name__)

# Azure Storage credentials
storage_account_key = ""
storage_account_name = ""
azure_storage_connection_string = ""
azure_storage_connection_string = ""
container_name = ""

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Get the uploaded file
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            try:
                # Create a BlobServiceClient using the connection string
                blob_service_client = BlobServiceClient.from_connection_string(azure_storage_connection_string)
                blob_client = blob_service_client.get_blob_client(container=container_name, blob=uploaded_file.filename)
                blob_service_client = BlobServiceClient.from_connection_string(azure_storage_connection_string)
                # Create a ContainerClient
                # container_client = blob_service_client.get_container_client(container_name)

                # Check if the blob (file) already exists in the container
                # blob_client = container_client.get_blob_client(uploaded_file.filename)
                if blob_client.exists():
                    # If it exists, delete the existing blob before uploading the new one
                    blob_client.delete_blob()

                # Upload the file to Azure Storage
                blob_client.upload_blob(uploaded_file.read())

                return "File successfully uploaded to Azure Storage!"

            except Exception as e:
                return str(e)

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)


# from azure.storage.blob import BlobServiceClient

# storage_account_key = "ok0LtCSnOQe8Lu/nPHzaumekoVa0ihQAVGYAR7FLJMQXUxcJ5+4VMotHHnL+FLfTLp2SJrfyHNdR+ASttHmKOQ=="
# storage_account_name = "storageaccount897"
# connection_string = "DefaultEndpointsProtocol=https;AccountName=storageaccount897;AccountKey=ok0LtCSnOQe8Lu/nPHzaumekoVa0ihQAVGYAR7FLJMQXUxcJ5+4VMotHHnL+FLfTLp2SJrfyHNdR+ASttHmKOQ==;EndpointSuffix=core.windows.net"
# container_name = "ok0LtCSnOQe8Lu/nPHzaumekoVa0ihQAVGYAR7FLJMQXUxcJ5+4VMotHHnL+FLfTLp2SJrfyHNdR+ASttHmKOQ=="

# def uploadToBlobStorage(file_path,file_name):
#    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
#    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
#    with open(file_path,”rb”) as data:
#       blob_client.upload_blob(data)
#       print(f”Uploaded {file_name}.”)

# # calling a function to perform upload
# uploadToBlobStorage('PATH_OF_FILE_TO_UPLOAD','FILE_NAME')