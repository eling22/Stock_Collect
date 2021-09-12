from pandas.core.frame import DataFrame
from pandas.core.series import Series
from pandas.core.tools.datetimes import to_datetime
from stock_collect.database.database import DataBase
import yfinance as yf
from datetime import date, datetime
from rich import print
import datetime as dt


def str_to_datatime(time: str, format: str = "%Y%m%d") -> date:
    return dt.datetime.strptime(str(time), format).date()


def datatime_to_str(time: date, format: str = "%Y%m%d") -> str:
    return time.strftime(format)


def test_div():
    stock_id = "2330"
    stock_info = yf.Ticker(f"{stock_id}.TW")
    USER_UID = "z1KBIEE1QFXYzB2lE6f5hI9ArfR2"
    db = DataBase(USER_UID)

    # get my trade data
    trade_data_df = db.get_trade_data_by_stock_id(stock_id)
    ch_name = trade_data_df["ch_name"].iloc[0]
    print(trade_data_df)

    # get stock dividend(div) data
    start_date = str_to_datatime(trade_data_df["date"].iloc[0])
    end_data = datetime.now()  # end_date will not be counted
    df = stock_info.history(start=start_date, end=end_data)
    print(df)

    # turn my div data to my trade data format
    div_df: DataFrame = stock_info.dividends.to_frame()
    div_df = div_df.reset_index(level=["Date"])
    div_df["Date"] = div_df["Date"].dt.strftime("%Y%m%d")
    div_df = div_df.rename(columns={"Date": "date", "Dividends": "price"})
    div_df["trade_type"] = "dividend"
    div_df["code"] = stock_id
    div_df["ch_name"] = ch_name
    print(div_df)

    # put div data to my trade data
    trade_data_df = trade_data_df.append(div_df).fillna(0)
    print(trade_data_df)

    # calculate the num of each div data

    # put the div data to database
