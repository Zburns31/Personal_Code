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

pd.set_option('float_format', '{:f}'.format)


def ReverseDCF(object):

    def __init__(self, stock_price, shares_out, market_cap):
        self.stock_price = stock_price
        self.shares_out = shares_out
        self.market_cap = market_cap

    @property
    def equity_value

    def main(stock_price, shares_out):

        return


if __name__ == '__main__':
