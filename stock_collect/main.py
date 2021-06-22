from multiprocessing import Lock
from multiprocessing.pool import ThreadPool

from rich import print
from rich.progress import Progress

from stock_collect.message import Message

from .gmail_service import GmailService


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
    QUERY_STRING = "fugletrade 交易明細"

    gmail = GmailService()
    msg_list = gmail.get_all_message_id_list(q=QUERY_STRING)
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


if __name__ == "__main__":
    main()
