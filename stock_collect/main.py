from stock_collect.database.database import DataBase
from .fetch_trade_data.data_process import get_json_from_excel
from .fetch_trade_data.message import crawl_excel_files


def main():

    # the search string for only show the email with the string
    QUERY_STRING = "fugletrade 交易明細"
    SAVE_FOLDER = "att_files"
    USER_UID = "z1KBIEE1QFXYzB2lE6f5hI9ArfR2"
    crawl_excel_files(QUERY_STRING, SAVE_FOLDER)

    data = get_json_from_excel(SAVE_FOLDER)

    db = DataBase()
    db.add_trade_data(data)


if __name__ == "__main__":
    main()
