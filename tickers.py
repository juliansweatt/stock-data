#!/usr/bin/env python3
import sys
import requests
import re
from iex import Stock

NASDAQ_URL = "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQrender=download"

def save_tickers(num, outfile):
    response = requests.get(NASDAQ_URL)
    tickers = set(re.findall(r'symbol/([a-z]*)', response.text))

    validTickers = set()

    for ticker in tickers:
        if len(validTickers) >= num:
            print(len(validTickers),"Valid Ticker(s) Found. Limit Reached.")
            break
        try:
            Stock(ticker).price()
            validTickers.add(ticker)
        except:
            print("Invalid Ticker:", ticker)
    
    f = open(outfile, "w")

    for i,ticker in enumerate(validTickers):
        if i < num:
            f.write(ticker + "\n")
        else:
            break

    f.close()

if __name__ == '__main__':
    numTickers = int(sys.argv[1])
    outFileName = sys.argv[2]
    save_tickers(numTickers, outFileName)