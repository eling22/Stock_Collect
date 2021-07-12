import warnings

import firebase_admin  # type: ignore
from firebase_admin import credentials, firestore
from rich import print
from rich.progress import track

from .fetch_trade_data.data_process import get_json_from_excel
from .fetch_trade_data.message import crawl_excel_files


def main():

    # the search string for only show the email with the string
    QUERY_STRING = "fugletrade 交易明細"
    SAVE_FOLDER = "att_files"
    crawl_excel_files(QUERY_STRING, SAVE_FOLDER)

    data = get_json_from_excel(SAVE_FOLDER)

    cred = credentials.Certificate("stock-collect-firebase-adminsdk.json")
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    query = (
        db.collection("eileen_trade_data")
        .order_by("date", direction=firestore.Query.DESCENDING)
        .limit(1)
    )
    docs = query.stream()

    try:
        warnings.simplefilter("ignore", ResourceWarning)
        for doc in docs:
            lastest_update = doc.to_dict()["date"]
    except StopIteration:
        lastest_update = 0
    print("lastest_update", lastest_update)

    data = {k: v for k, v in data.items() if v["date"] > lastest_update}

    print(f"add {len(data)} data to database")
    for key, value in track(data.items(), description="Upload data..."):
        db.collection("eileen_trade_data").add(value)


if __name__ == "__main__":
    main()
