#!/usr/local/bin/python3
""" This module controls the the webscraping portion of the Financial Modelling (FM) Tool. It scrapes data from a couple
    of the sub pages for the given stock ticker on TMX Money, including:
        - Quote data
        - Profile
        - Financials
            - Income Statement

    At a high level, we load in each page we would like to scrape as a Beautiful Soup object and search using the library to
    find the data we are looking for
"""

import requests
import bs4
import lxml
import re
import pandas as pd
import yfinance as yf  # using for data which is difficult to scrape
import itertools
import time
from requests.exceptions import HTTPError
from collections import defaultdict, OrderedDict

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
################################################################################################################


def load_html_page_to_bs(page, ticker, exchange='US', parser='html.parser', headless=True):
    """ Function to loads an html website into a beautiful soup object with help from the requests library

    Parameters:
        url: location of the html page to load into a bs object
        headers: headers to pass in GET request
        parser: type of parser to use when parsing html pages
        key_statistics: indicates whether to grab information from the stock quote key stats page
    """

    tmx_page = f"https://web.tmxmoney.com/{page}.php?qm_symbol={ticker}:{exchange}"

    # Add the headless command so we dont open the browser during runtime
    options = webdriver.ChromeOptions()
    # Turn off proxy detection for faster execution
    options.add_argument('--no-proxy-server')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")

    # Headless option can be slow
    if headless:
        options.add_argument("headless")

    # driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options = options)
    driver.get(tmx_page)
    print("Waiting for page to load")
    time.sleep(5)

    print(f'Grabbing {page} data')
    bs_object = bs4.BeautifulSoup(driver.page_source, parser)

    return bs_object, driver
################################################################################################################


def parse_quote_table(ticker_quote_data):
    """ Function to parse the Detailed quote data from the TMX quote page
    """
    data = [item.text for item in ticker_quote_data]
    clean_data = [item.replace('\n', '')
                  .replace('\t', '')
                  .replace(',', '')
                  .replace('\xa0', '')
                  .replace('USD', '')
                  for item in data]

    split_data = [item.split(':') for item in clean_data]

    quote_data_dict = {data[0]: data[1] for data in split_data}
    # Remove uneeded dict item
    del quote_data_dict['Exchange']

    return quote_data_dict
################################################################################################################


def get_company_data(bs_object):
    """
    """
    company_data = {}
    company_fy_end = bs_object.find_all('div', {'class': 'col-md-6 mb-4'})[-1]
    # Remove empty strings
    company_fy_end = [item for item in company_fy_end if item]
    company_fy_end = [item.text for item in company_fy_end if item != '\n']

    # Find the first occurence of a row tag
    company_classification_table = bs_object.find_all(
        'div', {'class': 'col-md-4 mb-4'})

    classification_data = [item.text.split(
        "\n") for item in company_classification_table]

    merged_lis = list(itertools.chain(*classification_data))
    clean_data = [item.replace('\t', '')
                  for item in merged_lis if not '\t' or item]

    # Slice list so we can pack into dictionary with all data
    keys = clean_data[::2]
    vals = clean_data[1::2]

    classification_dict = dict(zip(keys, vals))

    company_data = {'Fiscal Year End': company_fy_end[-1],
                    **classification_dict}

    return company_data
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


def parse_financial_statement(bs_object, tbody_class, driver):
    """ Function to retrieve all line items for the given financial statement

        Parameters:
            bs_object: HTML webpage as a BS4 object
            tbody_class: Name of financial statement which is used to locate the table
                where the data is located for the specified financial statement
    """

    headers = bs_object.find_all(
        'th', {'class': 'qmod-textr qmod-report-data-heading qmod-capitalize'})
    clean_headers = [item.text for item in headers]

    # Look for all div elements where there is a title attribute present
    table_body = bs_object.find_all('tbody', {'class': tbody_class})
    rows = table_body[0].find_all('tr')

    def parse_rows(table_rows):
        row_data = []
        for row in table_rows:
            row_elements = row.find_all('td')

        # Remove chart/graph cell information as its not needed
            cell_data = [
                item.text for item in row_elements if 'Created' not in item.text]

            clean_cell_data = [item.replace(
                ',', '') if item[0].isdigit() else item.title() for item in cell_data]

            row_data.append(clean_cell_data)

        return row_data

    clean_fin_st_data = parse_rows(rows)
    # Convert to dict for easier conversion to DF later on
    fin_st_dict = {item[0]: item[1:] for item in clean_fin_st_data}
    fin_st_dict['Headers'] = clean_headers

    return fin_st_dict
################################################################################################################


def dict_to_dataframe(data_dict):
    """ Function to transform dictionary of data into a DF. Used after parsing the financial statements
    """
    df = pd.DataFrame.from_dict(data_dict, orient='index')

    df = df.rename(index={'Headers': 'Period'})
    df.columns = df.loc['Period']

    return df.drop('Period')

################################################################################################################


