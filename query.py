import argparse
import re
import csv

def strbool(s):
    if s == "False":
        return False
    elif s == "True":
        return True
    else:
        return s

def validtime(s):
    temp = re.findall(r'([0-2][0-9]):([0-5][0-9])', s)
    if len(temp) == 1 and len(temp[0]) == 2:
        return s
    else:
        raise argparse.ArgumentTypeError('Time Format Expected (HH:MM such that 00 < HH < 24 and 00 < MM < 59 )')

def parseInput():
    parser = argparse.ArgumentParser()
    parser.add_argument("-verbose", type=strbool, choices=(True,False), required=True, default=False, help="Enable Verbose Output")
    parser.add_argument("-file", type=str, required=True, help="Specify Info Filename/Path")
    parser.add_argument("-ticker", type=str, required=True, help="Specify Ticker to Query")
    parser.add_argument("-time", type=validtime, required=True, help="Specify Time to Query")
    return parser.parse_args()
    print(args.verbose, args.file, args.ticker, args.time)

def getdata(fname, tick, time):
    try:
        infile = open(fname, "r")
    except IOError as e:
        exit(e)

    data = csv.DictReader(infile)

    for row in data:
        if row["Time"] == time and row["Ticker"] == tick:
            return row
    
    print("No Entry Found for Ticker", tick, "At", time)

def numRows(fname):
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
    try:
        infile = open(fname, "r")
    except IOError as e:
        exit(e)
    return len(csv.DictReader(infile).fieldnames)

def printEntry(entry, verbose=False, numCols=0, numRows=0):
    if verbose:
        print("Info File Details:")
        print(" Number of Columns:", numCols)
        print(" Number of Rows:", numRows)
        if entry:
            print("\n----- Query Results ------")
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
        printEntry(getdata(args.file, args.ticker, args.time), args.verbose,numCols(args.file),numRows(args.file))
    else:
        printEntry(getdata(args.file, args.ticker, args.time))