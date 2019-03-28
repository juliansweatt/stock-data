#!/usr/bin/env python3
import argparse
import csv
from sklearn import linear_model
import matplotlib.pyplot

def valid_file(s):
    """Verifies a filename/path.

    Args:
        s (str): Filename/path to validate.
    
    Returns:
        (str): Returns the filename/path if valid or exits if invalid.
    """
    try:
        open(s, "r")
        return s
    except IOError as e:
        exit(e)

def parseInput():
    """Parse arguments from standard input.

    Returns:
        Returns arguments object.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("ticker", type=str, help="Stock Ticker to Predict")
    parser.add_argument("info_filename", type=valid_file, help="Filename/Path to Info CSV File")
    parser.add_argument("graph_filename", type=str, help="Filename/Path to Output Graph")
    parser.add_argument("col", type=str, choices=("latestPrice", "latestVolume"), help="Column to Predict")
    parser.add_argument("t", type=int, help="Duration to Predict in Minutes")
    return parser.parse_args()

def queryTicker(fName, ticker, col):
    """Query CSV info file for all entries of a ticker.

    Args:
        fname (str): Filename/path to CSV info file.
        ticker (str): Ticker to query.
    
    Returns:
        (list): Returns all entries related to the ticker.
    """
    data = list()

    f = open(fName, "r")
    info = csv.DictReader(f)

    for row in info:
        if row["Ticker"] == ticker:
            data.append((row["Time"], row[col]))

    if len(data) > 1:
        return data
    else:
        print("No Instances of the Ticker", ticker, "Found in", fName)
        exit()

def plot(ticker, x_actual, y_actual, x_predict=[], y_predict=[], graph_filename="graph.png", col=""):
    """Save a plot/graph to specified file.

    Args:
        ticker (str): Name of Ticker Being Plotted
        x_actual: Set of known x values.
        y_actual: Set of known y values.
        x_predict: Set of predicted x values.
        y_predict: Set of predicted y values.
        graph_filename (str): Filename/path of output file.
        col(str): `latestPrice` or `latestVolume` depending on targeted prediction. 
    """
    # Configure Plot
    plt = matplotlib.pyplot
    plt.xlabel("Time (HH:MM)")
    plt.ylabel(col)
    plt.title("Actual & Predicted Stock Data of " + ticker.upper())
    plt.plot(x_actual,y_actual,"b.", label="Actual")          # Plot Known Data in Blue
    plt.plot(x_predict,y_predict,"r.", label="Prediction")    # Plot Prediction Data in Red
    plt.legend()

    # Save Plot
    plt.savefig(graph_filename)
    #plt.show()

def predictor(ticker, info_filename, graph_filename, col, t):
    from sklearn.model_selection import train_test_split  

    # Initialize Predictor
    reg = linear_model.LinearRegression()

    # Harvest Data from CSV
    allData = queryTicker(info_filename, ticker, col)

    # Split X/Y Pairs
    x,y = zip(*allData)

    # Split Values into Training & Test Data

    # reg.fit(train_data_X,train_data_Y)
    # print(reg.predict(trainer))

    # Plot Known Data With Prediction Data
    plot(ticker, x, y, x, y, graph_filename, col)

if __name__ == "__main__":
    # Parse Arguments
    args = parseInput()

    predictor(args.ticker, args.info_filename, args.graph_filename, args.col, args.t)
