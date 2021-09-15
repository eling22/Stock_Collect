from pandas.core.frame import DataFrame
from pandas.core.series import Series
from pandas.core.tools.datetimes import to_datetime
from stock_collect.database.database import DataBase
import yfinance as yf
from datetime import date, datetime
from rich import print
import datetime as dt
import math
import numpy as np


def str_to_datatime(time: str, format: str = "%Y%m%d") -> date:
    return dt.datetime.strptime(str(time), format).date()


def datatime_to_str(time: date, format: str = "%Y%m%d") -> str:
    return time.strftime(format)

    df["ch_name"] = ch_name


def stock_property_to_df(
    trade_type: str, prop: Series, stock_id: str, ch_name: str
) -> DataFrame:
    df: DataFrame = prop.to_frame()
    df = df.reset_index(level=["Date"])
    df["Date"] = df["Date"].dt.strftime("%Y%m%d").astype(int)
    df = df.rename(columns={"Date": "date"})
    df["trade_type"] = trade_type
    df["code"] = stock_id
    df["ch_name"] = ch_name
    return df


def calculate_div_split(df: DataFrame) -> DataFrame:
    stock_num = 0
    split_date = 0
    split_num = 0
    for idx, row in df.iterrows():
        if split_date < row["date"]:
            stock_num += split_num
            split_num = 0
        if row["trade_type"] == "buy":
            stock_num += row["num"]
        elif row["trade_type"] == "sell":
            stock_num -= row["num"]
        elif row["trade_type"] == "dividend":
            df.at[idx, "num"] = stock_num
            df.at[idx, "price"] = row["dividend"]
        elif row["trade_type"] == "split":
            split_num = math.floor(stock_num * (row["split"] - 1))
            df.at[idx, "num"] = split_num
            split_date = row["date"]
    return df


def test_div():
    # stock_id = "2330"
    stock_id = "2884"
    stock_info = yf.Ticker(f"{stock_id}.TW")
    USER_UID = "z1KBIEE1QFXYzB2lE6f5hI9ArfR2"
    db = DataBase(USER_UID)

    # get my trade data
    trade_data_df = db.get_trade_data_by_stock_id(stock_id)
    ch_name = trade_data_df["ch_name"].iloc[0]
    # print(trade_data_df)

    # get stock data
    start_date = str_to_datatime(trade_data_df["date"].iloc[0])
    end_data = datetime.now()  # end_date will not be counted
    df = stock_info.history(start=start_date, end=end_data)
    # print(df)

    # turn dividend(div) & split data to my trade data format
    div_df = stock_property_to_df("dividend", stock_info.dividends, stock_id, ch_name)
    split_df = stock_property_to_df("split", stock_info.splits, stock_id, ch_name)

    # put div & split data to my trade data
    trade_data_df = trade_data_df.append(div_df).append(split_df).fillna(0)
    trade_data_df = trade_data_df.sort_values(by=["date"])
    trade_data_df = trade_data_df.reset_index(drop=True)
    trade_data_df = trade_data_df.rename(
        columns={"Stock Splits": "split", "Dividends": "dividend"}
    )
    print(trade_data_df)

    # calculate the num of each div & split data
    trade_data_df = calculate_div_split(trade_data_df)
    print(trade_data_df)

    # put the div data to database
