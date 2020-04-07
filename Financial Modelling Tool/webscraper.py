#!/usr/local/bin/python3

import requests
import bs4
import lxml
import re
from requests.exceptions import HTTPError
from collections import defaultdict

def load_html_page_to_bs(url, sub_page, headers, parser = 'html.parser'):
    """ Function to loads an html website into a beautiful soup object with help from the requests library

    Parameters:
        url: location of the html page to load into a bs object
        headers: headers to pass in GET request
        parser: type of parser to use when parsing html pages
        key_statistics: indicates whether to grab information from the stock quote key stats page
    """

    if sub_page:
        url += f'/{sub_page}'
    
    response = requests.get(url, headers = headers)

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
    clean_metric_name_func = lambda x: x.split("-")[0]
    clean_metrics_lis = [(clean_metric_name_func(item), value) for item, value in stock_metrics_lis]

    return dict(clean_metrics_lis)
################################################################################################################

def get_data_table(bs_object, tag, tag_class):
    return bs_object.find_all(tag, tag_class)

################################################################################################################
def get_key_stock_stats(bs_object, row_tag = 'tr', cell_tag = 'td'):
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

def retrieve_stock_data(ticker):
    """ TODO: documentation
    """

    headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7",
        "Connection":"keep-alive",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"
    }
    # Type check to make sure ticker passed in is of type string
    if not isinstance(ticker, str):
        ticker = str(ticker)

    ticker = ticker.strip().upper()
    stock_data_loc = f'https://ca.finance.yahoo.com/quote/{ticker}'
    parser = "html.parser"

    stock_info = load_html_page_to_bs(url = stock_data_loc,
                                      sub_page = None,
                                      headers = headers, 
                                      parser = parser)
    
    # Get the current price of the stock
    current_price = stock_info.find_all("span", {'class':'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'})[0].text

    # TODO: create a function to find the table with given class
    lhs_stock_table, rhs_stock_table = get_data_table(stock_info, "table", {"class": "W(100%)"}) 

    # Need to go down a level (below tbody attribute) below the table class to find individual cells
    # and the required data we are lookng for 
    lhs_stock_table_data = lhs_stock_table.find_all("td", {'class': 'Ta(end) Fw(600) Lh(14px)'})
    rhs_stock_table_data = rhs_stock_table.find_all("td", {'class': 'Ta(end) Fw(600) Lh(14px)'})
    
    summary_stock_data = get_summary_stock_data(lhs_stock_table_data, rhs_stock_table_data)
    
    # Now, we are going to scrape the key statistics page from yahoo finance
    # rename key stats argument to something like sub_page as we can reuse it
    key_stats_stock_info = load_html_page_to_bs(url = stock_data_loc,
                                                sub_page = 'key-statistics',
                                                headers = headers,
                                                parser = parser
    )

    key_stock_stats = get_key_stock_stats(key_stats_stock_info)
    


    
    
    income_statement_bs_obj = load_html_page_to_bs(url = stock_data_loc, 
                                                   sub_page = 'financials', 
                                                   headers = headers, 
                                                   parser = parser
    )
    
    income_statement_data, table_headers = get_financial_statements_data(income_statement_bs_obj, 'income_statement')
    return income_statement_data, table_headers

def get_financial_statements_data(bs_object,
                                  financial_statement,
                                  row_tag = 'div', 
                                  row_class = {'class': 'D(tbr) fi-row Bgc($hoverBgColor):h'},
                                  header_tag = 'div', 
                                  header_class = {'class': 'D(tbr) C($primaryColor)'}):

    """ Retrieve financial statment data from the financials tab in yahoo finance. 
        Will scrape data from income statement, balance sheet and cash flow statement

        Parameters:
            url: path to financial statements
            bs_object: beautiful soup object to operate over (created from passing in html page above)
            financial_statement: which financial statement to choose
                - Income statement
                - Balance sheet
                - Cash flow statement
    """
    if financial_statement == 'income_statement':
        pass

    header = bs_object.find_all(header_tag, header_class)
    #Returns a list object, so we need to slice it to get our data
    header_data = header[0]
    headers = [header.text for header in header_data]
    # Get rid of the breakdown/first column header
    headers = headers[1:]
    
    # Here we set the recursive flag to be True so we can keep more than just the direct children 
    # (default is False)
    table_rows = bs_object.find_all(row_tag, row_class, recursive = True)

    financial_statement_dict = {}

    for row in table_rows:
        row_data = []
        row_data.extend([cell.text for cell in row])
        financial_statement_dict[row_data[0]] = row_data[1:]
    
    clean_financial_statement_data = {}
    for key, values in financial_statement_dict.items():
        values = ['N/A' if x == '-' else x for x in values]
        clean_financial_statement_data[key] = values

    return clean_financial_statement_data, headers
    



data, headers = retrieve_stock_data('AAPL')