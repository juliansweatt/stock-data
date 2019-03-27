# Stock Data Project
__CIS4930 - Python Programming__  
_Hannah Howard & Julian Sweatt_

---
## About
@todo

## Contents
* [README.md](./README.md) _This File_ | Project Details & Information Written in Markdown
* [tickers.py](./tickers.py) Generates File of Valid Stock Tickers
* [fetcher.py](./fetcher.py) @todo
* [query.py](./query.py) @todo
* [predictor.py](./predictor.py) @todo

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
* [predictor.py](./predictor.py)

## Recommended Execution
@todo

## Dependencies
* Python 3
* Modules
    * iex-api-python (`pip3 install iex-api-python`)
    * requests (`pip3 install requests`)
