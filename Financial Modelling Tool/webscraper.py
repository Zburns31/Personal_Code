#!/usr/local/bin/python3

import requests
import bs4
import lxml
import re
from requests.exceptions import HTTPError
from collections import defaultdict
from collections import OrderedDict

################################################################################################################
# List of data elements to keep for web scraping
balance_sheet_line_items = [
    "Cash And Cash Equivalents", "Other Short Term Investments", "Total Cash", "Net Receivables",
    "Inventory", "Other Current Assets", "Total Current Assets", "Gross property, plant and equipment",
    "Net property, plant and equipment", "Accumulated Depreciation", "Net property, plant and equipment",
    "Equity and other investments", "Goodwill", "Intangible Assets", "Other long-term assets",
    "Total non-current assets", "Total Assets", "Current Debt", "Accounts Payable", "Accrued liabilities",
    "Deferred revenues", "Other Current Liabilities", "Total Current Liabilities", "Long Term Debt",
    "Deferred taxes liabilities", "Deferred revenues", "Other long-term liabilities",
    "Total non-current liabilities", "Total Liabilities", "Common Stock", "Retained Earnings",
    "Accumulated other comprehensive income", "Total stockholders' equity",
    "Total liabilities and stockholders' equity",

]

income_statement_line_items = [
    "Total Revenue", "Cost of Revenue", "Gross Profit", "Research Development", "Selling General and Administrative",
    "Total Operating Expenses", "Operating Income or Loss", "Interest Expense", "Total Other Income/Expenses Net",
    "Income Before Tax", "Income Tax Expense", "Income from Continuing Operations", "Net Income",
    "Net Income available to common shareholders", "Basic EPS", "Diluted EPS", "Basic Average Shares",
    "Diluted Average Shares", "EBITDA"
]

cash_flow_line_items = [
    "Net Income", "Depreciation & amortization", "Deferred income taxes", "Stock based compensation",
    "Change in working capital", "Accounts receivable", "Inventory", "Accounts Payable",
    "Other working capital", "Other non-cash items", "Net cash provided by operating activites",
    "Investments in property, plant and equipment", "Acquisitions, net", "Purchases of investments",
    "Sales/Maturities of investments", "Other investing activites", "Net cash used for investing activites",
    "Debt repayment", "Common stock issued", "Common stock repurchased", "Dividends Paid",
    "Other financing activites", "Net cash used privided by (used for) financing activities",
    "Net change in cash", "Cash at beginning of period", "Cash at end of period", "Operating Cash Flow",
    "Capital Expenditure", "Free Cash Flow"
]


financial_statements_dict = {
    'Balance Sheet': balance_sheet_line_items,
    'Income Statement': income_statement_line_items,
    'Cash Flow Statement': cash_flow_line_items
}
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
        print('Grabbing stock data')

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
    clean_metrics_lis = [(clean_metric_name_func(item), value)
                         for item, value in stock_metrics_lis]

    return dict(clean_metrics_lis)
################################################################################################################


def get_element(bs_object, tag, tag_class):
    return bs_object.find_all(tag, tag_class)
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


def parse_financial_statements(bs_object,
                               financial_statement,
                               fin_statement_dict=financial_statements_dict,
                               periods=['Annual', 'ttm'],
                               tag='div'):
    """ Retrieve financial statment data from the financials tab in yahoo finance.
        Will scrape data from income statement, balance sheet and cash flow statement

    Parameters:
            bs_object: beautiful soup object to operate over(created from passing in html page above)
            financial_statement: which financial statement to choose
                - Income statement
                - Balance sheet
                - Cash flow statement
            - fin_statement_dict: Dictionary of line items to retrieve data for for each financial statement
            - periods: Keep header columns from table and keep ttm to see if present in the table
            -tag: Type of tag where data can be found from
    """
    all_elements = []
    line_items_to_keep = fin_statement_dict[financial_statement] + periods

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


def retrieve_stock_data(ticker, financial_statements_dict_map=financial_statements_dict):
    """ TODO: documentation
    """
    financial_statements_data_dict = {}

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

    # Load default stock quote page into a beautiful soup object
    stock_info = load_html_page_to_bs(url=stock_data_loc,
                                      sub_page=None,
                                      headers=headers,
                                      parser=parser)

    company_profile_element = load_html_page_to_bs(url=stock_data_loc,
                                                   sub_page='profile',
                                                   headers=headers,
                                                   parser=parser)

    company_profile_data = get_element(company_profile_element,
                                       tag='p',
                                       tag_class={'class': 'D(ib) Va(t)'})
    # Need to find all span class instances within the result set. This is where the data
    # needed is actually stored
    company_profile_data = [
        item.text for item in company_profile_data[0].find_all('span')]

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

    # Get the current price of the stock
    current_price = stock_info.find_all(
        "span", {'class': 'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'})[0].text

    # TODO: create a function to find the table with given class
    lhs_stock_table, rhs_stock_table = get_element(
        stock_info, "table", {"class": "W(100%)"})

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
    summary_stock_data = summary_stock_data.update(company_profile_dict)

    # Now, we are going to scrape the key statistics page from yahoo finance
    # rename key stats argument to something like sub_page as we can reuse it
    key_stats_stock_info = load_html_page_to_bs(url=stock_data_loc,
                                                sub_page='key-statistics',
                                                headers=headers,
                                                parser=parser)

    key_stock_stats = get_key_stock_stats(key_stats_stock_info)

    ############################################################################################################
    # Financial Statements Web Scraping
    income_statement_bs_obj = load_html_page_to_bs(url=stock_data_loc,
                                                   sub_page='financials',
                                                   headers=headers,
                                                   parser=parser)
    income_st_data = parse_financial_statements(income_statement_bs_obj,
                                                'Income Statement',
                                                fin_statement_dict=financial_statements_dict_map)

    balance_sheet_bs_obj = load_html_page_to_bs(url=stock_data_loc,
                                                sub_page='balance-sheet',
                                                headers=headers,
                                                parser=parser)

    balance_sheet_data = parse_financial_statements(balance_sheet_bs_obj,
                                                    'Balance Sheet',
                                                    fin_statement_dict=financial_statements_dict_map)

    cash_flow_bs_obj = load_html_page_to_bs(url=stock_data_loc,
                                            sub_page='cash-flow',
                                            headers=headers,
                                            parser=parser)

    cash_flow_data = parse_financial_statements(cash_flow_bs_obj,
                                                'Cash Flow Statement',
                                                fin_statement_dict=financial_statements_dict_map)

    ############################################################################################################

    return cash_flow_data


data = retrieve_stock_data('AAPL')
