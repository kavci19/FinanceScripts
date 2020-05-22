class stockID:

    def __init__(self, quote):

        self.open = quote[0]
        self.close = quote[1]
        self.high = 0
        self.low = 0

    def isUpward(self):

        return self.close > self.open

    def isDownwardOrEqual(self):

        return self.close <= self.open

    def halfMark(self):

        buffer = (self.close - self.open) * 0.1
        return self.open + ((self.close - self.open) / 2) - buffer

    def isQuarterGrowthPlus(self, previous):

        minGrowth = (previous.open - previous.close) / 2

        if (self.close >= previous.open + minGrowth):
            return True

        else:
            return False
