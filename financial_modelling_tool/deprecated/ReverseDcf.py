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

        self.date = dt.date.today()
        self.terminal_growth_rate = 0.03

        self.profile = dictionary.get('Company_Profile', None)
        self.financial_stats = dictionary.get('Company_Financial_Stats', None)
        self.estimates = dictionary.get('Company_Estimates', None)
        self.esg = dictionary.get('ESG_Scores', None)
        self.recommendations = dictionary.get('Analyst_Recommendations', None)
        self.sector_perf = dictionary.get('Sector_Performance', None)
        self.inc_st = dictionary.get('Income_Statement', None)
        self.balance_sh = dictionary.get('Balance_Sheet', None)
        self.cash_flow_st = dictionary.get('Cash_Flow_Statement', None)





    def get_equity_value(self, financial_stats):
        """ Calcuating equity value of a company. Defined as either:
            - Market Capitalization
            - Shares outstanding * Current share price

            Parameters:
                - financial_stats: Dictionary of company statistics (Shares Out, current price, etc.)
                                   retrieved from the company quote, summary and statistics pages
        """

        shares_out = financial_stats.get('Shares Outstanding')
        stock_price = financial_stats.get('Current Price')
        market_cap = financial_stats.get('Market Capitalization')

        equity_value = float(stock_price * shares_out)

        print(
            f'Calculated Equity Value == {equity_value} Vs. Retrieved Market Capitalization == {market_cap}')

        return equity_value


    def get_enterprise_value(self, equity_value, balance_sh):
        """ Calcualte the Enterprise value of the company using line items from the balance sheet
            TODO: preferred stock, noncontrolling interests

            Parameters:
                equity_value: Market capitalization of the company
                balance_sh: Balance sheet data
        """

        last_year = self.date.year - 1
        years = balance_sh.columns
        rel_data = [item for item in years if pd.to_datetime(item).year == 2019]

        short_term_debt = balance_sh.loc['Short-term debt', rel_data].iloc[0]
        long_term_debt = balance_sh.loc['Long-term debt', rel_data].iloc[0]

        cash_and_equivs = (balance_sh.loc['Cash and cash equivalents', rel_data].iloc[0] +
                           balance_sh.loc['Short-term investments', rel_data].iloc[0])

        # TODO
        # preferred_stock =
        # noncontrolling_interest =

        return equity_value + short_term_debt + long_term_debt - cash_and_equivs


    def get_debt_to_equity_ratio(self, balance_sh, ratio=None):

        debt = balance_sh.loc['Total liabilities'][-1]
        equity = balance_sh.loc['Total shareholders equity'][-1]

        return debt/equity


    def get_wacc(self, debt_to_tv, equity_to_tv, cost_of_equity, cost_of_debt, tax_rate):
        """ Function to calculate the weighted average cost of capital
        """

        return









    # @property
    # def get_risk_free_rate(api_key, t_bill_yr=10, date=dt.datetime.today()):
    #     fred = Fred(api_key=api_key)
    #     # Need to get Risk free frate from previous day to due to lag of data publishing
    #     previous_day = date - dt.timedelta(days=1)

    #     if t_bill_yr == 10:
    #         self.risk_free_rate = fred.get_series('DGS10').loc[previous_day]

    #     elif t_bill_yr == 5:
    #         self.risk_free_rate = fred.get_series('DGS5').loc[previous_day]

    #     else:
    #         print("Invalid Selection. Using 10 year treasury bill rate")
    #         self.risk_free_rate = fred.get_series('DGS10').loc[previous_day]

    def main(self):
        """
        """
        date = self.date

        # Start calculating required DCF data
        equity_value = self.get_equity_value(self.financial_stats)
        enterprise_value = self.get_enterprise_value(equity_value, self.balance_sh)



    ###############################################################################################
    # Start Creating the Reverse DCF

        return


if __name__ == '__main__':
    None
