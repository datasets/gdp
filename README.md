Country, regional and world GDP in current US Dollars ($). Regional means
collections of countries e.g. Europe & Central Asia. Data is sourced from the
World Bank and turned into a standard normalized CSV (code can be found in
process.py of data package repository).

## Source

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

