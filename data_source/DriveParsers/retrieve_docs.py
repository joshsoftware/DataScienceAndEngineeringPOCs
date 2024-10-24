from langchain_google_community import GoogleDriveLoader
import os
from dotenv import load_dotenv

load_dotenv()

def load_docs_from_folder(folder_id):
    loader = GoogleDriveLoader(
        folder_id=folder_id,
        credentials_path=os.getenv("GOOGLE_ACCOUNT_FILE"),
    )
    docs = loader.load()
    return docs

