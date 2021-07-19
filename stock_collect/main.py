from stock_collect.database.database import DataBase

from .fetch_stock_data.stock_price import StockPrice
from .fetch_trade_data.data_process import dump_json, get_df_from_excel
from .fetch_trade_data.message import crawl_excel_files

from google.api_core.exceptions import RetryError


def main():

    # the search string for only show the email with the string
    QUERY_STRING = "fugletrade 交易明細"
    SAVE_FOLDER = "att_files"
    USER_UID = "z1KBIEE1QFXYzB2lE6f5hI9ArfR2"
    crawl_excel_files(QUERY_STRING, SAVE_FOLDER)

    df = get_df_from_excel(SAVE_FOLDER)
    df.to_csv("trade_data.csv")
    data = dump_json(df)

    db = DataBase(USER_UID)
    db.add_trade_data(data)

    stock = StockPrice(db)

    try:
        list_of_all_stock = df["code"].drop_duplicates().tolist()
        stock.update(list_of_all_stock)
    except RetryError:
        print("today's quotas is reached, please run tomorrow")


if __name__ == "__main__":
    main()
