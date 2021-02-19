# import data from CSV
import pandas as pd
import requests
import argparse
import math

parser = argparse.ArgumentParser()
parser.add_argument("csv", help="a CSV of speedtest results from Measurement Lab")
parser.add_argument("threshold", help="the speed threshold to bucket the data by")
args = parser.parse_args()

data = pd.read_csv(args.csv)

def get_provider_name(row):
    # import pdb; pdb.set_trace()
    payload = { 'asn__in': math.nan if math.isnan(row['ProviderNumber']) else int(row['ProviderNumber']) }
    result = requests.get('https://www.peeringdb.com/api/net', params=payload)
    row['ProviderName'] = result.json()['data'][0]['name'] if ('data' in result.json() and len(result.json()['data']) > 0) else None
    return row

# Append Provider Names from the Peering DB API
providers = pd.DataFrame({'ProviderNumber': data.ProviderNumber.unique()})
providers = providers.apply(get_provider_name, axis=1).apply(pd.Series).set_index('ProviderNumber')

# Now Populate the ProviderName column with relevant data
def assign_provider_name(row):
    row['ProviderName'] = providers.loc[row['ProviderNumber'], 'ProviderName']
    return row

import pdb; pdb.set_trace()

data = data.apply(assign_provider_name, axis=1)

import pdb; pdb.set_trace()
tests_by_user = data.groupby(["ip", "date"]).max()

all_speeds = pd.DataFrame(columns=[f'Under {args.threshold} Mbps',f'Over {args.threshold} Mbps',f'Percent Under {args.threshold}',f'Percent Over {args.threshold}','Municipality'])

municipalities = ['Chelsea', 'Revere', 'Everett']
for municipality in municipalities:
    under = tests_by_user[(tests_by_user["MeanThroughputMbps"] <= int(args.threshold)) & (tests_by_user["City"] == municipality)]\
        .groupby("ProviderName")["ProviderName"]\
        .count()\
        .rename(f'Under {args.threshold} Mbps')

    over = tests_by_user[(tests_by_user["MeanThroughputMbps"] > int(args.threshold)) & (tests_by_user["City"] == municipality)]\
        .groupby("ProviderName")["ProviderName"]\
        .count()\
        .rename(f'Over {args.threshold} Mbps')
    
    combined = pd.concat([under,over], axis=1)
    combined[f'Percent Under {args.threshold}'] = combined[f'Under {args.threshold} Mbps'] / (combined[f'Under {args.threshold} Mbps'] + combined[f'Over {args.threshold} Mbps'])
    combined[f'Percent Over {args.threshold}'] = combined[f'Over {args.threshold} Mbps'] / (combined[f'Under {args.threshold} Mbps'] + combined[f'Over {args.threshold} Mbps'])
    combined['Municipality'] = municipality
    all_speeds = all_speeds.append(combined)

all_speeds.to_csv(f"data/finished/totals_{args.threshold}.csv")