# import data from CSV
import pandas as pd
import requests
import argparse
import math
import altair as alt

parser = argparse.ArgumentParser()
parser.add_argument("csv_2017", help="a CSV of speedtest results")
parser.add_argument("csv_2018", help="a CSV of speedtest results")
parser.add_argument("csv_2019", help="a CSV of speedtest results")
parser.add_argument("csv_2020", help="a CSV of speedtest results")
args = parser.parse_args()

data_2017 = pd.read_csv(args.csv_2017)
data_2018 = pd.read_csv(args.csv_2018)
data_2019 = pd.read_csv(args.csv_2019)
data_2020 = pd.read_csv(args.csv_2020)

data_2017['Year'] = 2017
data_2018['Year'] = 2018
data_2019['Year'] = 2019
data_2020['Year'] = 2020


combined_data = pd.concat([data_2017, data_2018, data_2019, data_2020])
download_tests_by_user = combined_data[(combined_data["City"] == "Everett")].groupby(["ip", "date"]).max().reset_index()

chart = alt.Chart(download_tests_by_user).mark_bar().encode(
    alt.X("MeanThroughputMbps", bin=alt.Bin(step=25)),
    y='count()',
).facet(
    "Year",
    columns=2
).properties(
    title="Everett Download Speedtests"
)
chart.save('data/finished/everett-download-counts.html')