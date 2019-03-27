import sys

def getdata(verbose, fname, tick, time):
    infile = open(fname, "r")
    for line in infile:
        if time in line and tick in line:
            print("check for debugging")

if __name__ == "__main__":
    if len(sys.argv) != 9 or sys.argv[1] != "-verbose" or sys.argv[3] != "-file" or sys.argv[5] != "-ticker" or sys.argv[7] != "-time":
        print("Invalid input. See usage.")
    else:
        verbosity = sys.argv[2]
        fname = sys.argv[4]
        ticker = sys.argv[6]
        time = sys.argv[8]
        getdata(verbosity, fname, ticker, time)

