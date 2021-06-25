import firebase_admin  # type: ignore
from firebase_admin import credentials, firestore
from rich import print

from .data_process import get_json_from_excel
from .message import crawl_excel_files


def main():
    # the search string for only show the email with the string
    QUERY_STRING = "fugletrade 交易明細"
    SAVE_FOLDER = "att_files"
    # crawl_excel_files(QUERY_STRING, SAVE_FOLDER)

    data = get_json_from_excel(SAVE_FOLDER)
    print(data["0"])

    # cred = credentials.Certificate("stock-collect-firebase-adminsdk.json")
    # firebase_admin.initialize_app(cred)

    # db = firestore.client()
    # dest = {"name": "Eileen", "state": "Taipie", "country": "Taiwan"}
    # db.collection("trade_data").add(dest)


if __name__ == "__main__":
    main()
