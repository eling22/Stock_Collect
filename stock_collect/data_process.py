import json
import os
import warnings
from os.path import join
from typing import Any

import pandas as pd  # type: ignore
from pandas.core.frame import DataFrame  # type: ignore


def get_dataframe_from_excel(save_folder: str, save_excel: bool = False) -> DataFrame:
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


def filter_for_database(df: DataFrame) -> DataFrame:
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
    df = df.rename(columns=target_columns_dict)
    df = df.replace("現買", "buy")
    df = df.replace("現賣", "sell")
    df = df.filter(items=target_columns_list)
    return df


def dump_json(df: DataFrame) -> Any:
    result = df.to_json(orient="index", force_ascii=False)
    json_data = json.loads(result)
    return json_data


def get_json_from_excel(save_folder: str, save_excel: bool = False) -> Any:
    df = get_dataframe_from_excel(save_folder, save_excel)
    df = filter_for_database(df)
    json_data = dump_json(df)
    return json_data
