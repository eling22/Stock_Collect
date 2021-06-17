import base64
import os

from rich import print

from stock_collect.gmail_service import GmailService


class Message:
    def __init__(self, gmail: GmailService, id: str) -> None:
        self.folder_name = "att_files"
        self.gmail = gmail
        self.message_id = id
        self.get_message_info(self.message_id)
        # attachment_id get from get_message_info
        self.get_att_info(self.message_id, self.attachment_id)

    def get_message_info(self, id):
        msg = self.gmail.get_message(id)
        headers = msg["payload"]["headers"]
        headers = {h["name"]: h["value"] for h in headers}
        self.source = headers["From"]
        self.subject = headers["Subject"]
        self.attachment_name = msg["payload"]["parts"][1]["filename"]
        self.attachment_id = msg["payload"]["parts"][1]["body"]["attachmentId"]

    def get_att_info(self, msg_id: str, att_id: str):
        att = self.gmail.get_attachment(msg_id, att_id)
        data = att["data"]
        self.save_data_to_file(data)

    def save_data_to_file(self, data):
        file_data = base64.urlsafe_b64decode(data.encode("UTF-8"))
        path = self.attachment_name
        file_name = self.folder_name + "\\" + path

        if os.path.exists(file_name):
            return

        try:
            with open(file_name, "wb") as f:
                f.write(file_data)
        except FileNotFoundError:
            os.makedirs(self.folder_name)
            with open(file_name, "wb") as f:
                f.write(file_data)
        print(f"add {path}...")
