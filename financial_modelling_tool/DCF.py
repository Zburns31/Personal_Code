""" This module is for constructing the DCF analysis for the Financial Modelling tool
"""
import datetime as dt
import pandas as pd
import os

import wacc as wacc

FRED_API_KEY = os.environ.get("FRED_API_KEY")


class DCF(object):
    """ Class for constructing the DCF analysis
        Parameters:
            - company_data: A nested dictionary containing all relevant/scraped data
                            from other modules to feed into the model
    """

    def __init__(self, company_data, terminal_growth=0.02, forecast_horizon=10):
        for key in company_data:
            setattr(self, key, company_data[key])

        self.terminal_growth = terminal_growth
        self.forecast_horizon = forecast_horizon

    def linear_decline_growth_forecast(
        self, current_year_estimate, next_year_estimate, terminal_growth, n_projections
    ):

        """ Formula to calculate linear decline in revenue growth based on terminal growth value
            and number of projection periods. We use n_projections -1 since we have next years
            estimate provided by the web scraper portion
        """
        decline_fig = (next_year_estimate - terminal_growth) / (n_projections - 2)
        print(decline_fig)
        projections = [
            round((next_year_estimate - (decline_fig * n)), 3) for n in range(1, n_projections - 1)
        ]

        return [current_year_estimate, next_year_estimate] + projections

    def build_proforma_income_statement(
        self, inc_statement, estimates, projection_period=5, historical_periods=3
    ):
        """
        """
        assert inc_statement.columns[-1] == max(inc_statement)

        # Take the last N years from the Income statement to help with projections
        cols = inc_statement.columns[-historical_periods:]
        inc_st = inc_statement.loc[:, cols]

        def projections(inc_st, estimates):

            year = dt.date.today().year
            next_year = year + 1

            cy_idx = estimates["Revenue Estimate"]["Revenue Estimate"].index(
                f"Current Year ({year})"
            )
            ny_idx = estimates["Revenue Estimate"]["Revenue Estimate"].index(
                f"Next Year ({next_year})"
            )

            current_year_sales_growth = estimates["Revenue Estimate"]["Sales Growth (year/est)"][
                cy_idx
            ]
            next_year_sales_growth = estimates["Revenue Estimate"]["Sales Growth (year/est)"][
                ny_idx
            ]

            def string_perc_to_float(string_val):
                """ Function to remove % sign from strings and format the value as a float
                """
                return float(string_val.replace("%", "")) / 100

            curr_year_growth = string_perc_to_float(current_year_sales_growth)
            next_year_growth = string_perc_to_float(next_year_sales_growth)

            return curr_year_growth, next_year_growth

        return projections(inc_st, estimates)

    def build_wacc_table(self, rf_rate, beta, lfy_interest_expense, total_debt):
        """ Build WACC table for DCF
        """

    def run(self):
        """ Main function to build DCF analysis
        """
        rf_rate = wacc.get_risk_free_rate(api_key=FRED_API_KEY)
        beta = self.Company_Financial_Stats["Beta (5Y Monthly) "]
        cost_of_equity = wacc.calculate_cost_of_equity(rf_rate, beta)
        cost_of_debt = wacc.calculate_cost_of_debt(
            lfy_interest_expense, self.Balance_Sheet.loc["totalDebt"][-1]
        )

        self.wacc = self.build_wacc_table()


if __name__ == "__main__":

    dcf = DCF(data)

    cy, nxt = dcf.build_proforma_income_statement(dcf.Income_Statement, dcf.Company_Estimates)
    growth_ests = dcf.linear_decline_growth_forecast(
        cy, nxt, dcf.terminal_growth, dcf.forecast_horizon
    )
