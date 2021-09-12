import datetime as dt
from collections import defaultdict
from copy import deepcopy
from multiprocessing.pool import ThreadPool
from typing import Any, DefaultDict, Dict, Tuple

import matplotlib.dates as mdates  # type: ignore
import matplotlib.pylab as plt  # type: ignore
from matplotlib.ticker import FormatStrFormatter
from pandas.core.frame import DataFrame  # type: ignore
from rich import print
from rich.progress import track

from stock_collect.database.database import DataBase
from tests.stock_inventory import StockInventory

MoneyData = defaultdict[Any, int]
StockData = Dict[str, StockInventory]
ValueData = defaultdict[Any, int]


def get_money_and_stock_data(df: DataFrame) -> Tuple[MoneyData, StockData]:
    money_data: MoneyData = defaultdict(int)
    stock_data: StockData = {}
    stock = StockInventory()
    money = 0.0
    for x in track(df.values):
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
        stock.update_date(date)
        stock.update_cash(money)
        money_data[date] = int(money)
        stock_data[date] = deepcopy(stock)
    return money_data, stock_data


def get_value_data(stock_data: StockData) -> ValueData:
    value_data = defaultdict(int)
    with ThreadPool(100) as p:

        def func(data):
            stock: StockInventory
            date: dt.datetime
            date, stock = data
            money = stock.to_money()
            return (date, money)

        res = p.map(func, stock_data.items())
        print("finish")
        for date, money in res:
            value_data[date] = money
    return value_data


def plot_the_view(money_data: MoneyData, value_data: ValueData):
    def plot(data: DefaultDict):
        lists = sorted(data.items())
        x, y = zip(*lists)
        plt.plot(x, y)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y/%m/%d"))
    plt.gca().yaxis.set_major_formatter(FormatStrFormatter("%d"))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=90))
    plot(money_data)
    plot(value_data)
    plt.gcf().autofmt_xdate()
    plt.show()


def test_draw_trade_data_view():
    # the search string for only show the email with the string
    USER_UID = "z1KBIEE1QFXYzB2lE6f5hI9ArfR2"

    db = DataBase(USER_UID)
    df = db.get_trade_data()
    # df.to_csv("trade_data.csv")
    print(df)
    money_data, stock_data = get_money_and_stock_data(df)
    value_data = get_value_data(stock_data)

    plot_the_view(money_data, value_data)
