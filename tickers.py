#!/usr/bin/env python3
"""Generate a file of stock tickers.

Example:
    $ python3 tickers.py 113 out.txt
"""

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
    """Prints a set to a file.

        Prints a set to an output file, such that each element of the
        set is a new line of the file.

        Args:
            outfile (str): The name/path of the output file.
            tickerSet (set): Set to print to the outfile
    """

    f = open(outFile, "w")
    for ticker in tickerSet:
        f.write(ticker + "\n")
    f.close()

def get_tickers_from_url(url, maximum, currentTickers):
    """Gets stock tickers from a specified NASDAQ url.

        Function retrieves a maximum amount of tickers from a specified URL.
        A NASDAQ URL is expected. The maximum quantity takes in to account the current
        amount of tickers already found outside the function. The function will return whenever
        the maximum is reached or the page tickers are exhausted. The intent is to feed this 
        function each successive page URL. Depends upon the PATTERN_SYMBOLS global variable.

        Args:
            url (str): URL to retrieve stock data from.
            maximum (int): The maximum number of tickers to retrieve. 0 <= maximum <= 150.
            currentTickers: The current amount of tickers already retrieved.

        Returns:
            set: A set of tickers (str).
    """

    # Get Initial Web Page
    response = requests.get(url)

    # Harvest Tickers
    tickers = set(re.findall(PATTERN_SYMBOLS, response.text))

    # Check Tickers for Validity & Limit
    validTickers = set()
    for ticker in tickers:
        if len(validTickers)+currentTickers >= maximum:
            print(len(validTickers)+currentTickers,"Valid Ticker(s) Found. User Specified Limit Reached.")
            break
        try:
            Stock(ticker).price()
            validTickers.add(ticker)
        except:
            print("Invalid Ticker:", ticker)

    return validTickers

def save_tickers(maximum, outfile):
    """Save a specified quantity of tickers to an output file.

        Saves a maximum number of tickers to an output file, such
        that each line in the output file is a ticker string.
        Depends upon the PATTERN_NEXT_PAGE global variable to set the
        pattern for finding the next page and the NASDAQ_URL global variable 
        for the first URL.

        Args:
            maximum (int): The maximum number of tickers to retrieve from NASDAQ.
            outfile (str): The name and path to the output file.
    """
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