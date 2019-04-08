#!/usr/bin/env python3
"""Generate a Graphical Prediction from Known Stock History

Examples:
    $ python3 predictor.py jobs info.csv graph.png latestPrice 10
    $ python3 predictor.py aapl alldata.csv prediction latestVolume 100
    $ python3 predictor.py googl sample.csv future.svg latestVolume 3
"""

import datetime
import argparse
import csv
import numpy
import matplotlib.pyplot
import matplotlib.dates
from sklearn import linear_model

def valid_graph_file(s):
    """Determine if graph output file is valid.

    Determine is the graph output file/path provided is valid. Valid files must
    end in one of these extensions: "eps", "pdf", "pgf", "png", "ps", "raw", "rgba", "svg", "svgz".
    If the file exists, consent to overwrite will be requested from standard input. 

    Args:
        s (str): Graph filename/path to verify.

    Returns:
        s(str): Returns the filename if valid, exits program if invalid or consent to override not gained.
    """

    # Check for Appropriate File Ending
    fname = str()
    validExtensions = ["eps", "pdf", "pgf", "png", "ps", "raw", "rgba", "svg", "svgz"] # Extensions Supported by matplotlib
    if s.find('.') < 0:
        # No File Ending, Insert Default .png
        fname = s + ".png"
    else:
        # File Ending
        fname = s
        if fname[s.find('.')+1:] not in validExtensions:
            exit(fname[s.find('.')+1:] + " Is Not A Valid Graph File Extension. Predictor Aborted.")

    # Check for Existing File & Handle Overrides by User Consent
    try:
        open(fname, "r")
        # File Exists Already, Check for Overwrite Consent
        consentOverride = str()
        while consentOverride != 'y' or consentOverride != 'n':
            consentOverride = input("The file " + fname + " already exists. Overwrite? [(y)es/(n)o]").lower()
            if consentOverride == 'y' or consentOverride == 'yes':
                return s
            elif consentOverride == 'n' or consentOverride == 'no':
                exit("User Did Not Constent to Overwrite " + fname + " Predictor Aborted.")
            else:
                print("Invalid Response! Please choose 'y' or 'n'.")
    except IOError as e:
        # File Does Not Exist
        return s

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
    parser.add_argument("graph_filename", type=valid_graph_file, help="Filename/Path to Output Graph")
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
            data.append((row["Time"], float(row[col])))

    if len(data) > 1:
        return data
    else:
        print("No Instances of the Ticker", ticker, "Found in", fName)
        exit()

def plot(ticker, x_actual, y_actual, x_predict=[], y_predict=[], graph_filename="graph.png", col=""):
    """Save a plot/graph to specified file.

    Args:
        ticker (str): Name of Ticker Being Plotted
        x_actual (2D datetime Array): Set of known x values. 
        y_actual (2D int Array): Set of known y values. 
        x_predict (2D datetime Array): Set of predicted x values 
        y_predict (2D int Array): Set of predicted y values. 
        graph_filename (str): Filename/path of output file.
        col(str): `latestPrice` or `latestVolume` depending on targeted prediction. 
    """

    # Configure Plot
    plt = matplotlib.pyplot
    plt.xlabel("Time (HH:MM)")                                      # Set X-Axis Label
    plt.ylabel(col)                                                 # Set Y-Axis Label
    plt.title("Actual & Predicted Stock Data of " + ticker.upper()) # Set Title
    plt.plot(x_actual, y_actual, "b.", label="Actual")              # Plot Known Data in Blue
    plt.plot(x_predict, y_predict, "r.", label="Prediction")        # Plot Prediction Data in Red
    plt.legend()                                                    # Generate Legend
    plt.gcf().autofmt_xdate()                                       # Format for Dates
    formatHHMM = matplotlib.dates.DateFormatter('%H:%M')            # Restrict Dates to HH:MM
    plt.gca().xaxis.set_major_formatter(formatHHMM)                 # Assign Format

    # Save Plot
    plt.savefig(graph_filename)

def convertMinutesToTime(timeInt):
    """Convert minutes (integer) to a time object.

    Args:
        timeInt (int): Time represented in minutes.

    Returns:
        (datetime.time): Time object.
    """
    hour = int(timeInt / 60)
    minute = timeInt-(hour*60)
    return datetime.datetime(1,1,1,hour,minute)

def convertToMinutes(time):
    """Convert a time string (HH:MM) to a minute integer

    Convert a time string (HH:MM) to a minute integer such that 00:00 is 0 minutes
    and 23:00 is 1380 minutes for example.

    Args:
        time (str): Time string in the form HH:MM

    Returns:
        (int): Minute representation of the time.
    """
    hour = int(time[:2])
    minute = int(time[3:])
    hour *= 60
    return hour + minute

def predictor(ticker, info_filename, graph_filename, col, t):
    """Generate a linear regression prediction graph from known stock data.

    Args:
        ticker (str): Valid Stock Ticker to Predict.
        info_filename (str): Valid Input CSV Info Filename/Path of Stock Data
        graph_filename (str): Valid Output Graph Filename/Path
        col (str): Column to Predict ('latestPrice' or 'latestVolume')
        t (int): Time in Minutes to Predict
    """

    # Initialize Predictor
    reg = linear_model.LinearRegression()

    # Harvest Data from CSV
    allData = queryTicker(info_filename, ticker, col)

    # Split X/Y Pairs
    x_values, y_values = zip(*allData)

    # Convert Time to Minutes
    x_trainer = []
    for x in x_values:
        x_trainer.append(convertToMinutes(x))
    
    # Generate Prediction Times
    x_predict = []
    first_predict = x_trainer[len(x_trainer)-1] + 1
    for i in range(first_predict, first_predict+t):
        x_predict.append(i)

    # Convert to 2D Arrays
    x_trainer = numpy.reshape(x_trainer, (-1,1))
    y_trainer = numpy.reshape(y_values, (-1,1))
    x_predict = numpy.reshape(x_predict, (-1,1))

    # Train Model
    reg.fit(x_trainer, y_trainer)

    # Make DateTimes
    x_trainer_time = []
    for x in x_trainer:
        x_trainer_time.append([convertMinutesToTime(x)])

    x_prediction_time = []
    for x in x_predict:
        x_prediction_time.append([convertMinutesToTime(x)])

    # Generate Prediction from the Model
    prediction_model = reg.predict(x_predict)

    # Plot Known Data With Prediction Data
    plot(ticker, x_trainer_time, y_trainer, x_prediction_time, prediction_model, graph_filename, col)

if __name__ == "__main__":
    # Parse Arguments
    args = parseInput()

    # Generate Prediction
    predictor(args.ticker, args.info_filename, args.graph_filename, args.col, args.t)
