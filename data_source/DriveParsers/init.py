from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from retrieve_docs import load_docs_from_folder
import os
from dotenv import load_dotenv

load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]

def get_credentials():
    """Get Google Drive API credentials."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.getenv("GOOGLE_ACCOUNT_FILE"),
                SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def get_folder_ids(service):
    """Get all folder IDs from Google Drive."""
    try:
        results = (
            service.files()
            .list(q="mimeType='application/vnd.google-apps.folder'", fields="nextPageToken, files(id, name)")
            .execute()
        )
        items = results.get("files", [])
        folder_ids = [item['id'] for item in items]
        return folder_ids
    except HttpError as error:
        print(f"An error occurred: {error}")
        return []

def main():
    """Main function to print the names and ids of all folders the user has access to."""
    creds = get_credentials()
    service = build("drive", "v3", credentials=creds)
    folder_ids = get_folder_ids(service)
    
    if not folder_ids:
        print("No folders found.")
        return

    for folder_id in folder_ids:
        docs = load_docs_from_folder(folder_id)
        print(docs)

if __name__ == "__main__":
    main()