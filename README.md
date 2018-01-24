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


## Preparation

Process is recorded and automated in python script:

```
scripts/process.py
```

## Automation

Up-to-date (auto-updates every year) gdp dataset could be found on the datahub.io:
https://datahub.io/core/gdp

## License

This Data Package is made available under the Public Domain Dedication and License v1.0 whose full text can be found at: http://www.opendatacommons.org/licenses/pddl/1.0/