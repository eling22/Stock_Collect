from __future__ import print_function
from importlib.resources import Resource
import os.path
from winreg import QueryValue
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from rich import print
import base64

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_gmail_service() -> Resource:
    """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service


def main():

    # the search string for only show the email with the string
    QUERY_STRING = "玉山證券經紀本部"

    service = get_gmail_service()
    results = service.users().messages().list(userId='me', q=QUERY_STRING).execute()
    messages = results.get('messages', [])
    mails = []
    # print(len(messages))
    for msg in messages:
        id = msg["id"]
        msg = service.users().messages().get(userId='me', id=id).execute()
        # print(msg)
        # print(msg["payload"]["headers"])
        mail = {}
        mfrom = [header["value"] for header in msg["payload"]
                 ["headers"] if header["name"] == 'From']
        subject = [header["value"] for header in msg["payload"]
                   ["headers"] if header["name"] == 'Subject']
        mail["messageId"] = msg["id"]
        mail["From"] = mfrom[0]
        mail["Subject"] = subject[0]
        mail["attachment"] = msg["payload"]["parts"][1]["filename"]
        mail["attachmentId"] = msg["payload"]["parts"][1]["body"]["attachmentId"]
        mails.append(mail)
        print(mail)
        att = service.users().messages().attachments().get(
            userId='me', messageId=mail["messageId"], id=mail["attachmentId"]).execute()
        # print(att)
        data = att['data']
        file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
        path = mail["attachment"]

        with open(path, 'wb') as f:
            f.write(file_data)
        break
    # print(mails)
    # print(results)


if __name__ == '__main__':
    main()
