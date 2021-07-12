import warnings

import firebase_admin  # type: ignore
from firebase_admin import credentials, firestore
from rich import print
from rich.progress import track


class DataBase:
    def __init__(self, user: str) -> None:
        cred = credentials.Certificate("stock-collect-firebase-adminsdk.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.user = user

    def add_trade_data(self, data):
        query = (
            self.db.collection("trade_data")
            .document(self.user)
            .collection("trade_record")
            .order_by("date", direction=firestore.Query.DESCENDING)
            .limit(1)
        )
        docs = query.stream()

        try:
            lastest_update = 0
            warnings.simplefilter("ignore", ResourceWarning)
            for doc in docs:
                lastest_update = doc.to_dict()["date"]
        except StopIteration:
            lastest_update = 0
        print("lastest_update", lastest_update)

        data = {k: v for k, v in data.items() if v["date"] > lastest_update}

        print(f"add {len(data)} data to database")
        for key, value in track(data.items(), description="Upload data..."):
            (
                self.db.collection("trade_data")
                .document(self.user)
                .collection("trade_record")
                .add(value)
            )
