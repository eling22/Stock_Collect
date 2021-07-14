import datetime as dt
from collections import defaultdict
from typing import DefaultDict, Dict

import matplotlib.dates as mdates
import matplotlib.pylab as plt
from matplotlib.ticker import FormatStrFormatter
from rich import print

from stock_collect.database.database import DataBase
from stock_collect.fetch_trade_data.message import crawl_excel_files
from tests.stock_inventory import StockInventory


def test_crawl_data():
    QUERY_STRING = "fugletrade 交易明細"
    SAVE_FOLDER = "att_files"
    crawl_excel_files(QUERY_STRING, SAVE_FOLDER)


def test_draw_trade_data_view():
    # the search string for only show the email with the string
    USER_UID = "z1KBIEE1QFXYzB2lE6f5hI9ArfR2"

    db = DataBase(USER_UID)
    df = db.get_trade_data()
    # df.to_csv("trade_data.csv")
    print(df)
    money_data = defaultdict(int)
    stock_data: Dict[str, DefaultDict[str, int]] = {}
    money = 0.0
    stock = StockInventory()
    for x in df.values:
        [trade_type, code, ch_name, num, price, fee, tax, date] = x
        money -= fee
        if trade_type == "buy":
            money -= num * price
            stock.add(code, num)
        else:  # sell
            money += num * price
            money -= tax
            stock.remove(code, num)
        date = dt.datetime.strptime(str(date), "%Y%m%d").date()
        money_data[date] = money
        stock_data[date] = stock.stock

    print(stock_data)

    lists = sorted(money_data.items())
    x, y = zip(*lists)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y/%m/%d"))
    plt.gca().yaxis.set_major_formatter(FormatStrFormatter("%d"))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=90))
    plt.plot(x, y)
    plt.gcf().autofmt_xdate()
    plt.show()


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
