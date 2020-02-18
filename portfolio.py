from list import List

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

    def drawPortfolio():
