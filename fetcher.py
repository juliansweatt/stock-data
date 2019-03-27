#!/usr/bin/env python3
"""Periodically fetch stock ticker data for a set duration.

Example:
    $ python3 fetcher.py 120 ticker.txt info.csv
"""
import sys
import time
import datetime
import os
from iex import Stock

def getTickers(fName):
    """Retrieve a set of tickers from a text file.

        Retrieves a set of tickers from a text file such that each
        line of the text file is a new ticker represented as a 
        string.

        Args:
            fName (str): Filename/path to ticker text file.
        
        Returns:
            set: A set of tickers such that each element is a valid ticker.
    """
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

def makeTimeString(hour, minute):
    """Makes a time string (HH:MM) from hour and minute.

    Args:
        hour (int): Hour.
        minute (int): Minute.
    
    Returns:
        str: String of time in the form HH:MM, substituting 0 as needed.
    """

    timeString = str()
    hourString = str()
    minuteString = str()

    if hour < 10:
        hourString = "0" + str(hour)
    else:
        hourString = str(hour)

    if minute < 10:
        minuteString = "0" + str(minute)
    else:
        minuteString = str(minute)
    
    timeString = hourString + ":" + minuteString

    return timeString

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
        # Initialize File if New
        outfile.write("Time,Ticker,latestPrice,latestVolume,Close,Open,low,high\n")
    outfile.flush()

    # Timed Execution
    endTime = time.time() + timeLimit
    currentMinute = datetime.datetime.now().minute
    firstPass = True
    while time.time() < endTime:
        if firstPass or (datetime.datetime.now().minute != currentMinute):
            # 
            if not exists and firstPass:
                print("Retrieving Stock Data")
                firstPass = False
            else:
                print("Updating Stock Data at", datetime.datetime.now().time())

            # Execute Update Here
            for ticker in tickerSet:
                tickInfo = Stock(ticker).quote()
                tickStr = str(makeTimeString(datetime.datetime.now().hour, datetime.datetime.now().minute) + "," + ticker + "," + str(tickInfo["latestPrice"]) + ",")
                tickStr = tickStr + str(tickInfo["latestVolume"]) + "," + str(tickInfo["close"]) + "," + str(tickInfo["open"]) + ","
                tickStr = tickStr + str(tickInfo["low"]) + "," + str(tickInfo["high"]) + "\n"
                outfile.write(tickStr)
            currentMinute = datetime.datetime.now().minute
            outfile.flush()
    print("Time Limit Has Expired at", datetime.datetime.now().time())
    outfile.close()