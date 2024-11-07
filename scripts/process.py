import os
import io
import csv
import json
import zipfile
import requests

from datetime import datetime, timedelta

cache = 'cache'
data = 'data/gdp.csv'
script_dir = os.path.dirname(os.path.abspath(__file__))
url = 'https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.CD?downloadformat=csv'
outheadings = ['Country Name', 'Country Code', 'Year', 'Value']
current_year = datetime.now().year
datapackage = '../datapackage.json'

def search_files_in_cache():
    cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache')

    if not os.path.exists(cache_dir):
        print("Cache folder does not exist!")
        return None

    filtered_files = [f for f in os.listdir(cache_dir) if 'metadata' not in f.lower()]

    if not filtered_files:
        print("No valid files found in cache.")
        return None

    return filtered_files


def transform_csv(dest):
    with open(dest, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        next(reader)
        updated_date_row = next(reader)
        last_updated_date = updated_date_row[1].split("-")
        last_updated_date = f"{last_updated_date[0]}-{last_updated_date[2]}-{last_updated_date[1]}"

        next(reader) 
        header = next(reader)
        transformed_data = []
        for row in reader:
            country_name = row[0]  
            country_code = row[1]  

            for i in range(4, len(row)):
                year = header[i]
                value = row[i]

                if value:
                    transformed_data.append([country_name, country_code, year, value])
    
    return last_updated_date, transformed_data

def update_datapackage(last_updated):
    with open(datapackage, 'r') as f:
        dp = json.load(f)

    dp['last_updated'] = str(last_updated)
    dp['version'] = str(current_year)

    with open(datapackage, 'w') as f:
        json.dump(dp, f, indent=2)

def extract_zip():
    cache_dir = os.path.join(script_dir, cache)

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(path=cache_dir)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the file: {e}")
        return


def process():
    extract_zip()  # Ensure ZIP extraction happens first
    file_name = search_files_in_cache()[0]
    dest = os.path.join(script_dir, cache, file_name)
    last_updated, transformed_data = transform_csv(dest)

    output_dir = os.path.dirname('data/')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(os.path.abspath(data), 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(outheadings)
        writer.writerows(transformed_data)

    update_datapackage(last_updated)
    
if __name__ == '__main__':
    process()
