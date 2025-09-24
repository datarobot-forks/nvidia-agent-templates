from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from langchain.tools import BaseTool, tool


def list_drive_files_tool(google_token: str) -> BaseTool:
    if not google_token:
        raise RuntimeError("Invalid google token")

    @tool
    def list_drive_files(query: str) -> list[str]:
        """
        Lists all files in Google Drive using the OAuth token from the RunnableConfig.

        Args:
            config (RunnableConfig): Langgraph RunnableConfig containing 'oauth_token'.

        Returns:
            list: List of file names in Google Drive.
        """
        query_words = query.split()
        q = " or ".join(
            f"fullText contains '{w}' or name contains '{w}'" for w in query_words
        )
        creds = Credentials(token=google_token)  # type:ignore[no-untyped-call]
        service = build("drive", "v3", credentials=creds)
        results = (
            service.files().list(pageSize=10, fields="files(id, name)", q=q).execute()
        )
        files = results.get("files", [])
        return [file["name"] for file in files]

    return list_drive_files
