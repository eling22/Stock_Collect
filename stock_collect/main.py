from stock_collect.message import crawl_excel_files
import pandas
import warnings


def main():
    # the search string for only show the email with the string
    QUERY_STRING = "fugletrade 交易明細"
    # crawl_excel_files(QUERY_STRING)
    
    warnings.simplefilter("ignore")
    x = pandas.read_excel("att_files\\交易明細20190125.xlsx",sheet_name='交易明細')
    warnings.simplefilter("default")
    
    print(x)
    


if __name__ == "__main__":
    main()
