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

pd.set_option('float_format', '{:f}'.format)


@dataclass
class DcfModel:
    """ Class for holding DCF and company financial data
    """
    income_st: Any
    balance_sh: Any
    cash_fl_st: Any
    estimates: Any
    num_projection_years: int = 10
    years_of_history: int = 3

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
        # AAPL figures are the first index of each list
        return projections
        current_year_growth = projections.get('Current Year')[0]
        current_year_growth = float(current_year_growth.strip('%'))
        print(current_year_growth)
        # need to start at current year + 1
        next_year_projection = projections.get('Next 5 Years (per annum)')[0]
        next_year_projection = round(float(next_year_projection.strip('%')), 1)
        print(next_year_projection)
        future_projections = [round(next_year_projection - projection, 1)
                              for projection in range(2, n_years+1)]

        projections = next_year_projection + future_projections
        return projections

    def calculate_growth_rates(self, line_item):
        deltas = []
        for idx in range(0, len(line_item)-1):
            yoy_growth_perc = (
                line_item[idx+1] - line_item[idx])/line_item[idx]
            deltas.append(yoy_growth_perc)

        return deltas
#############################################################################################################

    # expected_growth_proj
    def calculate_revenues(self, df, years_of_projections, estimates, rev_row='Total Revenue'):
        """ Function to retreive historical revenues and to project future revenues

            TODO: Expand the ability to forecast revenues by breaking down by product
                  line, segment, etc

            Parameters:
                df: Income statement of the given company where we can get historical
                        revenue figures
        """
        historical_revs = df.loc[rev_row].values

        growth_rates = self.calculate_rev_growth_rates(
            growth_projections, years_of_projections)
        return growth_rates

#############################################################################################################
    def main(self, income_st, balance_sh, cash_flow_st, estimates):

        self.income_st = dcf.convert_strings_to_ints(self.income_st)
        # Reverse the order of the columns so we go from first year of available data to projections on the right
        self.income_st = self.income_st.iloc[:, ::-1]

        time_bounds = self.get_time_bounds(
            self.income_st, self.num_projection_years)

        revs = self.calculate_revenues(
            income_st, self.num_projection_years, self.num_projection_years)

        return revs


if __name__ == '__main__':

    dcf = DcfModel(inc_st.drop('ttm', axis=1))
    data = dcf.main(dcf.income_st)
