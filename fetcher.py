#!/usr/bin/env python3
import sys
import time
import datetime

def getTickers(fName):
    tickers = set()

    try:
        f = open(fName,"r")
        for line in f:
            tickers.add(line[:-1])
        f.close()
    except:
        print("Error While Accessing the Ticker File.")
        return

    return tickers

if __name__ == '__main__':
    # Collect System Arguments
    timeLimit = int(sys.argv[1])
    tickerFname = sys.argv[2]
    infoFname = sys.argv[3]

    # Collect Stock Tickers
    print(getTickers(tickerFname)) # Printing for debugging

    # Timed Execution
    endTime = time.time() + timeLimit
    currentMinute = datetime.datetime.now().minute
    while time.time() < endTime:
        if(datetime.datetime.now().minute != currentMinute):
            print("Updating Stock Data")
            # Execute Update Here
            currentMinute = datetime.datetime.now().minute
    print("Time Limit Has Expired at", datetime.datetime.now().time())