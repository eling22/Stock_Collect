from multiprocessing import Lock
from multiprocessing.pool import ThreadPool

from rich import print
from rich.progress import Progress

from stock_collect.message import Message

from .gmail_service import GmailService


import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("stock-collect-firebase-adminsdk-towjq-475cc7a29e.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
dest = {"name": "Eileen", "state": "Taipie", "country": "Taiwan"}
db.collection("trade_data").add(dest)


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


def main():
    # the search string for only show the email with the string
    # QUERY_STRING = "玉山證券經紀本部"

    # gmail = GmailService()
    # msg_list = gmail.get_all_message_id_list(q=QUERY_STRING)
    # print(f"crawl {len(msg_list)} files")

    # with Progress() as progress:
    #     lock = Lock()
    #     task = progress.add_task("[red]crawl...", total=len(msg_list))
    #     data = [
    #         {"lock": lock, "progress": progress, "task": task, "id": msg["id"]}
    #         for msg in msg_list
    #     ]

    #     with ThreadPool(5) as p:
    #         p.map(crawl_data, data)
    print("good")


if __name__ == "__main__":
    main()
