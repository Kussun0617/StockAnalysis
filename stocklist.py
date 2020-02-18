from list import List

class StockList(List):
    def getDataFrame(self,df):
        self.df = df
        self.code_column_num = 1
        self.name_column_num = 2
        self.sector_column_num = 4
        self.stock_column_num = 6
