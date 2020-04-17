#!/usr/local/bin/python3
"""
This is the main module for the financial modelling tool.It serves as a script to execute any
necessary functions in order to parse or transform the data to give us the results we need
"""
# Custom module imports
import get_historical_data as ghd
import webscraper as scrp

# Standard imports
import sys
import os
import argparse


def run(args):
    """
    """
    ticker = args.ticker
    data_volume = args.years

    company_data = scrp.retrieve_stock_data(ticker)

    company_sector = company_data['Company Financial Stats'].get('Sector')
    sector_performance = ghd.get_sector_performance(company_sector)
    return sector_performance


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='python3 main.py',
                                     description="Run the financial modelling tool on a specified company")

    parser.add_argument(
        "ticker", help="Stock ticker name of the company to retrieve data for")

    parser.add_argument("years",
                        help="Number of years of company data to retrieve",
                        default=4)
    # args = parser.parse_args()
    args = parser.parse_args(['AAPL', '5'])
    print(args)

    data = run(args)
