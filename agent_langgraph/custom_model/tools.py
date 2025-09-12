from langchain.tools import tool
from langchain_core.runnables.config import RunnableConfig
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


@tool
def list_drive_files(config: RunnableConfig) -> list[str]:
    """
    Lists all files in Google Drive using the OAuth token from the RunnableConfig.

    Args:
        config (RunnableConfig): Langgraph RunnableConfig containing 'oauth_token'.

    Returns:
        list: List of file names in Google Drive.
    """
    oauth_token = config.get("configurable", {}).get("oauth_token")
    if not oauth_token:
        raise ValueError("OAuth token not found in config.")
    creds = Credentials(token=oauth_token)
    service = build('drive', 'v3', credentials=creds)
    results = service.files().list(pageSize=100, fields="files(id, name)").execute()
    files = results.get('files', [])
    return [file['name'] for file in files]