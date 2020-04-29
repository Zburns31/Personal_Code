#!/usr/local/bin/python3
""" This module controls the the webscraping portion of the Financial Modelling (FM) Tool. It scrapes data from a couple
    of the sub pages for the given stock ticker on yahoo finance, including:
        - Summary Tab
        - Statistics
        - Profile
        - Financials
            - Income Statement
            - Balance Sheet
            - Cash Flow Statement
        - Analysis: TODO
        - Holders: TODO
        - Sustainability: TODO
    At a high level, we load in each page we would like to scrape as a Beautiful Soup object and search using the library to
    find the data we are looking for
"""

import requests
import bs4
import lxml
import re
import pandas as pd
import yfinance as yf  # using for data which is difficult to scrape
from requests.exceptions import HTTPError
from collections import defaultdict, OrderedDict
################################################################################################################


def load_html_page_to_bs(url, sub_page, headers, parser='html.parser'):
    """ Function to loads an html website into a beautiful soup object with help from the requests library
    Parameters:
        url: location of the html page to load into a bs object
        headers: headers to pass in GET request
        parser: type of parser to use when parsing html pages
        key_statistics: indicates whether to grab information from the stock quote key stats page
    """

    if sub_page:
        url += f'/{sub_page}'

    response = requests.get(url, headers=headers)

    try:
        response.raise_for_status()

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')

    except Exception as err:
        print(f'Other error occurred: {err}')

    else:
        if sub_page is None:
            sub_page = 'summary'

        print(f'Grabbing {sub_page.title()} data')

        response.encoding = 'utf-8'
        bs_object = bs4.BeautifulSoup(response.text, parser)

        return bs_object
################################################################################################################


def get_summary_stock_data(lhs_table, rhs_table):
    """ Function to retrieve the passed in metric names from the lhs and rhs of the table
    Parameters:
        lhs_table: should be the lhs of the summary stock table (of type bs4.element.tag)
        rhs_table: should be the lhs of the summary stock table (of type bs4.element.tag)
        metric_names" summary stock data to be retrieved/scraped
    It's split into lhs and rhs since the result of findall from looking for all tables (since the summary
    table is split into two seperate html tables)
    """
    stock_table_data = lhs_table + rhs_table

    # Retrieve each stock
    stock_metrics_lis = [(item.attrs['data-test'],
                          item.text) for item in stock_table_data]

    # Remove the -value from each metric name. Need a function since tuples are immutable
    # apply the function to the first element of each tuple in the list (metric_name)
    def clean_metric_name_func(x): return x.split("-")[0]

    # lower case and capitalize the metric name to stay consistent with other values
    clean_metrics_lis = [(clean_metric_name_func(item).lower().capitalize(), value)
                         for item, value in stock_metrics_lis]

    return dict(clean_metrics_lis)
################################################################################################################


def get_key_stock_stats(bs_object, row_tag='tr', cell_tag='td'):
    """ Function to retrieve key stock stats from the yahoo finance page
    """
    stock_stats_dict = {}
    # Return all matching row tags (should include all table elements from the page)
    rows = bs_object.find_all(row_tag)

    for row in rows:
        # Need to parse through each element in the row using the cell tag (td) to get the value which
        # is located in the .text attribute
        metric_name = row.find_all(cell_tag)[0].text
        metric_score = row.find_all(cell_tag)[1].text

        stock_stats_dict[metric_name] = metric_score

    return stock_stats_dict
################################################################################################################


def get_stock_analysis_tables(bs_object):
    """
    """
    data_dict = {}

    analysis_page_tables = bs_object.find_all(
        'table', {'class': 'W(100%) M(0) BdB Bdc($seperatorColor) Mb(25px)'})

    for table in analysis_page_tables:
        line_item_vals = []

        # Find each row in the given table
        rows = table.find_all('tr')
        # headers = rows[0]
        # header_vals = [item.text for item in headers]
        # Header Name is item 0, vals are 1--> end
        # data_dict[header_vals[0]] = header_vals[1:]

        # row_vals = rows[1:]
        line_item_vals = [[item.text for item in row] for row in rows]
        line_item_dict = {line_item[0]: line_item[1:]
                          for line_item in line_item_vals}

        table_name = line_item_vals[0][0]
        # Seperate the data elements by table using their header name
        data_dict[table_name] = line_item_dict

    return data_dict
################################################################################################################


def get_financial_statement_line_items(bs_object, tag='div'):
    """ Function to retrieve all line items for the given financial statement
        Parameters:
            bs_object: HTML webpage as a BS4 object
            tag: which tag we want to look in to find our data
    """
    # Look for all div elements where there is a title attribute present
    line_items = bs_object.find_all(tag, title=True)

    # Add all returned items to a list
    line_item_lis = []
    for item in line_items:
        line_item_lis.append(item.string)

    # Remove None values from the list and return
    clean_line_items = list(filter(None, line_item_lis))

    return clean_line_items
################################################################################################################


