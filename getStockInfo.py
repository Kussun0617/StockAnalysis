from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import datetime
import time

class List:
    def __init__(self,file_name):
        self.file_name = file_name

class StockList(List):
    def getDataFrame(self,df):
        self.df = df
        self.code_column_num = 1
        self.name_column_num = 2
        self.sector_column_num = 4
        self.stock_column_num = 6

class Portfolio(List):
    values = []

    def setColumns(self):
        self.columns = [
        "code",
        "name",
        "sector",
        "shocks",
        "stock price",
        "asset per company",
        "dividend yield",
        "PER",
        "PBR",
        "sales",
        "operation income",
        "operation margin",
        "current ratio",
        "dividend",
        "payout ratio"
        ]

    def setDataFrame(self):
        self.df = pd.DataFrame(self.values, columns = self.columns)
        date_info = datetime.date.today().strftime("%Y%m%d")
        self.file_name = "{}_portfolio.csv".format(date_info)

    # def setFromStockList(self, code, name, sector, stock):
    #     self.code = code
    #     self.name = name
    #     self.sector = sector
    #     self.stock = stocks

class Html:
    def __init__(self):
        self.class_name = "TextLabel__text-label___3oCVw TextLabel__black___2FN-Z TextLabel__regular___2X0ym digits MarketsTable-value-FP5ul"
        self.price_index = 0
        self.dividend_index = 32
        self.PER_index = 41
        self.PBR_index = 51
        self.dividend_yield_index = 60
        self.current_ratio_index = 63
        self.payout_ratio_index = 66
        self.operation_margin_index = 82
        self.sale_index = 129
        self.operation_income_index = 133

    def setCode(self, code):
        self.code = code

    def setSoup(self):
        url = "https://jp.reuters.com/companies/{}.T/key-metrics" .format(self.code)
        r = requests.get(url)
        self.soup = BeautifulSoup(r.text, "html.parser")

    def setAllValues(self, all_values):
        self.all_values = all_values

    def setEachValue(self, price, dividend, PER, PBR, dividend_yield, current_ratio, payout_ratio, operation_margin,sales, operation_income):
        self.price = price
        self.dividend = dividend
        self.PER = PER
        self.PBR = PBR
        self.dividend_yield = dividend_yield
        self.current_ratio = current_ratio
        self.payout_ratio = payout_ratio
        self.operation_margin = operation_margin
        self.sales = sales
        self.operation_income = operation_income

    def replaceStockPrice(self, price):
        return price.replace(",","")

stock_list = StockList("stock_list.csv")
stock_list.getDataFrame(pd.read_csv(stock_list.file_name))

portfolio = Portfolio("portfolio.csv")
stock_info = Html()
# price_column = [
# "stock price"
# ]
#
# financial_statements_list = [
# "Sales/last year",
# "operation income",
# "operation margin",
# "current ratio",
# "dividend"
# ]

for i in range(len(stock_list.df)):
    stock_info.setCode(stock_list.df.iloc[i,stock_list.code_column_num])
    stock_info.setSoup()

    print(stock_info.soup.title.text)

    stock_info.setAllValues(
        stock_info.soup.find_all("span",{"class":{stock_info.class_name}})
        )

    stock_info.setEachValue(
        stock_info.all_values[stock_info.price_index].get_text(),
        stock_info.all_values[stock_info.dividend_index].get_text(),
        stock_info.all_values[stock_info.PER_index].get_text(),
        stock_info.all_values[stock_info.PBR_index].get_text(),
        stock_info.all_values[stock_info.dividend_yield_index].get_text(),
        stock_info.all_values[stock_info.current_ratio_index].get_text(),
        stock_info.all_values[stock_info.payout_ratio_index].get_text(),
        stock_info.all_values[stock_info.operation_margin_index].get_text(),
        stock_info.all_values[stock_info.sale_index].get_text(),
        stock_info.all_values[stock_info.operation_income_index].get_text(),
    )

    values = []
    try:
        if stock_info.price.find(",") != -1:
            stock_info.price = stock_info.replaceStockPrice(stock_info.price)
        print(stock_info.price)

        my_asset = int(stock_list.df.iloc[i,stock_list.stock_column_num])*float(stock_info.price)

        values = [
        stock_list.df.iloc[i,stock_list.code_column_num],
        stock_list.df.iloc[i,stock_list.name_column_num],
        stock_list.df.iloc[i,stock_list.sector_column_num],
        stock_list.df.iloc[i,stock_list.stock_column_num],
        stock_info.price,
        my_asset,
        stock_info.PER,
        stock_info.PBR,
        stock_info.dividend_yield,
        stock_info.sales,
        stock_info.operation_income,
        stock_info.operation_margin,
        stock_info.current_ratio,
        stock_info.dividend,
        stock_info.payout_ratio
        ]

        portfolio.values.append(values)
    except IndexError:
        print ("could not get stock info")

portfolio.setDataFrame()
portfolio.df.to_csv(portfolio.file_name)

print("Well Done!!")