def load_page_from_dropdown_menu(driver, company_name, page, parser='html.parser'):

    element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located(
        (By.XPATH, f"//h4[text()='Financials for {company_name}']")))

    driver.execute_script("window.scrollBy(0,600)")

    ActionChains(driver).move_to_element(WebDriverWait(driver, 20).until(EC.visibility_of_element_located(
        (By.XPATH, "//a[@class='qmod-dropdown_toggle qmod-type-toggle']/span[text()='Income Statement']")))).perform()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, f"//ul[@class='qmod-dropdown-menu']//li/a[text()='{page}']"))).click()

    time.sleep(5)
    page = bs4.BeautifulSoup(driver.page_source, parser)
    return page
################################################################################################################


def retrieve_stock_data(ticker, listing_country='US'):
    """ Main function to scrape required data for the given stock ticker

        We use the BS4 and requests library to load HTML pages into a BS object. We can then use this to
        easily find the data we are looking for

        Ticker:
            ticker: stock ticker to scrape data for
    """
    all_company_data = {}

    # Type check to make sure ticker passed in is of type string
    if not isinstance(ticker, str):
        ticker = str(ticker)

    ticker = ticker.strip().upper()
    parser = "html.parser"

############################################################################################################
# Getting Stock statistics (Summary Tab, Key Statistics and Profile)
    # Load default stock quote page into a beautiful soup object
    stock_info, driver = load_html_page_to_bs(page='quote',
                                              ticker=ticker,
                                              parser=parser)
    driver.close()
    # return stock_info
    # Need to get the company name so that we can use it to find the company 10ks
    company_name = stock_info.find_all('h4')[0].text

    # Get the current price of the stock
    current_price = stock_info.find_all("span", {'class': 'price'})[0]
    current_price = [float(item.string)
                     for item in current_price if item.string[0].isdigit()][0]

    all_company_data['Company Name'] = company_name
    all_company_data['Current Price'] = current_price

############################################################################################################
# Get quote page data
    detailed_quote = stock_info.find_all('div', {'class': 'dq-card'})
    quote_data = parse_quote_table(detailed_quote)

    all_company_data['Quote Data'] = quote_data
############################################################################################################
# Company data
    company_info, driver = load_html_page_to_bs(page='company',
                                                ticker=ticker,
                                                parser=parser)
    driver.close()

    company_profile_dict = get_company_data(company_info)

    all_company_data['Company Profile'] = company_profile_dict
################################################################################################################
    # Financial Statements Web Scraping

    # Income Statement
    inc_st, driver = load_html_page_to_bs(page='financials',
                                          ticker=ticker,
                                          parser=parser)

    inc_st_data = parse_financial_statement(
        inc_st, 'IncomeStatement', driver=driver)

    driver.close()
    # Transform dictionary of data to DF
    income_st_df = dict_to_dataframe(inc_st_data)

    all_company_data['Income Statement'] = income_st_df
############################################################################################################

    return all_company_data
    """ TODO: Scraping the balance sheet and cash flow statement
    """
    # Balance Sheet
    # bal_sh, driver = load_html_page_to_bs(page='financials',
    #                                       ticker=ticker,
    #                                       parser=parser)
    # return bal_sh, driver
    # bal_sheet_webpage = load_page_from_dropdown_menu(
    #     driver, company_name, 'Balance Sheet')


# balance_sheet_data = parse_financial_statement(
#     bal_sheet_webpage, 'BalanceSheet')

# return balance_sheet_data

# # Transform dictionary of data to DF
# bal_sh_df = dict_to_dataframe(balance_sheet_data)

# all_company_data['Balance Sheet'] = bal_sh_df
# return bal_sh_df
############################################################################################################
# Cash Flow Statement
# cash_flow_bs_obj = load_html_page_to_bs(url=stock_data_loc,
#                                         sub_page='cash-flow',
#                                         headers=headers,

#                                         parser=parser)

# cash_flow_st_line_items = get_financial_statement_line_items(
#     cash_flow_bs_obj)

# cash_flow_data = parse_financial_statements(bs_object=cash_flow_bs_obj,
#                                              financial_statement='Cash Flow Statement',
#                                              fin_st_line_items=cash_flow_st_line_items)

#  # Transform dictionary of data to DF
#  cash_flow_df = dict_to_dataframe(cash_flow_data)
#   cash_flow_df = cash_flow_df.set_index('Annual')

#    if drop_ttm:
#         cash_flow_df = cash_flow_df.drop('ttm', axis=1)

#     all_company_data['Cash Flow Statement'] = cash_flow_df
#     ############################################################################################################

#     return all_company_data


if __name__ == '__main__':

    data = retrieve_stock_data('AAPL')

# button = driver.find_element_by_css_selector(
#     '#pane-charting > div > div > div.col-md-9.col-lg-10 > div > div > div.qmod-tool-wrap > div > div.qmod-block-wrapper.qmod-financials-block > div.qmod-modifiers > div > div:nth-child(1) > div.qmod-mod-pad.qmod-pad-right > div > div > a')
# button.click()
# options = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
#     (By.CSS_SELECTOR, '#pane-charting > div > div > div.col-md-9.col-lg-10 > div > div > div.qmod-tool-wrap > div > div.qmod-block-wrapper.qmod-financials-block > div.qmod-modifiers > div > div:nth-child(1) > div.qmod-mod-pad.qmod-pad-right > div > div > ul')))
