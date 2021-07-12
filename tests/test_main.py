from stock_collect.database.database import DataBase
from stock_collect.fetch_trade_data.data_process import (dump_json,
                                                         get_df_from_excel)
from stock_collect.fetch_trade_data.message import crawl_excel_files


def test_crawl_data():
    QUERY_STRING = "fugletrade 交易明細"
    SAVE_FOLDER = "att_files"
    crawl_excel_files(QUERY_STRING, SAVE_FOLDER)


def test_main():
    # the search string for only show the email with the string
    SAVE_FOLDER = "att_files"
    USER_UID = "z1KBIEE1QFXYzB2lE6f5hI9ArfR2"

    df = get_df_from_excel(SAVE_FOLDER)
    df.to_csv("trade_data.csv")
    data = dump_json(df)

    db = DataBase(USER_UID)
    db.add_trade_data(data)
