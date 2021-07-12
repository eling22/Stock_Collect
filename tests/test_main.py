from typing import DefaultDict
from collections import defaultdict
from stock_collect.database.database import DataBase
from stock_collect.fetch_trade_data.data_process import dump_json, get_df_from_excel
from stock_collect.fetch_trade_data.message import crawl_excel_files
import matplotlib.pylab as plt
from rich import print
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, AutoMinorLocator
import datetime as dt


def test_crawl_data():
    QUERY_STRING = "fugletrade 交易明細"
    SAVE_FOLDER = "att_files"
    crawl_excel_files(QUERY_STRING, SAVE_FOLDER)


def test_draw_trade_data_view():
    # the search string for only show the email with the string
    SAVE_FOLDER = "att_files"
    USER_UID = "z1KBIEE1QFXYzB2lE6f5hI9ArfR2"

    df = get_df_from_excel(SAVE_FOLDER)
    # df.to_csv("trade_data.csv")
    print(df)
    data = defaultdict(int)
    money = 0
    for x in df.values:
        [trade_type, code, ch_name, num, price, fee, tax, date] = x
        money -= fee
        if trade_type is "buy":
            money -= num * price
        else:  # sell
            money += num * price
            money -= tax
        date = dt.datetime.strptime(str(date), "%Y%m%d").date()
        data[date] = money

    lists = sorted(data.items())
    x, y = zip(*lists)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y/%m/%d"))
    plt.gca().yaxis.set_major_formatter(FormatStrFormatter("%d"))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=90))
    plt.plot(x, y)
    plt.gcf().autofmt_xdate()
    plt.show()

    print(data)
