class WeeksInDatabase:

    @classmethod
    def get_all_weeks(self):
        weeks = dict()
        weeks[2012] = range(1,14)
        weeks[2013] = range(1,12)
        return weeks

    def __init__(self):
        self.weeks = dict()

    def add_weeks(self,year,weeks):
        self.weeks[year] = weeks

    def get_weeks(self):
        return self.weeks
