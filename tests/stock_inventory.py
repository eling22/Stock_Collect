from collections import defaultdict
from datetime import datetime
from stock_collect.database.database import DataBase
from typing import DefaultDict

from numpy import float_power


class StockInventory:
    def __init__(self) -> None:
        self.stock: DefaultDict[str, int] = defaultdict(int)
        self.date: datetime
        self.cash: float

    def update_date(self, date: datetime):
        self.date = date

    def update_cash(self, cash: float):
        self.cash = cash

    def add(self, code, num):
        self.stock[code] += num

    def remove(self, code, num):
        self.stock[code] -= num

    def to_money(self):
        money: float = 0.0
        db = DataBase()
        for stock_id, num in self.stock.items():
            price = db.get_stock_price(self.date, stock_id)
            money += price * num
        return money + self.cash
