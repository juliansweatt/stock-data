import argparse
import re

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
    parser.add_argument("-verbose", type=strbool, choices=(True,False), required=False, default=False, help="Enable Verbose Output")
    parser.add_argument("-file", type=str, required=True, help="Specify Info Filename/Path")
    parser.add_argument("-ticker", type=str, required=True, help="Specify Ticker to Query")
    parser.add_argument("-time", type=validtime, required=True, help="Specify Time to Query")
    return parser.parse_args()
    print(args.verbose, args.file, args.ticker, args.time)

def getdata(verbose, fname, tick, time):
    infile = open(fname, "r")
    for line in infile:
        if time in line and tick in line:
            print("check for debugging")

if __name__ == "__main__":
    # Parse Named Arguments With Argsparse
    args = parseInput()

    # Get Data
    getdata(args.verbose, args.file, args.ticker, args.time)