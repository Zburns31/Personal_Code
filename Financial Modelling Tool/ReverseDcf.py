""" This module is for constructing the Reverse Discounted Cash Flow Analysis template. The goal is for this template to be used
    for any given company

    At a high level, we use the current stock price to work backwards and determine what level of FCF a company needs
    to generate in order to justify its current valuation
"""
from dataclasses import dataclass
from typing import List, Dict, Any
from statistics import mean
import pandas as pd
import datetime as dt
import math
import fredapi as Fred

pd.set_option('float_format', '{:f}'.format)


def ReverseDCF(object):

    def __init__(self, stock_price, shares_out, market_cap):
        self.stock_price = stock_price
        self.shares_out = shares_out

    @property
    def equity_value(stock_price, shares_out):
        return float(stock_price * shares_out)

    @property
    def get_risk_free_rate(api_key, t_bill_yr=10):
        fred = Fred(api_key=api_key)

        if t_bill_yr == 10:
            return fred.get_series('DGS10')

        elif t_bill_yr == 5:
            return fred.get_series('DGS5')

        else:
            print("Invalid Selection. Using 10 year treasury bill rate")
            return fred.get_series('DGS10')

    def main(stock_price, shares_out):

        return


if __name__ == '__main__':
    None
