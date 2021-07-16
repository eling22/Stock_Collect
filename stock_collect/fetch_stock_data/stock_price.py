import twstock  # type: ignore
from rich import print

from stock_collect.database.database import DataBase


class StockPrice:
    def __init__(self) -> None:
        pass

    def run(self):
        stock_id = "8299"
        stock = twstock.Stock(stock_id)
        data = stock.fetch_31()
        x = {d.date.strftime("%Y%m%d"): dict(d._asdict()) for d in data}

        db = DataBase()
        db.add_stock_data(stock_id, x)

        # data = stock.fetch_from(2000, 5)
        print(x)
