<a className="gh-badge" href="https://datahub.io/core/gdp"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

Country, regional and world GDP in current US Dollars ($). Regional means
collections of countries e.g. Europe & Central Asia.

## Data

The data is sourced from the World Bank (specifically [this dataset][current]) which
in turn lists as sources: *World Bank national accounts data, and OECD National
Accounts data files*.

Note that there are a variety of different GDP indicators on offer from the
World Bank including:

* [GDP in current USD][current]
* [GDP in constant USD (2000)][constant]
* [GDP, PPP (constant 2005 international $)][ppp]
* [GDP (constant LCU)][lcu]

[constant]: http://data.worldbank.org/indicator/NY.GDP.MKTP.KD
[current]: http://data.worldbank.org/indicator/NY.GDP.MKTP.CD
[ppp]: http://data.worldbank.org/indicator/NY.GDP.MKTP.PP.KD
[lcu]: http://data.worldbank.org/indicator/NY.GDP.MKTP.KN


## Data notes

- `data/gdp.csv` is regenerated automatically each month by `scripts/process.py`.
- `data/top-economies.csv` is derived from `gdp.csv` by the same script: it covers the 10 largest economies (by latest-year GDP) from 2000 onward, with values in USD trillions.

## Preparation

Process is recorded and automated in python script:

```
scripts/process.py
```

## Automation

Up-to-date (auto-updates every month) gdp dataset could be found on the datahub.io:
https://datahub.io/core/gdp

## License

This dataset is made available under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/) (CC BY 4.0).

The underlying data originates from the [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD), which publishes its open data under CC BY 4.0. Attribution: World Bank – World Development Indicators.
