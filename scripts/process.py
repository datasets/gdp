import os
import urllib.request
import csv
from zipfile import ZipFile

cache = 'cache'
if not os.path.exists(cache):
    os.makedirs(cache)

dest = os.path.join(cache, 'worldbank-gdp.zip')

urllib.request.urlretrieve('http://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.CD?downloadformat=csv', dest)
with ZipFile(dest, 'r') as zObject:
  
    # Extracting all the members of the zip 
    # into a specific location.
    zObject.extractall(
        path=os.path.join(cache, "data"))

datapath = os.path.join(cache, "data", "API_NY.GDP.MKTP.CD_DS2_en_csv_v2_5728855.csv")

fo = open(datapath)
lines = [row for row in csv.reader(fo)]
headings = lines[4]
lines = lines[5:]

outheadings = [*headings[:2], 'Year', 'Value']
outlines = []

for row in lines:
    for idx, year in enumerate(headings[4:]):
        if row[idx+4]:
            # do not convert to float as we end up with scientific notation
            value = row[idx+4]
            outlines.append(row[:2] + [int(year), value])

writer = csv.writer(open('data/gdp.csv', 'w'))
writer.writerow(outheadings)
writer.writerows(outlines)

