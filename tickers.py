#!/usr/bin/env python3
import sys
import requests
import re

NASDAQ_URL = "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQrender=download"

def save_tickers(num, outfile):
    response = requests.get(NASDAQ_URL)
    tickers = set(re.findall(r'symbol/([a-z]*)', response.text))

if __name__ == '__main__':
    numTickers = sys.argv[1]
    outFileName = sys.argv[2]
    save_tickers(numTickers, outFileName)