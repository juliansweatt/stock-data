#!/usr/bin/env python3
import sys
import time
import datetime
import os
from iex import Stock

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
    tickerSet = getTickers(tickerFname)

    # Setup for Print File
    exists = os.path.isfile(infoFname)
    outfile = open(infoFname, "a")
    if not exists:
        # Appending to File
        outfile.write("Time, Ticker, latestPrice, latestVolume, Close, Open, low, high\n")
    outfile.flush()

    # Timed Execution
    endTime = time.time() + timeLimit
    currentMinute = datetime.datetime.now().minute
    firstPass = True
    while time.time() < endTime:
        if firstPass or (datetime.datetime.now().minute != currentMinute):
            outfile = open(infoFname, "a")
            if firstPass:
                print("Retrieving Stock Data")
                firstPass = False
            else:
                print("Updating Stock Data for", datetime.datetime.now().time())

            # Execute Update Here
            for ticker in tickerSet:
                tickInfo = Stock(ticker).quote()
                tickStr = str(datetime.datetime.now().hour) + ":" + str(currentMinute) + ", " + ticker + ", " + str(tickInfo["latestPrice"]) + ", "
                tickStr = tickStr + str(tickInfo["latestVolume"]) + ", " + str(tickInfo["close"]) + ", " + str(tickInfo["open"]) + ", "
                tickStr = tickStr + str(tickInfo["low"]) + ", " + str(tickInfo["high"]) + "\n"
                outfile.write(tickStr)
            currentMinute = datetime.datetime.now().minute
            outfile.flush()
    print("Time Limit Has Expired at", datetime.datetime.now().time())
    outfile.close()