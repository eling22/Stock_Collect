import datetime as dt
from collections import defaultdict
from typing import DefaultDict, Dict


from rich import print

from stock_collect.database.database import DataBase
from stock_collect.fetch_trade_data.message import crawl_excel_files
from tests.stock_inventory import StockInventory


def test_crawl_data():
    QUERY_STRING = "fugletrade 交易明細"
    SAVE_FOLDER = "att_files"
    crawl_excel_files(QUERY_STRING, SAVE_FOLDER)


def test_get_data_from_db():
    USER_UID = "z1KBIEE1QFXYzB2lE6f5hI9ArfR2"
    db = DataBase(USER_UID)
    df = db.get_trade_data()
    print(df)


def test_enter_data_to_db():
    USER_UID = "z1KBIEE1QFXYzB2lE6f5hI9ArfR2"
    DataBase(USER_UID)
    # data = {
    #     "tax": 382,
    #     "ch_name": "台泥",
    #     "trade_type": "sell",
    #     "fee": 181,
    #     "code": "1101",
    #     "num": 3000,
    #     "price": 42.8,
    #     "date": 20200130,
    # }
    # data = {
    #     "tax": 0,
    #     "ch_name": "順天",
    #     "trade_type": "buy",
    #     "fee": 31,
    #     "code": "5525",
    #     "num": 1000,
    #     "price": 21.75,
    #     "date": 20200203,
    # }
    # data = {
    #     "tax": 711,
    #     "ch_name": "瑞昱",
    #     "trade_type": "sell",
    #     "fee": 337,
    #     "code": "2379",
    #     "num": 1000,
    #     "price": 239,
    #     "date": 20191125,
    # }
    # db.add_one_trade_data(data)
