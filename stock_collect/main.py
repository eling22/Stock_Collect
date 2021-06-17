from stock_collect.message import Message

from .gmail_service import GmailService


def main():
    # the search string for only show the email with the string
    QUERY_STRING = "玉山證券經紀本部"

    gmail = GmailService()
    msg_list = gmail.get_message_list(QUERY_STRING)
    messages = msg_list.get("messages", [])
    # print(len(messages))
    for msg in messages:
        id = msg["id"]
        msg = Message(gmail, id)
        break


if __name__ == "__main__":
    main()
