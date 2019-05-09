# Stock Data Project
__CIS4930 - Python Programming__  
_Julian Sweatt & Hannah Howard_

---
## About
This suite of stock-data analysis tools is intended to collect tickers from the NASDAQ website in an intentionally unorthodox way (HTML Parsing), verify them, and save them to a list. This list can then be used to fetch minute-incremental stock data information and save stock history in CSV format. This CSV stock history data can then be queried or used to predict future stock information using a linear regression machine learning model. 

## Contents
* [README.md](./README.md) _This File_ | Project Details & Information Written in Markdown
* [tickers.py](./tickers.py) Generates File of Valid Stock Tickers
* [fetcher.py](./fetcher.py) Gets Periodic Stock Information in CSV Format
* [query.py](./query.py) Query a CSV file for a Particular Ticker at a Given Time.
* [predictor.py](./predictor.py) Generate a Graph of Predicted Stock Data from Known Stock History Data

## Usage
* [tickers.py](./tickers.py)  
  * Usage: `python3 tickers.py n fname`
    * `n` _(int)_ - The maximum number of tickers to save to the output file. _(`n`<= 150)_
    * `fname` _(str)_ - The filename to output ticker list to. If the file does not exist, it will be created.
    **Caution:** If the file already exists it will be overwritten. 
  * Example: `python3 tickers.py 5 ticker.txt`
    * In this example, the first `5` valid tickers will be written to the file `ticker.txt` in the current directory.
* [fetcher.py](./fetcher.py)
  * Usage: `python3 fetcher.py timeLimit tickerFname infoFname`
    * `timeLimit` _(int)_ - The duration for which periodic fetches should occur.
    * `tickerFname` _(str)_ - The filename/path to the list of tickers. This file is expected to be
    a plain-text list of validated stock tickers such that each line of the text file contains
    a single valid ticker represented as a string (such as the output of [`tickers.py`](./tickers.py)).
    * `infoFname` _(str)_ - The filename/path to output fetched data to. This file should not be the same
    file as `tickerFname`. Output will be in CSV format, therefore a `.csv` file is advised but not required.
    If the file exists, it will be appended to, if it does not exist, it will be created.
    If the file is being appended to, it is expected that the file was created by this python
    script.
  * Example: `python3 fetcher.py 120 ticker.txt info.csv`
    * In this example, tickers contained in `ticker.txt` will be fetched for basic stock information and saved to
    `info.csv`. After the initial fetch, if the time limit has not expired, the script will busy-wait until the next
    minute (or the time expires, whichever comes first). At the next minute another fetch will be made, appending to the
    `info.csv` file.
* [query.py](./query.py)
  * Usage: `python3 query.py –verbose True/False –file info_filename –ticker ticker –time time`
  * Example: `python3 query.py –verbose False –file info.csv –ticker jobs –time 01:07`
    * In this example, `info.csv` will be queried for a row containing `01:07` as the time and `jobs` as the ticker. If
    such a row exists, relevant data from that row will be printed. The `verbose` flag is set to `False`, so column names and
    row/column lengths of the CSV file will not be printed.
* [predictor.py](./predictor.py)
  * Usage: `python3 predictor.py ticker info_filename graph_filename col t`
    * `ticker` _(str)_ - The stock ticker to predict.
    * `info_filename` _(str)_ - The CSV info filename/path containing stock history. Expected to be the output of `fetcher.py`.
    * `graph_filename` _(str)_ - The output filename/path for the prediction graph being created. Must have no file extension
    (default is `.png`) or a supported file extension (`eps`, `pdf`, `pgf`, `png`, `ps`, `raw`, `rgba`, `svg`, or `svgz`).
    * `col` _(str)_ - The column to predict. Must be `latestPrice` or `latestVolume`.
    * `t` _(int)_ - The duration of time to predict stock data for in minutes.
  * Example: `python3 predictor.py jobs info.csv graph.png latestPrice 10`

## Stock-Data Suite Execution Example 
1. `python3 tickers.py 100 ticker.txt`
    * Retrieve `100` Valid Tickers and Save to `ticker.txt`
2. `python3 fetcher.py 600 ticker.txt info.csv`
    * Collect `600` seconds *(10 Minutes)* of Stock History for Tickers in `ticker.txt` and Save to `info.csv`
    * Note, Collecting Data Outside of *9:30am to 4:00pm EST* Will Yield Only Linear Data as the Market is Closed,
  So Stocks Can Not Change.
3. `python3 query.py -verbose True -file info.csv -ticker jobs -time 15:10`
    * Query `info.csv` for a Row Representing the `jobs` Ticker at `15:10` with Verbose Output
    * Note, the time used in this example is `15:10` but the time used must be during the time frame `fetcher.py` was running.
4. `python3 predictor.py jobs info.csv graph.png latestPrice 10`
    * Predict `10` Minutes of Stock Data for the `jobs` Ticker Using Stock History Data from `info.csv` and Save to `graph.png`.
    * Note, the ticker used in this example is `jobs` but the ticker must have been in `tickers.txt`, used during
    fetching in `fetcher.py` and have corresponding data saved in `info.csv`. A ticker is valid if it can be queried using `query.py`. 

## Dependencies
* Python 3
* Modules
    * iex-api-python
      * **Install:** `pip3 install iex-api-python`
      * **Purpose:** Used to Obtain NASDAQ Stock Data
    * requests
      * **Install:** `pip3 install requests`
      * **Purpose:** Used for HTTP Requests
    * argparse
      * **Install:** `pip3 install argparse`
      * **Purpose:** Used for Named Argument Parsing
    * sklearn
      * **Install:** `pip3 install sklearn`
      * **Purpose:** Used for Model Training
    * matplotlib
      * **Install:** `pip3 install matplotlib`
      * **Purpose:** Used for Plotting Data
    * numpy
      * **Install:** `pip3 install numpy`
      * **Purpose:** Array Manipulation

## Known Bugs
* Predictor can not predict at a time that exceeds the known day. 
For example, if known data is collected from 07:00 to 10:00,
predictions can not be made past 23:59. However, it doesn't make
much sense to need to predict outside of the current day as the NASDAQ 
market is closed late at night/early in the morning.

# Academic Honesty & Appropriate Use
This repository branch is available on the personal github of Julian Sweatt for academic and professional purposes. The repository is purposefully obfuscated from search engine indexing/crawling to comply with the [Florida State University Academic Honor Policy](https://fda.fsu.edu/sites/g/files/imported/storage/original/application/0ab8e9de6a98c1377d68de9717988bda.pdf). The content of this repository may be used as a reference of the technical abilities of the developer. The content of this repository may not be used by another student to complete an academic assignment in any way.