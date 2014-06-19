import argparse
import os

class FBPoolArgs:

    def __init__(self):
        self.__setup_args()
        self.__excel_files = self.__get_excel_files()

    def get_action(self):
        if self.args.load == "teams" and self.args.year:
            return "load_teams_in_year"
        elif self.args.load == "teams":
            return "load_teams_most_recent_year"
        elif self.args.load == "players" and self.args.year:
            return "load_players_in_year"
        elif self.args.load == "players":
            return "load_players_all_years"
        elif self.args.load == "week" and self.args.year and self.args.week:
            return "load_week"
        elif self.args.load == "year" and self.args.year:
            return "load_year"

    def get_url(self):
        if self.args.port != None:
            return self.args.url + ":" + str(self.args.port)
        return self.args.url

    def get_args(self):
        return self.args

    def __setup_args(self):
        parser = argparse.ArgumentParser(description="load, edit, and query the football pool database ")
        parser.add_argument("-l","--load",
                            type=str,
                            action="store",
                            help="loads data from an excel file into the database")

        parser.add_argument("-u","--url",
                            type=str,
                            action="store",
                            default="http://localhost",
                            help="specify the base url of the database to load")

        parser.add_argument("-p","--port",
                            type=int,
                            action="store",
                            help="specify the http port number of the database to load")
    
        parser.add_argument("-y","--year",
                            type=int,
                            action="store",
                            help="specify the year")

        parser.add_argument("-w","--week",
                            type=int,
                            action="store",
                            help="specify the week number")
    
        parser.add_argument("-d","--excel_dir",
                            type=str,
                            action="store",
                            default="../data",
                            help="directory where the excel files are located")

        self.args = parser.parse_args()

    def __parse_excel_filename(self,filename):
        file_ext = filename.split(".")
        if file_ext == None or len(file_ext) != 2:
            return None

        name = file_ext[0]
        extension = file_ext[1]

        not_excel_file = extension not in [ ".xls", ".xlsm" ]
        if not_excel_file:
            return None

        pool_year_standing = name.split("_")
        if pool_year_standing == None or len(pool_year_standing) != 3:
            return None

        try:
            year = int(pool_year_standing[1])
        except ValueError:
            return None

        need_to_adjust_year = year < 100
        if need_to_adjust_year:
            year += 1900

        return year

    def __get_excel_files(self):
        extensions = [ ".xls", ".xlsm" ]
        files = os.listdir(self.args.excel_dir)

        pool_files = []
        for filename in files:
            year = self.__parse_excel_filename(filename)
            if year != None:
                pool_files[year] = filename
        return pool_files

    def get_latest_pool_file_and_year(self):
        years = self.__excel_files.keys()
        if years == None or len(years) == 0:
            print "**ERROR!** could not find any excel pool files"
            sys.exit(1)
        years_sorted = sorted(years,reverse=True)
        last_year = years_sorted[0]
        return last_year,self.__excel_files[last_year]

    def get_excel_file(self,year):
        years = self.__excel_files.keys()
        if years == None or len(years) == 0:
            print "**ERROR!** could not find any excel pool files"
            sys.exit(1)
        if year not in years:
            print "**ERROR!** could not find any excel file for year %d" % (year)
            sys.exit(1)
        return self.__excel_files[year]

    def get_excel_files(self):
        return self.__excel_files

    def get_years(self):
        return self.__excel_files.keys()
        


