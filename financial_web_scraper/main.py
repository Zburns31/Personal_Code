"""
This is the main module for the financial modelling tool.It serves as a script to execute any
necessary functions in order to parse or transform the data to give us the results we need
"""
# Standard imports
# import sys
import os
import argparse
import json
import pandas as pd
import subprocess

# import re

# Custom module imports
import get_historical_data as ghd
import yfinance_webscraper as yfin_scrp
import tmx_webscraper as tmx_scrp
import fin_statements as fin
import wacc as wacc
from dashboard import run_dashboard

FRED_API_KEY = os.environ.get("FRED_API_KEY")


def clean_dict_items(dictionary):
    """ TODO
    """

    def is_float(string):
        """ Function to check whether a number is a float or not
        """
        try:
            # True if string is a number contains a dot
            return float(string) and "." in string
        except ValueError:  # String is not a number
            return False

    for key, value in dictionary.items():

        if value[-1] == "T":
            new_value = value[:-1]
            dictionary[key] = float(new_value) * 1000000000000

        if value[-1] == "M":
            new_value = value[:-1]
            dictionary[key] = float(new_value) * 1000000

        if value[-1] == "B":
            new_value = value[:-1]
            dictionary[key] = float(new_value) * 1000000000

        if "%" in value and "(" not in value:  # need to exclude fields with ()
            # % Remove the % sign
            new_value = value.replace("%", "")
            dictionary[key] = round(float(new_value) / 100, 3)

        if value.isdigit() or is_float(value):
            dictionary[key] = float(value)

        else:  # String has doesn't need to be converted at the moment
            pass

    return dictionary


def write_json_data(fin_data, file_path):
    """ Function to write results to JSON so we can pass this information to the dashboard
    """
    clean_data = {}

    def is_jsonable(x):
        """ Helper function to determine if an object is serializable to JSON
        """
        try:
            json.dumps(x)
            return True
        except:
            return False

    for key, value in fin_data.items():
        if is_jsonable(value):
            clean_data[key] = value
        else:
            json_value = value.to_json(orient="index")
            clean_data[key] = json_value

    with open(file_path, "w+", encoding="utf-8") as file:
        json.dump(clean_data, file)

    file.close()


def run(func_args):
    """ TODO
    """
    ticker = func_args.ticker
    data_volume = args.years
    FMP_API_KEY = os.environ.get("FMP_API_KEY")

    # Dict to store all data
    consolidated_data = {}

    ###############################################################################################
    # Get data
    yfin_data = yfin_scrp.retrieve_stock_data(ticker)
    tmx_data = tmx_scrp.retrieve_stock_data(ticker)

    # Clean up some of the data elements contained in the dictionary
    yfin_data["Company Financial Stats"] = clean_dict_items(yfin_data["Company Financial Stats"])

    company_sector = tmx_data["Company Profile"].get("Sector")
    sector_performance = ghd.get_sector_performance(company_sector)

    income_st = fin.get_jsonparsed_data(ticker, "income-statement", FMP_API_KEY)
    balance_sh = fin.get_jsonparsed_data(ticker, "balance-sheet-statement", FMP_API_KEY)
    cash_flow_st = fin.get_jsonparsed_data(ticker, "cash-flow-statement", FMP_API_KEY)

    ###############################################################################################
    # Organize data

    consolidated_data["Company_Profile"] = yfin_data["Company Profile"]
    consolidated_data["Company_Financial_Stats"] = yfin_data["Company Financial Stats"]
    consolidated_data["Company_Estimates"] = yfin_data["Company Estimates"]
    consolidated_data["ESG_Scores"] = yfin_data["ESG"]
    consolidated_data["Analyst_Recommendations"] = yfin_data["Recommendations"]
    consolidated_data["Sector_Performance"] = sector_performance

    # Getting some stats from TMX money as they are more precise
    shares_out = tmx_data["Quote Data"]["Shares Out."]
    market_cap = tmx_data["Quote Data"]["Market Cap1"]

    consolidated_data["Company_Financial_Stats"]["Shares Outstanding"] = float(shares_out)
    consolidated_data["Company_Financial_Stats"]["Market Capitalization"] = float(market_cap)

    fy_end = tmx_data["Company Profile"]["Fiscal Year End"]
    company_cik = tmx_data["Company Profile"]["CIK"]

    consolidated_data["Company_Profile"]["Fiscal Year"] = fy_end
    consolidated_data["Company_Profile"]["CIK"] = company_cik

    consolidated_data["Income_Statement"] = income_st
    consolidated_data["Balance_Sheet"] = balance_sh
    consolidated_data["Cash_Flow_Statement"] = cash_flow_st

    # create data directory for storage
    if not os.path.exists("data"):
        os.makedirs("data")

    write_json_data(consolidated_data, f"data/{ticker}.json")

    return consolidated_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="python3 main.py",
        description="Run the financial modelling tool on a specified company",
    )

    parser.add_argument("ticker", help="Stock ticker name of the company to retrieve data for")

    parser.add_argument("years", help="Number of years of company data to retrieve", default=4)
    # args = parser.parse_args()
    args = parser.parse_args(["AAPL", "5"])
    print(args)

    data = run(args)
    run_dashboard(args.ticker)
    # print(os.path.basename(__file__))
    # subprocess.run(["streamlit", "run", "dashboard.py"])
