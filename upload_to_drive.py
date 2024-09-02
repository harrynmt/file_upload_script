import os
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Function to initialize Google Drive API client
def initialize_drive_service(service_account_file):
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file,
        scopes=['https://www.googleapis.com/auth/drive.file']  # Adjust scopes as necessary
    )
    return build('drive', 'v3', credentials=credentials)

# Function to upload a file to Google Drive
def upload_file_to_drive(file_path, folder_id, service_account_file):
    # Initialize the Drive service
    drive_service = initialize_drive_service(service_account_file)

    # Prepare file metadata
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': ['1HVveRLTMwkPj0CahinfLSwi4wuO_9sTv']  # Replace with your folder ID
    }

    # Ensure the file exists before attempting to upload
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    media = MediaFileUpload(file_path)

    # Upload the file
    gfile = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"Uploaded file ID: {gfile['id']}")


# Function to delete a file from Google Drive
def delete_file_from_drive(file_id, service_account_file):
    # Initialize the Drive service
    drive_service = initialize_drive_service(service_account_file)

    try:
        # Delete the file
        drive_service.files().delete(fileId=file_id).execute()
        print(f"File with ID {file_id} deleted successfully.")
    except Exception as e:
        print(f"Error deleting file: {str(e)}")


# Main function to run the script
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python upload_to_drive.py <file_path> <folder_id> <service_account_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    folder_id = sys.argv[2]
    service_account_file = sys.argv[3]

    try:
        upload_file_to_drive(file_path, folder_id, service_account_file)
        print("File uploaded successfully!")
    except Exception as e:
        print(f"Error uploading file: {str(e)}")

