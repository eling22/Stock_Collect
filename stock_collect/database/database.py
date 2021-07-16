import warnings
from typing import Any, Dict

import firebase_admin  # type: ignore
from firebase_admin import credentials, firestore
from pandas.core.frame import DataFrame  # type: ignore
from rich import print
from rich.progress import track


class DataBase:
    def __init__(self, user: str = None) -> None:
        cred = credentials.Certificate("stock-collect-firebase-adminsdk.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.user = user

    def add_stock_data(self, stock_id: str, data: Dict[str, Dict[str, Any]]):
        for key, value in track(data.items(), description="Upload stock data..."):
            (
                self.db.collection("stock")
                .document(stock_id)
                .collection("main")
                .document(key)
                .set(value)
            )

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

    def add_one_trade_data(self, data):
        self.db.collection("trade_data").document(self.user).collection(
            "trade_record"
        ).add(data)

    def get_trade_data(self) -> DataFrame:
        query = (
            self.db.collection("trade_data")
            .document(self.user)
            .collection("trade_record")
            .order_by("date")
        )
        docs = query.stream()

        df = DataFrame(
            columns=[
                "trade_type",
                "code",
                "ch_name",
                "num",
                "price",
                "fee",
                "tax",
                "date",
            ]
        )
        for doc in docs:
            df = df.append(doc.to_dict(), ignore_index=True)
        return df
