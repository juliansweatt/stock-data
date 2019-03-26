#!/usr/bin/env python3
import sys
import requests
import re
from iex import Stock

# Initial URL to Visit
NASDAQ_URL = "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQrender=download"

# Compile Regex Patterns
PATTERN_SYMBOLS = re.compile(r'symbol/([a-z]*)')
PATTERN_NEXT_PAGE = re.compile(r'<a href="(.{90,105})" id="main_content_lb_NextPage"')

def print_to_file(outFile, tickerSet):
    f = open(outFile, "w")
    for ticker in tickerSet:
        f.write(ticker + "\n")
    f.close()
    
def get_tickers_from_url(url, maximum, currentLength):
    # Get Initial Web Page
    response = requests.get(url)

    # Harvest Tickers
    tickers = set(re.findall(PATTERN_SYMBOLS, response.text))

    # Check Tickers for Validity & Limit
    validTickers = set()
    for ticker in tickers:
        if len(validTickers)+currentLength >= maximum:
            print(len(validTickers)+currentLength,"Valid Ticker(s) Found. User Specified Limit Reached.")
            break
        try:
            Stock(ticker).price()
            validTickers.add(ticker)
        except:
            print("Invalid Ticker:", ticker)
    
    return validTickers

def save_tickers(maximum, outfile):
    # Initialize
    validTickers = set()
    currentURL = NASDAQ_URL

    while len(validTickers) < maximum:
        # Collect Tickers
        validTickers.update(get_tickers_from_url(currentURL,maximum,len(validTickers)))

        # Collect New Page URL
        response = requests.get(currentURL)
        currentURL = re.findall(PATTERN_NEXT_PAGE,response.text)[0]

        # Print Valid Ticker Set to Output File
        print_to_file(outfile, validTickers)

        # Announce Page Change
        if len(validTickers) < maximum:
            print("Moving to Next Page", currentURL, "Valid Ticker(s) Found:", len(validTickers),)

if __name__ == '__main__':
    # Input Checking
    if len(sys.argv) != 3 or int(sys.argv[1]) > 150 or int(sys.argv[1]) < 0:
        print("Invalid Input. See Usage.")
    else:
        numTickers = int(sys.argv[1])
        outFileName = sys.argv[2]
        save_tickers(numTickers, outFileName)