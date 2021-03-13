import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

GOOGLE_OAUTH_SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def create_service():
    """
    Create the Google API service.

    :return: The corresponding `Resource`.
    """

    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', GOOGLE_OAUTH_SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # run first-time oauth flow
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', GOOGLE_OAUTH_SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)
