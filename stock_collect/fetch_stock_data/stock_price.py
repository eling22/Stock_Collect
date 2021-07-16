import twstock
from rich import print


class StockPrice:
    def __init__(self) -> None:
        pass

    def run(self):
        stock = twstock.Stock("8299")
        data = stock.fetch_31()

        # data = stock.fetch_from(2000, 5)
        print(data)
