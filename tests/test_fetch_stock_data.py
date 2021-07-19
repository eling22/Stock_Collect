from stock_collect.database.database import DataBase
from stock_collect.fetch_stock_data.stock_price import StockPrice
from stock_collect.fetch_trade_data.data_process import get_df_from_excel


def test_stock_price():
    stock = StockPrice()
    stock.run()


def test_update_stock_price():
    SAVE_FOLDER = "att_files"
    df = get_df_from_excel(SAVE_FOLDER)
    db = DataBase()
    stock = StockPrice(db)
    # list_of_all_stock = df["code"].drop_duplicates().tolist()
    list_of_all_stock = ["006208"]
    stock.update(list_of_all_stock)
