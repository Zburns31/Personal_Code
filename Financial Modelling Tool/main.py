#!/usr/local/bin/python3
"""
This is the main module for the financial modelling tool.It serves as a script to execute any
necessary functions in order to parse or transform the data to give us the results we need
"""
# Custom module imports
import get_historical_data as ghd
import yfinance_webscraper as yfin_scrp  # import as yfin
import tmx_webscraper as tmx_scrp
import fin_statements as fin
from dcf import DcfModel


# Standard imports
import sys
import os
import argparse


def run(args):
    """
    """
    ticker = args.ticker
    data_volume = args.years

    # Dict to store all data
    consolidated_data = {}

    ###############################################################################################
    # Get data
    yfin_data = yfin_scrp.retrieve_stock_data(ticker)
    tmx_data = tmx_scrp.retrieve_stock_data(ticker)

    company_sector = tmx_data['Company Profile'].get('Sector')
    sector_performance = ghd.get_sector_performance(company_sector)

    income_st = fin.get_jsonparsed_data(ticker, 'income-statement')
    balance_sh = fin.get_jsonparsed_data(ticker, 'balance-sheet-statement')
    cash_flow_st = fin.get_jsonparsed_data(ticker, 'cash-flow-statement')

    ###############################################################################################
    # Organize data

    consolidated_data['Company Profile'] = yfin_data['Company Profile']
    consolidated_data['Company Financial Stats'] = yfin_data['Company Financial Stats']
    consolidated_data['Company Estimates'] = yfin_data['Company Estimates']
    consolidated_data['ESG Scores'] = yfin_data['ESG']
    consolidated_data['Analyst Recommendations'] = yfin_data['Recommendations']
    consolidated_data['Sector Performance'] = sector_performance

    # Getting some stats from TMX money as they are more precise
    shares_out = tmx_data['Quote Data']['Shares Out.']
    market_cap = tmx_data['Quote Data']['Market Cap1']

    consolidated_data['Company Financial Stats']['Shares Outstanding'] = shares_out
    consolidated_data['Company Financial Stats']['Market Capitalization'] = market_cap

    fy_end = tmx_data['Company Profile']['Fiscal Year End']
    company_cik = tmx_data['Company Profile']['CIK']

    consolidated_data['Company Profile']['Fiscal Year'] = fy_end
    consolidated_data['Company Profile']['CIK'] = company_cik

    consolidated_data['Income Statement'] = income_st
    consolidated_data['Balance Sheet'] = balance_sh
    consolidated_data['Cash Flow Statement'] = cash_flow_st

    return consolidated_data


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


# stock_price = data['Company Financial Stats']['Current Price']
# shares_out = data['Company Financial Stats']['Current Price']
# dcf = DcfModel(income_st=data['Income Statement'],
#                balance_sh=data['Balance Sheet'],
#                cash_flow_st=data['Cash Flow Statement'],
#                estimates=data['Company Estimates'])

# dcf_data = dcf.main(income_st=dcf.income_st, balance_sh=dcf.balance_sh,
#                     cash_flow_st=dcf.cash_flow_st, estimates=dcf.estimates,
#                     num_projection_years=dcf.num_projection_years)
