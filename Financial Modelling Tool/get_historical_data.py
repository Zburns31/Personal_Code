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


def get_historical_stock_data(ticker, start, end, api_key=API_KEY):
    """
    """
    data = web.DataReader(ticker,
                          "av-daily-adjusted",
                          start=start,
                          end=end,
                          api_key=API_KEY)

    return data


def get_sector_performance(ticker_sector, api_key=API_KEY):
    """ Function to retreive sector performance metrics for a given ticker

        Parameter:
            ticker_sector: Sector that a given ticker falls into
            API_KEY
    """
    # Make sure each ticker sector matches the format of the sector performance DF
    # Capitalize the first letter of each word
    ticker_sector = ticker_sector.lower().title()

    sector_performance = web.get_sector_performance_av(api_key=api_key)

    # Company sector may not match returned data sector name
    sectors = list(sector_performance.index)
    company_sector = [item for item in sectors if ticker_sector in item]

    # Select specific row (sector performance metrics) with all columns
    return sector_performance.loc[company_sector, :]


if __name__ == '__main__':
    start = datetime.date.today() - datetime.timedelta(days=days_to_subtract(4))
    end = datetime.date.today()

    stock = "AAPL"
    stock_data = get_historical_stock_data(stock)
