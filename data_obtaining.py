from datetime import date
from datetime import timedelta

from wwo_hist import retrieve_hist_data

import os
os.chdir(".\csv_files")

# interval in hours
FREQUENCY = 1
# days to look back from current date (including the current day)
DAYS = 5

START_DATE = (date.today() - timedelta(days=DAYS - 1)).strftime("%d-%b-%Y").upper()
END_DATE = date.today().strftime("%d-%b-%Y").upper()

#here goes your api key
API_KEY = 'your token here'
LOCATION_LIST = ['moscow']

hist_weather_data = retrieve_hist_data(API_KEY,
                                LOCATION_LIST,
                                START_DATE,
                                END_DATE,
                                FREQUENCY,
                                location_label = False,
                                export_csv = True,
                                store_df = True)