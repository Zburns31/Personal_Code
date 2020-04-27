""" This module is for constructing the Discounted Cash Flow Analysis template. The goal is for this template to be used
    for any given company

    Components of a DCF:
        - Top Line Revenue (Historical and Projections into the future)
            - TODO: breakdown into revenues by different product lines
        - COGS
        -

"""
from dataclasses import dataclass
from typing import List, Dict, Any
from statistics import mean
import pandas as pd
import datetime as dt
import math

pd.set_option('float_format', '{:f}'.format)


class DcfModel(object):
    """ Class for holding DCF and company financial data
    """

    def __init__(self, income_st, balance_sh, cash_flow_st, estimates):

        self.income_st = income_st
        self.balance_sh = balance_sh
        self.cash_flow_st = cash_flow_st
        self.estimates = estimates
        self.num_projection_years = 5
    # years_of_history: int = 3

    #############################################################################################################
    def convert_strings_to_ints(self, df):
        """ Helper function
        """
        for col in df.columns:
            # Need to remove commas in the strings before we cast to int
            df[col] = df[col].apply(lambda x: ''.join(x.split(',')))
            df[col] = df[col].astype('float')

        return df
    #############################################################################################################

    def get_time_bounds(self, df, years_to_project):
        """ Function to determine upper and lower bounds ofr historical and projections of financial data
        """

        historical_periods = [
            period for period in df.columns if 'ttm' not in period.lower()]

        # Get the most recent FY date so we can incrementally add years to it
        last_fy_period = max([dt.datetime.strptime(item, '%Y-%m-%d').date()
                              for item in historical_periods])

        projection_periods = [
            last_fy_period + pd.DateOffset(years=year) for year in range(1, years_to_project)]

        # Convert timestamps to dates()
        projection_periods = [str(x.date()) for x in projection_periods]

        return historical_periods + projection_periods
#############################################################################################################

    def calculate_rev_growth_rates(self, projections, n_years):
        """ Function to calculate growth rates for revenue
        """
        # Get Nested dict values for company estimates (eps, growth, etc)
        growth_projections = projections['Growth Estimates']

        # AAPL figures are the first index of each list
        current_year_growth = growth_projections.get('Current Year')[0]
        current_year_growth = float(current_year_growth.strip('%'))

        # need to start at current year + 1
        next_year_projection = growth_projections.get(
            'Next 5 Years (per annum)')[0]

        next_year_projection = float(next_year_projection.strip('%'))

        # Use next year projection and decrease by 1% for growth per year thereafter
        future_projections = [(next_year_projection - projection)
                              for projection in range(2, n_years+1)]

        projections = [next_year_projection] + future_projections

        # Need to divide figures by 100 so we can get percentages
        projections = [round(rate/100, 3) for rate in projections]

        return projections
#############################################################################################################

    def calculate_growth_rates(self, line_item):
        deltas = []
        for idx in range(0, len(line_item)-1):
            yoy_growth_perc = (
                line_item[idx+1] - line_item[idx])/line_item[idx]
            deltas.append(round(yoy_growth_perc,3))

        return deltas
#############################################################################################################

    # expected_growth_proj
    def calculate_revenues(self, df, num_projection_years, estimates, rev_row='Total Revenue'):
        """ Function to retreive historical revenues and to project future revenues

            TODO: Expand the ability to forecast revenues by breaking down by product
                  line, segment, etc

            Parameters:
                df: Income statement of the given company where we can get historical
                        revenue figures
        """
        revenues = list(df.loc[rev_row].values)
        hist_growth = self.calculate_growth_rates(revenues)

        future_growth_rates = self.calculate_rev_growth_rates(
            estimates, num_projection_years)

        for growth_rate in future_growth_rates:
            # Get the last calcualted year of revenues so we can use it to calculate FY +1 revenues
            last_fy_rev = revenues[-1]
            next_yr_rev = last_fy_rev * (1 + growth_rate)
            revenues.append(next_yr_rev)

        revenues = [round(rev) for rev in revenues]
        growth_rates = hist_growth + future_growth_rates

        self.revenues = {'Total Revenues': revenues}
        self.growth_rates = {'YoY Percentage Growth': growth_rates}

#############################################################################################################
    def main(self, income_st, balance_sh, cash_flow_st, estimates, num_projection_years):

        self.income_st = self.convert_strings_to_ints(income_st)
        # Reverse the order of the columns so we go from first year of available data to projections on the right
        self.income_st = income_st.iloc[:, ::-1]

        time_bounds = self.get_time_bounds(
            self.income_st, self.num_projection_years)

        self.calculate_revenues(
            self.income_st, num_projection_years, estimates)

        return self


if __name__ == '__main__':

    DCF = DcfModel(income_st=inc_st.copy(deep=True), balance_sh=None,
                   cash_flow_st=None, estimates=estimates)

    dcf = DCF.main(DCF.income_st, DCF.balance_sh,
                   DCF.cash_flow_st, DCF.estimates, DCF.num_projection_years)
