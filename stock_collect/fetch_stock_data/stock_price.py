from datetime import datetime
from typing import List, Optional

import yfinance as yf  # type: ignore

from stock_collect.database.database import DataBase


class StockPrice:
    def __init__(self, db: DataBase) -> None:
        self.db = db
        self.start_date = datetime(2000, 1, 1)

    def update(self, list_of_all_stock: List[str], start_date: datetime):
        exist_stock = self.db.get_record_stock_id_list()

        for stock_id in list_of_all_stock:
            if stock_id in exist_stock:
                last_update_time_str = self.db.get_last_update_time(stock_id)
                last_update_time = datetime.strptime(last_update_time_str, "%Y%m%d")
                self.fetch_from(stock_id, last_update_time)
            else:
                self.fetch_from(stock_id, start_date)

    def fetch_from(self, stock_id: str, start_date: Optional[datetime]):
        stock = yf.Ticker(f"{stock_id}.TW")
        df = stock.history(start=start_date)
        if len(df) == 0:
            stock = yf.Ticker(f"{stock_id}.TWO")
            df = stock.history(start=start_date)

        print(df)

        data = {}
        for index, row in df.iterrows():
            time = index.strftime("%Y%m%d")
            data[time] = row.to_dict()
            data[time]["Date"] = index
        self.db.add_stock_data(stock_id, data)
