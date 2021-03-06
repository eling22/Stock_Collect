import os.path

from google.auth.transport.requests import Request  # type: ignore
from google.oauth2.credentials import Credentials  # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore
from googleapiclient.discovery import Resource, build  # type: ignore

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


class GmailService:
    def __init__(self) -> None:
        # self.service = GmailService()
        self.service = self.get_gmail_service()
        self.user_id = "me"

    def get_gmail_service(self) -> Resource:
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        service = build("gmail", "v1", credentials=creds)
        return service

    def get_message_list(self, q=None, pageToken=None):
        return (
            self.service.users()
            .messages()
            .list(userId=self.user_id, q=q, pageToken=pageToken)
            .execute()
        )

    def get_all_message_id_list(self, q=None, pageToken=None):
        all_msg_list = []
        msg_list = self.get_message_list(q=q, pageToken=pageToken)
        all_msg_list.extend(msg_list.get("messages", []))
        nextPageToken = msg_list.get("nextPageToken", None)
        while nextPageToken:
            print(f"crawl {len(all_msg_list)} files", end="\r")
            msg_list = self.get_message_list(q=q, pageToken=nextPageToken)
            msg_list.get("nextPageToken", None)
            all_msg_list.extend(msg_list.get("messages", None))
            nextPageToken = msg_list.get("nextPageToken", None)
        return all_msg_list

    def get_message(self, id):
        return self.service.users().messages().get(userId=self.user_id, id=id).execute()

    def get_attachment(self, message_id, attachment_id):
        return (
            self.service.users()
            .messages()
            .attachments()
            .get(userId=self.user_id, messageId=message_id, id=attachment_id)
            .execute()
        )
