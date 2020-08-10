""" Module for calculating the WACC / Required rate of return for a given company. In order to
    calculate the WACC we need the following items:

    - Risk free rate of return
    - Equity risk premium
    - Cost of Equity
        - Beta (from webscraping)
        - Market value of equity (preferred and common stock) (from webscraping)
    - Cost of Debt
        - Market value of debt (net debt from latest balance sheet)
    - Marginal tax rate
"""

# import pandas_datareader as pdr
# pdr.get_data_fred('GS10')
import os
import datetime as dt
from fredapi import Fred


FRED_API_KEY = os.environ.get("FRED_API_KEY")


def get_risk_free_rate(api_key, t_bill_yr=10):
    """ Get the latest risk free rate from the St Louis FED website using the fredapi
    """
    fred = Fred(api_key=api_key)
    # Need to get Risk free frate from previous day to due to lag of data publishing

    if t_bill_yr == 10:
        rate = fred.get_series("DGS10")[-1]

    elif t_bill_yr == 5:
        rate = fred.get_series("DGS5")[-1]

    else:
        print("Invalid Selection. Using 10 year treasury bill rate")
        rate = fred.get_series("DGS10")[-1]

    return rate / 100


def calculate_cost_of_equity(risk_free_rate, beta, expected_market_return=0.06):
    """ Function to calculate the cost of equity for a company
    """
    return round(risk_free_rate + beta * (expected_market_return - risk_free_rate), 3)


def calculate_cost_of_debt(lfy_interest_expense, book_value_debt):
    """Function to calculate the cost of debt
    """

    return round((lfy_interest_expense / book_value_debt), 3)


def calculate_wacc(mv_equity, mv_debt, cost_of_equity, cost_of_debt, two_year_avg_tax_rate):
    """ Function to calculate the weighted average cost of capital for a company
    """

    equity_weight = mv_equity / (mv_equity + mv_debt)
    debt_weight = mv_debt / (mv_debt + mv_equity)

    wacc = equity_weight * cost_of_equity + debt_weight * cost_of_debt
    return round(wacc, 3)


if __name__ == "__main__":

    rf_rate = get_risk_free_rate(api_key=FRED_API_KEY)
