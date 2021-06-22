import os
import warnings
from os.path import join

import pandas as pd  # type: ignore
from pandas.core.frame import DataFrame  # type: ignore


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
    SAVE_FOLDER = "att_files"
    # crawl_excel_files(QUERY_STRING,SAVE_FOLDER)

    df = get_trade_data(SAVE_FOLDER)
    print(df)


if __name__ == "__main__":
    main()
