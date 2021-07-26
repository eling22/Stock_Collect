from datetime import datetime
from stock_collect.database.database import DataBase
from stock_collect.fetch_stock_data.stock_price import StockPrice
from stock_collect.fetch_trade_data.data_process import get_df_from_excel
from stock_collect.fetch_trade_data.data_process import dump_json, get_df_from_excel
from google.api_core.exceptions import RetryError
from typing import Dict, Any, List


class MockDataBase:
    def add_stock_data(self, stock_id: str, data: Dict[str, Dict[str, Any]]):
        print("add stock data to db")
        ldata = list(data.items())
        print(ldata[0])
        print(ldata[-1])

    def get_record_stock_id_list(self) -> List[str]:
        return []

    def get_last_update_time(self, stock_id: str):
        return "20190101"


def patch_database(mocker):
    mdb = MockDataBase()
    database = "stock_collect.database.database.DataBase."
    mocker.patch(database + "add_stock_data", mdb.add_stock_data)
    mocker.patch(database + "get_record_stock_id_list", mdb.get_record_stock_id_list)
    mocker.patch(database + "get_last_update_time", mdb.get_last_update_time)


def test_parse_stock_data(mocker):
    SAVE_FOLDER = "att_files"
    start_date = datetime(2019, 1, 1)
    patch_database(mocker)
    df = get_df_from_excel(SAVE_FOLDER)
    db = DataBase()
    stock = StockPrice(db)
    try:
        list_of_all_stock = df["code"].drop_duplicates().tolist()
        stock.update(list_of_all_stock, start_date)
    except RetryError:
        print("today's quotas is reached, please run tomorrow")
