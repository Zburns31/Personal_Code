#!/usr/local/bin/python3

import pandas as pd
import quandl
import datetime

# Needed for get requests of data
api_key = "9jdxXhYHdzavbniMcpn6"

start = datetime.datetime(2016,1,1)
end = datetime.date.today()

#
s = "AAPL"
apple = quandl.get("WIKI/" + s, start_date=start, end_date=end)

print(type(apple))
print(apple.columns)
