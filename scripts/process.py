import os
import urllib
import csv

cache = 'cache'
if not os.path.exists(cache):
    os.makedirs(cache)

dest = os.path.join(cache, 'worldbank-gdp.csv')
urllib.urlretrieve('http://api.worldbank.org/indicator/NY.GDP.MKTP.CD?format=csv', dest)

# TODO: use worldbank api v2 (it returns a zip file)
# urllib.urlretrieve('http://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.CD?downloadformat=csv', dest)

fo = open(dest)
lines = [row for row in csv.reader(fo)]
headings = lines[0]
lines = lines[1:]

outheadings = ['Country Name', 'Country Code', 'Year', 'Value']
outlines = []

for row in lines:
    for idx, year in enumerate(headings[2:]):
        if row[idx+2]:
            # do not convert to float as we end up with scientific notation
            value = row[idx+2]
            outlines.append(row[:2] + [int(year), value])

writer = csv.writer(open('data/gdp.csv', 'w'))
writer.writerow(outheadings)
writer.writerows(outlines)

