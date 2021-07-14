from collections import defaultdict
from typing import DefaultDict


class StockInventory:
    def __init__(self) -> None:
        self.stock: DefaultDict[str, int] = defaultdict(int)

    def add(self, code, num):
        self.stock[code] += num

    def remove(self, code, num):
        self.stock[code] -= num
