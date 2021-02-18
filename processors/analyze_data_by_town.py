# import data from CSV
import pandas as pd
import requests
import argparse
import math

parser = argparse.ArgumentParser()
parser.add_argument("upload_csv", help="a CSV of speedtest upload results from Measurement Lab")
parser.add_argument("download_csv", help="a CSV of speedtest upload results from Measurement Lab")
args = parser.parse_args()

upload_data = pd.read_csv(args.upload_csv)
download_data = pd.read_csv(args.download_csv)

def get_provider_name(row):
    payload = { 'asn__in': math.nan if math.isnan(row['ProviderNumber']) else int(row['ProviderNumber']) }
    result = requests.get('https://www.peeringdb.com/api/net', params=payload)
    row['ProviderName'] = result.json()['data'][0]['name'] if ('data' in result.json() and len(result.json()['data']) > 0) else None
    return row

# Append Provider Names from the Peering DB API
upload_providers = pd.DataFrame({'ProviderNumber': upload_data.ProviderNumber.unique()})
download_providers = pd.DataFrame({'ProviderNumber': download_data.ProviderNumber.unique()})
providers = upload_providers.append(download_providers)
providers = providers.apply(get_provider_name, axis=1).apply(pd.Series).set_index('ProviderNumber')

# Now Populate the ProviderName column with relevant data
def assign_provider_name(row):
    row['ProviderName'] = providers.loc[row['ProviderNumber'], 'ProviderName']
    return row

upload_data = upload_data.apply(assign_provider_name, axis=1)
download_data = download_data.apply(assign_provider_name, axis=1)

upload_tests_by_user = upload_data.groupby(["ip", "date"]).max()
download_tests_by_user = download_data.groupby(["ip", "date"]).max()

all_speeds = pd.DataFrame(columns=[f'Under 25 Mbps',f'Over 25 Mbps',f'Percent Under 25 Mbps',f'Percent Over 25 Mbps',f'Under 3 Mbps',f'Over 3 Mbps',f'Percent Under 3 Mbps',f'Percent Over 3 Mbps','Municipality'])

municipalities = ['Chelsea', 'Revere', 'Everett']
for municipality in municipalities:
    upload_under = upload_tests_by_user[(tests_by_user["MeanThroughputMbps"] <= 3) & (tests_by_user["City"] == municipality)]\
        .groupby("ProviderName")["ProviderName"]\
        .count()\
        .rename(f'Under 3 Mbps')

    upload_over = upload_tests_by_user[(tests_by_user["MeanThroughputMbps"] > 3) & (tests_by_user["City"] == municipality)]\
        .groupby("ProviderName")["ProviderName"]\
        .count()\
        .rename(f'Over 3 Mbps')
    
    upload_combined = pd.concat([upload_under,upload_over], axis=1)
    upload_combined[f'Percent Under 3 Mbps'] = upload_combined[f'Under 3 Mbps'] / (upload_combined[f'Under 3 Mbps'] + upload_combined[f'Over 3 Mbps'])
    upload_combined[f'Percent Over 3 Mbps'] = upload_combined[f'Over 3 Mbps'] / (upload_combined[f'Under 3 Mbps'] + upload_combined[f'Over 3 Mbps'])
    
    download_under = download_tests_by_user[(tests_by_user["MeanThroughputMbps"] <= 25) & (tests_by_user["City"] == municipality)]\
    .groupby("ProviderName")["ProviderName"]\
    .count()\
    .rename(f'Under 25 Mbps')

    download_over = download_tests_by_user[(tests_by_user["MeanThroughputMbps"] > 25) & (tests_by_user["City"] == municipality)]\
        .groupby("ProviderName")["ProviderName"]\
        .count()\
        .rename(f'Over 25 Mbps')
    
    download_combined = pd.concat([download_under,download_over], axis=1)
    download_combined[f'Percent Under 25 Mbps'] = download_combined[f'Under 25 Mbps'] / (download_combined[f'Under 25 Mbps'] + download_combined[f'Over 25 Mbps'])
    download_combined[f'Percent Over 25 Mbps'] = download_combined[f'Over 25 Mbps'] / (download_combined[f'Under 25 Mbps'] + download_combined[f'Over 25 Mbps'])
    
    combined = pd.concat([upload_combined, download_combined], axis=1)
    all_speeds = all_speeds.append(combined)

all_speeds.to_csv(f"data/finished/totals.csv")