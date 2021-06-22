import base64
import os
from multiprocessing import Lock
from multiprocessing.pool import ThreadPool

from rich.progress import Progress

from stock_collect.gmail_service import GmailService

# can set by crawl_excel_files
SAVE_FOLDER = "att_files"


class Message:
    def __init__(self, id: str) -> None:
        self.folder_name = SAVE_FOLDER
        self.gmail = GmailService()
        self.message_id = id

    def crawl_data(self):
        self.get_message_info(self.message_id)
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
        file_name = os.path.join(self.folder_name, path)

        if os.path.exists(file_name):
            return

        try:
            with open(file_name, "wb") as f:
                f.write(file_data)
        except FileNotFoundError:
            try:
                os.makedirs(self.folder_name)
            except FileExistsError:
                pass
            with open(file_name, "wb") as f:
                f.write(file_data)
        # print(f"add {path}...", end="\r")


def crawl_data(param):
    id = param["id"]
    progress: Progress = param["progress"]
    task = param["task"]
    lock = param["lock"]

    msg = Message(id)
    msg.crawl_data()

    lock.acquire()
    progress.update(task, advance=1)
    lock.release()


def crawl_excel_files(query_str, save_folder) -> None:
    global SAVE_FOLDER
    SAVE_FOLDER = save_folder
    gmail = GmailService()
    msg_list = gmail.get_all_message_id_list(q=query_str)
    print(f"crawl {len(msg_list)} files")

    with Progress() as progress:
        lock = Lock()
        task = progress.add_task("[red]crawl...", total=len(msg_list))
        data = [
            {"lock": lock, "progress": progress, "task": task, "id": msg["id"]}
            for msg in msg_list
        ]

        with ThreadPool(5) as p:
            p.map(crawl_data, data)
