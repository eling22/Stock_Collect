from typing import Dict
import firebase_admin  # type: ignore
from firebase_admin import credentials, firestore
import warnings
from rich import print
from rich.progress import track


class DataBase:
    def __init__(self) -> None:
        cred = credentials.Certificate("stock-collect-firebase-adminsdk.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def add_trade_data(self, data):
        query = (
            self.db.collection("eileen_trade_data")
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
            self.db.collection("eileen_trade_data").add(value)
