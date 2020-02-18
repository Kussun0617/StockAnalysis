import pandas as pd

class List:
    def __init__(self,file_name):
        self.file_name = file_name

    def readAsDataFrame(self):
        return self.df =　pd.read_csv(self.file_name)

    def writeToCSV(self, file_name):
        self.df.to_csv(file_name)
