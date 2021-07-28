import warnings
from datetime import date, datetime, timedelta
from typing import Any, Dict, List

import firebase_admin  # type: ignore
from firebase_admin import credentials, firestore
from pandas.core.frame import DataFrame  # type: ignore
from rich import print
from rich.progress import track


class DataBase:
    is_init_db: bool = False

    def __init__(self, user: str = None) -> None:
        if not DataBase.is_init_db:
            print("init_db")
            DataBase.init_db()
            DataBase.is_init_db = True
        self.db = firestore.client()
        self.user = user

    @staticmethod
    def init_db():
        cred = credentials.Certificate("stock-collect-firebase-adminsdk.json")
        firebase_admin.initialize_app(cred)

    def add_stock_data(self, stock_id: str, data: Dict[str, Dict[str, Any]]):
        for key, value in track(
            data.items(), description=f"Saving stock {stock_id} data..."
        ):
            print(key)
            (
                self.db.collection("stock")
                .document(stock_id)
                .collection("main")
                .document(key)
                .set(value)
            )
            (
                self.db.collection("stock")
                .document(stock_id)
                .set({"last_update_time": key})
            )

    def get_last_update_time(self, stock_id: str):
        doc = self.db.collection("stock").document(stock_id).get()
        if doc.exists:
            return doc.to_dict()["last_update_time"]

    def get_record_stock_id_list(self) -> List[str]:
        docs = self.db.collection("stock").stream()
        stock_id_list = []
        for doc in docs:
            stock_id_list += [str(doc.id)]
        return stock_id_list

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

    def get_stock_price(self, date: date, stock_id: str) -> float:
        date_str = date.strftime("%Y%m%d")
        doc = self.db.document(f"stock/{stock_id}/main/{date_str}").get()
        if doc.exists:
            return doc.to_dict()["Close"]
        else:
            query = (
                self.db.collection("stock")
                .document(f"{stock_id}")
                .collection("main")
                .order_by("Date")
                .limit(1)
            )
            docs = query.stream()
            oldest_record_date = datetime.now().date()
            warnings.simplefilter("ignore", ResourceWarning)
            for doc in docs:
                time: datetime = doc.to_dict()["Date"]
                oldest_record_date = time.date()
            if date < oldest_record_date:
                return 0
            one_day = timedelta(days=-1)
            return self.get_stock_price(date - one_day, stock_id)
