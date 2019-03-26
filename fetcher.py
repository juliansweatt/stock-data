#!/usr/bin/env python3
import sys

def getTickers(fName):
    tickers = set()

    try:
        f = open(fName,"r")
        for line in f:
            tickers.add(line[:-1])
        f.close()
    except:
        print("Error While Accessing the Ticker File.")

    return tickers

if __name__ == '__main__':
    timeLimit = int(sys.argv[1])
    tickerFname = sys.argv[2]
    infoFname = sys.argv[3]
    print(getTickers(tickerFname)) # Printing for debugging