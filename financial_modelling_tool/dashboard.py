""" Dashboard for stock
"""

import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
import subprocess
import json


# DATE_COLUMN = "date/time"
# DATA_URL = "https://s3-us-west-2.amazonaws.com/" "streamlit-demo-data/uber-raw-data-sep14.csv.gz"


def read_json_data(data_folder, ticker):
    """ Read in JSON data and convert to appropriate types
    """
    data = json.load(open(data_folder + ticker + ".json"))

    df_keys = [
        "Analyst_Recommendations",
        "Sector_Performance",
        "Income_Statement",
        "Balance_Sheet",
        "Cash_Flow_Statement",
    ]

    for key in df_keys:
        df = pd.read_json(data[key]).T
        data[key] = df

    return data


def run_dashboard(ticker):
    """ Main function to create financial dashboard for the given company
    """
    fin_data = read_json_data("data/", ticker)
    company_name = fin_data["Company_Profile"].get("Company Name")
    st.title(f"Financial Overview of {company_name}")

    print(os.path.basename(sys.argv[0]))
    subprocess.Popen(["streamlit", "run", "dashboard.py"]).wait()


if __name__ == "__main__":

    run_dashboard("AAPL")

# @st.cache
# def load_data(nrows):
#     data = pd.read_csv(DATA_URL, nrows=nrows)
#     lowercase = lambda x: str(x).lower()
#     data.rename(lowercase, axis="columns", inplace=True)
#     data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
#     return data


# data_load_state = st.text("Loading data...")
# data = load_data(10000)
# data_load_state.text("Done! (using st.cache)")

# if st.checkbox("Show raw data"):
#     st.subheader("Raw data")
#     st.write(data)

# st.subheader("Number of pickups by hour")
# hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
# st.bar_chart(hist_values)

# # Some number in the range 0-23
# hour_to_filter = st.slider("hour", 0, 23, 17)
# filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

# st.subheader("Map of all pickups at %s:00" % hour_to_filter)
# st.map(filtered_data)
