#!/usr/local/bin/python3

import pandas as pd
# import quandl
import datetime
import os
import pandas_datareader.data as web
import sys

# TODO: pass in api key as function/module parameter
# Needed for get requests of data
API_KEY = "J8PMIN9JGW4WQGIR"
value = os.getenv(API_KEY)


def days_to_subtract(num_years, days_in_year=365):
    """

    TODO: May want to align this with company quarterly or annual financial statement
          releases
    """
    # TODO, check for leap year
    return num_years * days_in_year


start = datetime.date.today() - datetime.timedelta(days=days_to_subtract(4))
end = datetime.date.today()

stock = "AAPL"


def get_historical_stock_data(ticker, start=start, end=end, api_key=API_KEY):
    """
    """
    data = web.DataReader(ticker,
                          "av-daily-adjusted",
                          start=start,
                          end=end,
                          api_key=API_KEY)

    return data


def get_sector_performance(ticker_sector):
    """
    """
    return


stock_data = get_historical_stock_data(stock)
