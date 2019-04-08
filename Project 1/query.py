#!/usr/bin/env python3
"""Query a CSV file for a particular ticker at a given time.

Examples:
    $ python3 query.py -ticker appl -file x.csv -verbose True -time 16:11
    $ python3 query.py –verbose False –file info.csv –ticker jobs –time 01:07
"""
import argparse
import re
import csv

def strbool(s):
    """Convert string value to bool type. 

    Convert the string values 'True' or 'False' to their
    respective boolean values, or returns the original string
    if there are no valid matches.

    Args:
        s (str): String to convert to bool.

    Returns:
        (bool/str) Returns boolean equivalent if valid, else returns original string.
    """
    if s == "False":
        return False
    elif s == "True":
        return True
    else:
        return s

def validtime(s):
    """Validates time strings.

    If the time string is in the form HH:MM such that 00 < HH < 24 and 00 < MM < 59,
    then the string will be returned as valid. Else an exception will be raised.

    Args:
        s (str): Time string to be validated

    """
    temp = re.findall(r'^([0-2][0-9]):([0-5][0-9])$', s)
    if len(temp) == 1 and len(temp[0]) == 2:
        return s
    else:
        raise argparse.ArgumentTypeError('Time Format Expected (HH:MM such that 00 < HH < 24 and 00 < MM < 59)')

def parseInput():
    """Parse arguments from standard input.

    Returns:
        Returns arguments object.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-verbose", type=strbool, choices=(True,False), required=True, default=False, help="Enable Verbose Output")
    parser.add_argument("-file", type=str, required=True, help="Specify Info Filename/Path")
    parser.add_argument("-ticker", type=str, required=True, help="Specify Ticker to Query")
    parser.add_argument("-time", type=validtime, required=True, help="Specify Time to Query")
    return parser.parse_args()

def query(fname, tick, time):
    """Query a CSV file for a particular ticker and time stamp.

    Args:
        fname (str): Filename/path to CSV file.
        tick (str): Name of ticker to query.
        time (str): Timestamp to query (HH:MM)

    Returns:
        (OrderedDict) Returns CSV row if a match is found. Returns None otherwise.
    """
    try:
        infile = open(fname, "r")
    except IOError as e:
        exit(e)

    data = csv.DictReader(infile)

    for row in data:
        if row["Time"] == time and row["Ticker"] == tick:
            return row
    
    print("No Entry Found for Ticker", tick, "At", time)
    return

def numRows(fname):
    """Get number of rows in a CSV file.

    Args:
        fname (str): Filename/path to CSV file.
    
    Returns:
        (int) Number of rows in CSV file.
    """
    tally = 0
    try:
        infile = open(fname, "r")
    except IOError as e:
        exit(e)
    data = csv.DictReader(infile)
    for row in data:
        tally += 1
    return tally

def numCols(fname):
    """Get number of columns in a CSV file.

    Args:
        fname (str): Filename/path to CSV file.
    
    Returns:
        (int) Number of columns in CSV file.
    """
    try:
        infile = open(fname, "r")
    except IOError as e:
        exit(e)
    return len(csv.DictReader(infile).fieldnames)

def printEntry(entry, verbose=False, numCols=0, numRows=0):
    """Print a dictionary entry.

    Args:
        entry (OrderedDict): Entry to print. Intended to be the value return of query.
        verbose (bool): [OPTIONAL] Enable printing of query result with names of columns
            and number of columns/rows in the info file.
        numCols (int): [OPTIONAL] Number of columns in the info file. Intended to be provided
            only if verbose is enabled.
        numRows (int): [OPTIONAL] Number of rows in the info file. Intended to be provided
            only if verbose is enabled. 
    """
    if verbose:
        print("Info File Details:")
        print(" Number of Columns:", numCols)
        print(" Number of Rows:", numRows)
        if entry:
            print()
            for key in entry:
                print(key + ": " + entry[key])
    else:
        if entry:
            for i,key in enumerate(entry):
                print("Field", str(i) + ":", entry[key])

if __name__ == "__main__":
    # Parse Named Arguments With Argsparse
    args = parseInput()

    # Get Data
    if args.verbose:
        printEntry(query(args.file, args.ticker, args.time), args.verbose, numCols(args.file), numRows(args.file))
    else:
        printEntry(query(args.file, args.ticker, args.time))