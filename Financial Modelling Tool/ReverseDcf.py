""" This module is for constructing the Reverse Discounted Cash Flow Analysis template. The goal is for this template to be used
    for any given company

    At a high level, we use the current stock price to work backwards and determine what level of FCF a company needs
    to generate in order to justify its current valuation
"""
from typing import List, Dict, Any
from statistics import mean
import pandas as pd
import datetime as dt
import math
import fredapi as Fred

pd.set_option('float_format', '{:f}'.format)


class ReverseDCF(object):
    """ TODO
    """

    def __init__(self, dictionary):

        self.profile = dictionary['Company_Profile']
        self.financial_stats = dictionary['Company_Financial_Stats']
        self.estimates = dictionary['Company_Estimates']
        self.esg = dictionary['ESG_Scores']
        self.recommendations = dictionary['Analyst_Recommendations']
        self.sector_perf = dictionary['Sector_Performance']
        self.inc_st = dictionary['Income_Statement']
        self.balance_sh = dictionary['Balance_Sheet']
        self.cash_flow_st = dictionary['Cash_Flow_Statement']

    @property
    def equity_value(stock_price, shares_out, market_cap):
        equity_value = float(stock_price * shares_out)
        print(
            f'Calculated Equity Value == {equity_value} Vs. Retrieved Market Capitalization == {market_cap}')
        self.equity_value = equity_value

    @property
    def get_risk_free_rate(api_key, t_bill_yr=10, date=dt.datetime.today()):
        fred = Fred(api_key=api_key)
        # Need to get Risk free frate from previous day to due to lag of data publishing
        previous_day = date - dt.timedelta(days=1)

        if t_bill_yr == 10:
            self.risk_free_rate = fred.get_series('DGS10').loc[previous_day]

        elif t_bill_yr == 5:
            self.risk_free_rate = fred.get_series('DGS5').loc[previous_day]

        else:
            print("Invalid Selection. Using 10 year treasury bill rate")
            self.risk_free_rate = fred.get_series('DGS10').loc[previous_day]

    def main(self, stock_price, shares_out):

        return


if __name__ == '__main__':
    None
