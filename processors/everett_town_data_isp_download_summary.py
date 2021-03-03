# import data from CSV
import pandas as pd
import requests
import argparse
import math
import altair as alt

parser = argparse.ArgumentParser()
parser.add_argument("csv_2017", help="a CSV of speedtest result summary statistics")
parser.add_argument("csv_2018", help="a CSV of speedtest result summary statistics")
parser.add_argument("csv_2019", help="a CSV of speedtest result summary statistics")
parser.add_argument("csv_2020", help="a CSV of speedtest result summary statistics")
args = parser.parse_args()

data_2017 = pd.read_csv(args.csv_2017)
data_2018 = pd.read_csv(args.csv_2018)
data_2019 = pd.read_csv(args.csv_2019)
data_2020 = pd.read_csv(args.csv_2020)

data_2017['Year'] = 2017
data_2018['Year'] = 2018
data_2019['Year'] = 2019
data_2020['Year'] = 2020

# Group Data so it is all together.
combined_data = pd.concat([data_2017, data_2018, data_2019, data_2020])
combined_data = combined_data.drop(columns=["Percent Under 25", "Percent Over 25"]).melt(id_vars=["ProviderName","Year"],
    var_name="Speedtest Result Type",
    value_name="Speedtest Count"
)

# combined_data.to_csv(f"data/finished/everett_totals_uploads.csv")

# Create a matrix of charts, one chart per year, with providers on the X axis,
# and the Y axis representing the number of tests, and shading representing
# the split between above and below 25 Mbps for download, and above and below
# 3 Mbps for uploads.

chart = alt.Chart(combined_data).mark_bar().encode(
    x="ProviderName",
    y="Speedtest Count",
    color="Speedtest Result Type"
).facet(
    "Year",
    columns=2
).properties(
    title="Everett Download Speedtests"
)
chart.save('data/finished/everett-chart.html')