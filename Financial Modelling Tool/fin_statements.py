#!/usr/local/bin/python3

# edgar tool is for scraping SEC website
from edgar import Edgar, Company
import sys


# if __name__ == '__main__':

def get_company_sec_listing(company_name):
    """ Function to get SEC data for a given company

        Parameters:
            Company: The name of the company for which we want to get financial data for
    """
    company_name = company_name.upper()
    edgar = Edgar()
    possible_companies = edgar.find_company_name(company_name)

    if len(possible_companies) == 1:
        company = possible_companies[0]

    elif len(possible_companies) == 0:
        print("No companies found by the specified name")
        print("")
        print("Stopping program")
        sys.exit()

    else:  # if there are multiple companies returned
        # TODO: This assumes a match will be found
        companies = [
            item for item in possible_companies if company_name in item]
        # TODO: what if it returns more than 1 result
        if len(companies) == 1:
            company = companies[0]

        else:
            print("Multiple company names returned. Please select a choice: ")
            print("")

            for idx, company in enumerate(companies):
                print(f"Option {idx}: Company Name: {company}")
            option = int(input("Please enter an option: "))
            company = companies[option]

    company_cik = edgar.get_cik_by_company_name(company)

    return Company(company, company_cik)


company = get_company_sec_listing('Apple Inc.')
