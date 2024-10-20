import os
import csv
import json
import xlrd
import requests

from datetime import datetime, timedelta

cache = 'cache'
data = '../data/gdp.csv'
url = 'https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.CD?downloadformat=excel'
outheadings = ['Country Name', 'Country Code', 'Year', 'Value']
current_year = datetime.now().year
datapackage = '../datapackage.json'

def create_cache():
    if not os.path.exists(cache):
        os.makedirs(cache)

def create_csv(dct):

    rows = list(zip(dct['Country Name'], dct['Country Code'], dct['Year'], dct['Value']))
    sorted_rows = sorted(rows, key=lambda x: (x[0], x[2]))

    # Write the processed data to a new CSV file
    with open(data, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(outheadings)
        writer.writerows(sorted_rows)

def xldate_to_date(xldate):
    # Excel starts on 1900-01-01 but treats 1900 as a leap year (so we subtract 1 day)
    start_date = datetime(1899, 12, 30)
    converted_date = start_date + timedelta(days=xldate)
    return converted_date.strftime('%Y-%m-%d')


def update_datapackage(last_updated):
    with open(datapackage, 'r') as f:
        dp = json.load(f)

    dp['last_updated'] = str(last_updated)
    dp['version'] = str(current_year)

    with open(datapackage, 'w') as f:
        json.dump(dp, f, indent=2)

def process():
    dest = os.path.join(cache, 'worldbank-gdp.xls')
    response = requests.get(url)

    with open(dest, 'wb') as f:
        f.write(response.content)

    workbook = xlrd.open_workbook(dest)
    worksheet = workbook['Data']

    list_rows = list(worksheet.get_rows())

    dct = {
        'Country Name': [],
        'Country Code': [],
        'Year': [],
        'Value': [],
    }
    last_updated = xldate_to_date(list_rows[1][1].value)
    for values in list_rows[4:]:  
        start_year = 1960
        ln = len(values[4:])
        for elem in range(ln):
            if values[4 + elem].value == '':
                continue
            dct['Country Name'].append(values[0].value)
            dct['Country Code'].append(values[1].value)
            dct['Year'].append(start_year)
            dct['Value'].append(values[4 + elem].value)
            start_year += 1

    return dct, last_updated

if __name__ == '__main__':
    create_cache()
    dct, last_updated = process()
    create_csv(dct)
    update_datapackage(last_updated)