import os
import warnings
from os.path import join

import firebase_admin  # type: ignore
import pandas as pd  # type: ignore
from firebase_admin import credentials, firestore
from pandas.core.frame import DataFrame  # type: ignore

from .message import crawl_excel_files
from rich import print


def get_trade_data(save_folder: str, save_excel: bool = False) -> DataFrame:
    df_list = []
    warnings.simplefilter("ignore")
    for f in os.listdir(save_folder):
        path = join(save_folder, f)
        df = pd.read_excel(path, sheet_name="交易明細", converters={"代碼": str})
        df_list.append(df)
    warnings.simplefilter("default")
    df = pd.concat(df_list).fillna(0)

    if save_excel:
        with pd.ExcelWriter("trade_data.xlsx") as writer:
            df.to_excel(writer, index=False)
    return df


def main():
    # the search string for only show the email with the string
    QUERY_STRING = "fugletrade 交易明細"
    SAVE_FOLDER = "att_files"
    # crawl_excel_files(QUERY_STRING, SAVE_FOLDER)

    df = get_trade_data(SAVE_FOLDER)
    print(df)
    df = df.reset_index(drop=True)
    target_columns_dict = {
        "交易別": "trade_type",
        "代碼": "code",
        "商品名稱": "ch_name",
        "成交股數": "num",
        "成交單價": "price",
        "手續費": "fee",
        "交易稅": "tax",
        "交易日期": "date",
    }
    target_columns_list = [en_name for ch_name, en_name in target_columns_dict.items()]
    print(target_columns_list)
    df = df.rename(columns=target_columns_dict)
    df = df.replace("現買", "buy")
    df = df.replace("現賣", "sell")
    df = df.filter(items=target_columns_list)
    print(df)
    # print(df.to_json(orient="index"))

    # cred = credentials.Certificate(
    #     "stock-collect-firebase-adminsdk.json"
    # )
    # firebase_admin.initialize_app(cred)

    # db = firestore.client()
    # dest = {"name": "Eileen", "state": "Taipie", "country": "Taiwan"}
    # db.collection("trade_data").add(dest)


if __name__ == "__main__":
    main()
