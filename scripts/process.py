import os
import io
import csv
import json
import zipfile
import requests

from datetime import datetime

cache = 'cache'
script_dir = os.path.dirname(os.path.abspath(__file__))
gdp_path = os.path.join(script_dir, '..', 'data', 'gdp.csv')
top_economies_path = os.path.join(script_dir, '..', 'data', 'top-economies.csv')
datapackage_path = os.path.join(script_dir, '..', 'datapackage.json')
url = 'https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.CD?downloadformat=csv'
outheadings = ['Country Name', 'Country Code', 'Year', 'Value']
current_year = datetime.now().year

# World Bank codes that are regional/income-group aggregates, not individual countries.
# Used as a fallback filter when the Metadata_Country file is unavailable.
WB_AGGREGATE_CODES = {
    'AFE', 'AFW', 'ARB', 'CEB', 'CSS', 'EAP', 'EAR', 'EAS', 'ECA', 'ECS',
    'EMU', 'EUU', 'FCS', 'HIC', 'HPC', 'IBD', 'IBT', 'IDA', 'IDB', 'IDX',
    'LAC', 'LCN', 'LDC', 'LIC', 'LMC', 'LMY', 'LTE', 'MEA', 'MIC', 'MNA',
    'NAC', 'OEC', 'OED', 'OSS', 'PRE', 'PSS', 'PST', 'SAS', 'SSA', 'SSF', 'SST',
    'TEA', 'TEC', 'TLA', 'TMN', 'TSA', 'TSS', 'UMC', 'WLD',
}


def search_files_in_cache():
    cache_dir = os.path.join(script_dir, cache)

    if not os.path.exists(cache_dir):
        print("Cache folder does not exist!")
        return None

    filtered_files = [f for f in os.listdir(cache_dir) if 'metadata' not in f.lower()]

    if not filtered_files:
        print("No valid files found in cache.")
        return None

    return filtered_files


def get_country_codes_from_metadata():
    """Return the set of individual-country codes from the WB Metadata_Country file.

    Countries have a non-blank Region field; aggregates do not.
    Falls back to reading gdp.csv and excluding known aggregate codes if the
    metadata file is absent (e.g. when running locally without a fresh cache).
    Returns None only if neither source is available.
    """
    cache_dir = os.path.join(script_dir, cache)
    if os.path.exists(cache_dir):
        metadata_files = [f for f in os.listdir(cache_dir) if 'Metadata_Country' in f]
        if metadata_files:
            meta_path = os.path.join(cache_dir, metadata_files[0])
            country_codes = set()
            with open(meta_path, 'r') as f:
                for row in csv.DictReader(f):
                    if row.get('Region', '').strip():
                        country_codes.add(row['Country Code'])
            return country_codes

    # Fallback: derive from gdp.csv by excluding known aggregate codes
    if os.path.exists(gdp_path):
        all_codes = set()
        with open(gdp_path, 'r') as f:
            for row in csv.DictReader(f):
                all_codes.add(row['Country Code'])
        return all_codes - WB_AGGREGATE_CODES

    return None


def generate_top_economies(gdp_csv, top_economies_csv, start_year=2000, n=10):
    """Derive top-economies.csv from gdp.csv.

    Selects the n countries with the highest GDP in the latest available year,
    then writes all their rows from start_year onward with GDP in USD trillions.
    Returns (start_year, latest_year).
    """
    country_codes = get_country_codes_from_metadata()

    country_data = {}
    with open(gdp_csv, 'r') as f:
        for row in csv.DictReader(f):
            if country_codes is not None and row['Country Code'] not in country_codes:
                continue
            country = row['Country Name']
            year = int(row['Year'])
            country_data.setdefault(country, {})[year] = float(row['Value'])

    latest_year = max(y for d in country_data.values() for y in d)
    top_countries = sorted(
        (c for c in country_data if latest_year in country_data[c]),
        key=lambda c: country_data[c][latest_year],
        reverse=True
    )[:n]

    rows = [
        [country, year, round(country_data[country][year] / 1e12, 4)]
        for country in top_countries
        for year in sorted(y for y in country_data[country] if y >= start_year)
    ]

    with open(top_economies_csv, 'w', newline='') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(['country', 'year', 'gdp_trillion'])
        writer.writerows(rows)

    return start_year, latest_year


def transform_csv(dest):
    with open(dest, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        next(reader)
        updated_date_row = next(reader)
        last_updated_date = updated_date_row[1].split("-")
        last_updated_date = f"{last_updated_date[0]}-{last_updated_date[1]}-{last_updated_date[2]}"

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


def update_datapackage(last_updated, top_start_year, top_end_year):
    with open(datapackage_path, 'r') as f:
        dp = json.load(f)

    dp['last_updated'] = str(last_updated)
    dp['version'] = str(current_year)

    year_range = f"{top_start_year}–{top_end_year}"
    for resource in dp['resources']:
        if resource['name'] == 'top-economies':
            resource['description'] = (
                f"GDP in current USD trillions for the world's 10 largest economies, "
                f"covering {year_range}. Derived from the main gdp resource."
            )
    for view in dp.get('views', []):
        if view.get('name') == 'top-economies':
            view['title'] = f"GDP of the World's 10 Largest Economies ({year_range})"

    with open(datapackage_path, 'w') as f:
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
    extract_zip()
    file_name = search_files_in_cache()[0]
    dest = os.path.join(script_dir, cache, file_name)
    last_updated, transformed_data = transform_csv(dest)

    os.makedirs(os.path.dirname(gdp_path), exist_ok=True)

    with open(gdp_path, 'w', newline='') as outfile:
        writer = csv.writer(outfile, lineterminator='\n')
        writer.writerow(outheadings)
        writer.writerows(transformed_data)

    start_year, end_year = generate_top_economies(gdp_path, top_economies_path)
    update_datapackage(last_updated, start_year, end_year)


if __name__ == '__main__':
    process()
