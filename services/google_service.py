from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import os
from datetime import datetime

class GoogleDocsService:
    def __init__(self):
        self.SCOPES = [
            'https://www.googleapis.com/auth/documents',
            'https://www.googleapis.com/auth/drive.file'
        ]
        self.creds = self._get_credentials()
        self.docs_service = build('docs', 'v1', credentials=self.creds)
        self.drive_service = build('drive', 'v3', credentials=self.creds)

    def _get_credentials(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secrets.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return creds

    async def create_document(self, content: str, topic: str) -> str:
        try:
            title = f"LinkedIn Post - {topic} - {datetime.now().strftime('%Y-%m-%d')}"
            doc = self.docs_service.documents().create(body={'title': title}).execute()
            doc_id = doc.get('documentId')

            requests = [{
                'insertText': {
                    'location': {'index': 1},
                    'text': content
                }
            }]

            self.docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()

            return f"https://docs.google.com/document/d/{doc_id}/edit"

        except Exception as e:
            return f"Error: {str(e)}"
