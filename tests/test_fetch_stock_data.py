from stock_collect.database.database import DataBase
from stock_collect.fetch_stock_data.stock_price import StockPrice


def test_stock_price():
    stock = StockPrice()
    stock.run()


def test_update_stock_price():
    db = DataBase()
    stock = StockPrice()
    # TODO: get the list od stock id from user's data
    list_of_all_stock = []
    stock.update(db, list_of_all_stock)
