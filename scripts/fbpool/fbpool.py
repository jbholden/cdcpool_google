ROOT_PATH = '../../.'
import sys
sys.path.append(ROOT_PATH)

import argparse
from scripts.api.fbpool_api import *
from scripts.api.fbpool_api_exception import *
from scripts.excel.pool_spreadsheet import *
from scripts.excel.team import *
from fbpool_args import *

class FBPool:
    def __init__(self,url,excel_dir):
        self.url = url
        self.excel_dir = excel_dir

    def __excel_filename(self,year):
        filename = "%s/pool_%d_standings.xlsm" % (self.excel_dir,year)
        return filename

    def load_teams(self,year):
        excel = PoolSpreadsheet(year,self.__excel_filename(year))
        teams = excel.get_teams()

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            for team in teams:
                fbpool_api.createTeam(team.name,team.conference)
        except FBAPIException as e:
            print "**ERROR** Encountered error when loading teams"
            print "---------------------------------------------"
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            print "Database data may be in an invalid state."
            print ""
            sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="load, edit, and query the football pool database ")

    parser.add_argument("-l","--load",
                        type=str,
                        action="store",
                        help="loads data from an excel file into the database")

    parser.add_argument("-u","--url",
                        type=str,
                        action="store",
                        default="http://localhost:10090",
                        help="specify the base url of the database to load")

    parser.add_argument("-y","--year",
                        type=int,
                        action="store",
                        help="specify the year")

    parser.add_argument("-d","--excel_dir",
                        type=str,
                        action="store",
                        default="../data",
                        help="directory where the excel files are located")

    args = parser.parse_args()

    fbpool = FBPool(url=args.url,excel_dir=args.excel_dir)

    import pdb; pdb.set_trace()
    print "load=%s" % (args.load)

    #if args.load == "teams":
        #fbpool.load_teams(2013)
