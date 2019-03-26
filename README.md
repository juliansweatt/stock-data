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
    * `n` - The maximum number of tickers to save to the output file. _(`n`<= 150)_
    * `fname` - The filename to output ticker list to. If the file does not exist, it will be created. **Caution:** If the file already exists it will be overwritten. 
  * Example: `python3 tickers.py 5 ticker.txt`
    * In this example, the first `5` valid tickers will be written to the file `ticker.txt` in the current directory.
* [fetcher.py](./fetcher.py)
* [query.py](./query.py)
* [predictor.py](./predictor.py)

## Recommended Execution
@todo

## Dependencies
* Python 3
* Modules
    * iex-api-python (`pip3 install iex-api-python`)
    * requests (`pip3 install requests`)