def parse_financial_statements(bs_object,
                               financial_statement,
                               fin_st_line_items,
                               periods=['Annual', 'ttm'],
                               tag='div'):
    """ Retrieve financial statment data from the financials tab in yahoo finance.
        Will scrape data from income statement, balance sheet and cash flow statement
        Parameters:
            - bs_object: beautiful soup object to operate over(created from passing in html page above)
            - financial_statement: which financial statement to choose
                - Income statement
                - Balance sheet
                - Cash flow statement
            - fin_st_line_items: List of line items to retrieve data for for each financial statement
            - periods: Keep header columns from table and keep ttm to see if present in the table
            -tag: Type of tag where data can be found from
    """
    all_elements = []
    line_items_to_keep = fin_st_line_items + periods

    # We know the the data we want to find is located under the div tag, so we need to search through and
    # find what we need
    for element in bs_object.find_all(tag):
        # Use the string method to find text attributes of each element
        # many of the elements (div tags) will be None
        # .string is a navigable string vs .text returns all text concatenated for all child elements which
        # makes parsing difficult in this format
        # https: // stackoverflow.com/questions/25327693/difference-between-string-and-text-beautifulsoup
        all_elements.append(element.string)

    # filter out None values from list
    remove_none_vals = list(filter(None, all_elements))

    def clean_items(financial_statement_data_lis, line_items=line_items_to_keep):
        clean_list = []

        for item in financial_statement_data_lis:
            if item in line_items:
                clean_list.append(item)

            elif item[0].isdigit():
                clean_list.append(item)

            elif item[0] == '-':  # indicates a blank cell which we want to keep
                clean_list.append(item)
            else:
                pass

        return clean_list

    statement_data = clean_items(remove_none_vals)

    # Without the TTM column, the table will have Name of line item: [last reported year, last -2,etc.]
    num_prior_year_cols = 5
    if 'ttm' in statement_data:
        num_prior_year_cols = 6

    # iterate over 5 items at a time and assign to a tuple so we can load into a DF
    fin_statement = list(zip(*[iter(statement_data)]*num_prior_year_cols))

    return fin_statement
################################################################################################################


def get_company_profile_data(bs_object,
                             outer_tag='p',
                             outer_tag_class={'class': 'D(ib) Va(t)'},
                             inner_tag='span'):
    """
    """
    company_profile_elements = bs_object.find_all(outer_tag, outer_tag_class)

    # Need to find all span class instances within the result set. This is where the data
    # needed is actually stored
    company_profile_elements = company_profile_elements[0].find_all(inner_tag)

    company_profile_data = [item.text for item in company_profile_elements]

    # Cant use sets because they are unordered
    # Can use regular dictionary as of Python 3.7 since it guarantees ordering
    # https://stackoverflow.com/questions/7961363/removing-duplicates-in-lists
    # Basically maps all items in the list to dict keys and then back to list
    # This works because keys cannot be the same and will remove duplicates
    company_profile_data = list(OrderedDict.fromkeys(company_profile_data))
    # Take every other element and assign as either the key or value
    company_profile_dict = dict(zip(company_profile_data[::2],
                                    company_profile_data[1::2])
                                )

    return company_profile_dict
################################################################################################################


def dict_to_dataframe(data_dict):
    """ Function to transform dictionary of data into a DF. Used after parsing the financial statements
    """

    row_to_start = 0
    columns = []

    if all(isinstance(item, str) for item in data_dict[0]):
        row_to_start = 1
        columns = list(data_dict[0])

    df = pd.DataFrame(data_dict[row_to_start:], columns=columns)

    return df
################################################################################################################


def retrieve_stock_data(ticker, drop_ttm=True):
    """ Main function to scrape required data for the given stock ticker
        We use the BS4 and requests library to load HTML pages into a BS object. We can then use this to
        easily find the data we are looking for
        Ticker:
            ticker: stock ticker to scrape data for
    """
    all_company_data = {}

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"
    }
    # Type check to make sure ticker passed in is of type string
    if not isinstance(ticker, str):
        ticker = str(ticker)

    ticker = ticker.strip().upper()
    stock_data_loc = f'https://ca.finance.yahoo.com/quote/{ticker}'
    parser = "html.parser"

