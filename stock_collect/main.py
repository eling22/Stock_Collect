from multiprocessing.pool import ThreadPool

from rich import print

from stock_collect.message import Message

from .gmail_service import GmailService


def get_message(msg):
    id = msg["id"]
    return Message(id)


def main():
    # the search string for only show the email with the string
    QUERY_STRING = "玉山證券經紀本部"

    gmail = GmailService()
    msg_list = gmail.get_all_message_id_list(q=QUERY_STRING)
    print(f"crawl {len(msg_list)} files")
    data = [{"gmail": gmail, "id": msg["id"]} for msg in msg_list]

    with ThreadPool(5) as p:
        p.map(get_message, data)

    # for msg in msg_list:
    #     id = msg["id"]
    #     msg = Message(gmail, id)
    #     break


if __name__ == "__main__":
    main()