############################################################################################################
# Getting Stock statistics (Summary Tab, Key Statistics and Profile)
    # Load default stock quote page into a beautiful soup object
    stock_info = load_html_page_to_bs(url=stock_data_loc,
                                      sub_page=None,
                                      headers=headers,
                                      parser=parser)

    # Need to get the company name so that we can use it to find the company 10ks
    company_name = stock_info.find_all(
        'h1', {'class': 'D(ib) Fz(18px)'})[0].text

    # Remove (Ticker) from string
    clean_company_name = re.sub(r'\([^)]*\)', '', company_name).strip()

    company_profile_element = load_html_page_to_bs(url=stock_data_loc,
                                                   sub_page='profile',
                                                   headers=headers,
                                                   parser=parser)

    company_profile_dict = get_company_profile_data(company_profile_element)
    company_profile_dict['Company Name'] = clean_company_name

    all_company_data['Company Profile'] = {'Company Name': clean_company_name,
                                           **company_profile_dict
                                           }

    # Get the current price of the stock
    current_price = stock_info.find_all(
        "span", {'class': 'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'})[0].text

    # TODO: May be able to simplify this
    # Find the summary tables in the page so we can grab the data from it
    lhs_stock_table, rhs_stock_table = stock_info.find_all(
        "table", {"class": "W(100%)"})

    # Need to go down a level (below tbody attribute) below the table class to find individual cells
    # and the required data we are lookng for
    # TODO: shorten up this code with find_all statement
    # Can probably move this into a function
    lhs_stock_table_data = lhs_stock_table.find_all(
        "td", {'class': 'Ta(end) Fw(600) Lh(14px)'})

    rhs_stock_table_data = rhs_stock_table.find_all(
        "td", {'class': 'Ta(end) Fw(600) Lh(14px)'})

    summary_stock_data = get_summary_stock_data(
        lhs_stock_table_data, rhs_stock_table_data)

    # Add in the company profile info into the summary data
    # summary_stock_data.update(company_profile_dict)

    # Now, we are going to scrape the key statistics page from yahoo finance
    # rename key stats argument to something like sub_page as we can reuse it
    key_stats_stock_element = load_html_page_to_bs(url=stock_data_loc,
                                                   sub_page='key-statistics',
                                                   headers=headers,
                                                   parser=parser)

    key_stock_stats = get_key_stock_stats(key_stats_stock_element)

    company_stats = {'Current Price': current_price,
                     **summary_stock_data,
                     **key_stock_stats}

    # Compile into dict to organize all data
    all_company_data['Company Financial Stats'] = company_stats

################################################################################################################
    analysis_elements = load_html_page_to_bs(stock_data_loc,
                                             sub_page='analysis',
                                             headers=headers,
                                             parser=parser)

    stock_analysis_data = get_stock_analysis_tables(analysis_elements)
    # Compile into single dict for simplicity
    all_company_data['Company Estimates'] = stock_analysis_data
################################################################################################################
    # Using yfinance module to get hard to scrape elements
    ticker_data = yf.Ticker(ticker)
    ticker_esg_score = ticker_data.sustainability.reset_index()
    ticker_esg_score.columns = ['esg_metric', 'value']
    esg_data = dict(zip(ticker_esg_score.esg_metric, ticker_esg_score.value))

    # Get analyst recommendations for the stock
    ticker_recommendations = ticker_data.recommendations

    all_company_data['ESG'] = esg_data
    all_company_data['Recommendations'] = ticker_recommendations
################################################################################################################
    # Financial Statements Web Scraping

    # Income Statement
    income_statement_bs_obj = load_html_page_to_bs(url=stock_data_loc,
                                                   sub_page='financials',
                                                   headers=headers,
                                                   parser=parser)

    income_st_line_items = get_financial_statement_line_items(
        income_statement_bs_obj)

    income_st_data = parse_financial_statements(bs_object=income_statement_bs_obj,
                                                financial_statement='Income Statement',
                                                fin_st_line_items=income_st_line_items)

    # Transform dictionary of data to DF
    income_st_df = dict_to_dataframe(income_st_data)
    income_st_df = income_st_df.set_index('Annual')

    if drop_ttm:
        income_st_df = income_st_df.drop('ttm', axis=1)

    all_company_data['Income Statement'] = income_st_df
############################################################################################################
    # Balance Sheet
    balance_sheet_bs_obj = load_html_page_to_bs(url=stock_data_loc,
                                                sub_page='balance-sheet',
                                                headers=headers,
                                                parser=parser)

    balance_sheet_line_items = get_financial_statement_line_items(
        balance_sheet_bs_obj)

    balance_sheet_data = parse_financial_statements(bs_object=balance_sheet_bs_obj,
                                                    financial_statement='Balance Sheet',
                                                    fin_st_line_items=balance_sheet_line_items)

    # Transform dictionary of data to DF
    bal_sh_df = dict_to_dataframe(balance_sheet_data)
    bal_sh_df = bal_sh_df.set_index('Annual')

    all_company_data['Balance Sheet'] = bal_sh_df
############################################################################################################
    # Cash Flow Statement
    cash_flow_bs_obj = load_html_page_to_bs(url=stock_data_loc,
                                            sub_page='cash-flow',
                                            headers=headers,

                                            parser=parser)

    cash_flow_st_line_items = get_financial_statement_line_items(
        cash_flow_bs_obj)

    cash_flow_data = parse_financial_statements(bs_object=cash_flow_bs_obj,
                                                financial_statement='Cash Flow Statement',
                                                fin_st_line_items=cash_flow_st_line_items)

    # Transform dictionary of data to DF
    cash_flow_df = dict_to_dataframe(cash_flow_data)
    cash_flow_df = cash_flow_df.set_index('Annual')

    if drop_ttm:
        cash_flow_df = cash_flow_df.drop('ttm', axis=1)

    all_company_data['Cash Flow Statement'] = cash_flow_df
    ############################################################################################################

    return all_company_data


if __name__ == '__main__':

    data = retrieve_stock_data('AAPL')
