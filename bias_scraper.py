# Title: bias_scraper.py
# Author: Scott Kleinman
# Date: 7 February 2018

# Scrapes news sources and biases from allsides.com.
# Requires Python 3.

# To get this to work, you first need to run the following:
    # pip install fire
    # pip install tabulator

# The source file must be an Excel spreadsheet with the following format:

# url	                                                                date
# http://web.archive.org/web/20121030221821/http://www.allsides.com/    01/01/10
# http://web.archive.org/web/20121115135247/http://www.allsides.com/    04/14/10

# The date format shouldn't matter; it will be converted automatically.

import urllib, re, os, csv, datetime
import fire
from tabulator import Stream
from bs4 import BeautifulSoup

def read_page(url):
    # Reads the html from a url and returns a Beautiful Soup object
    f = urllib.request.urlopen(url)
    soup = BeautifulSoup(f.read(), 'html.parser')
    return soup

def print_rows(rows):
    # Prints a list of rows as CSV data to the terminal
    for row in rows:
        print(','.join(row))

def get_row_data(soup, date):
    # Parses a Beautiful Soup object into comma-separated rows of news source, bias, and date
    sources = []
    for source in soup.find_all("div", {"class": "news-source"}):
        sources.append(source.text.strip())
    biases = []
    for bias in soup.find_all("div", {"class": "bias-image"}):
        link = re.sub('\">.+', '', str(bias.a))
        bias = link.split('/')[-1]
        biases.append(bias)
    rows = []
    for i, item in enumerate(sources):
        row = item + ',' + biases[i] + ',' + date
        rows.append(row.split(','))
    return rows

def get_rows(url, date):
    # Fetches the row data
    soup = read_page(url)
    data = get_row_data(soup, date)
    return data

def write_file(rows, mode, date, output):
    # Writes the data rows to a CSV file
    if mode == 'w':
        rows.insert(0, ['Source', 'Bias', 'Date'])
    with open(output, mode, newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)
    print('\nRows successfully written the CSV file for ' + date + '.\n')
    print('=========================================\n')

def execute(kwargs):
    # Execute pipeline if the command has valid arguments
    try:
        mode =  kwargs['mode']
    except:
        mode = 'w'
    try:
        save =  kwargs['save']
    except:
        save = True
    with Stream(kwargs['source'], headers=1, sheet=1) as stream:
        for row in stream:
            date = row[1].strftime('%Y-%m-%d')
            rows = get_rows(row[0], date)
            if save == True:
                write_file(rows, mode, date, kwargs['output'])
            else:
                print_rows(rows)

def validate(**kwargs):
    # Check for valid input from the command line
    valid = True
    help = False
    # Provide output if the --help flag exists
    try:
        assert kwargs['help']
        help = True
        print('\nValid arguments are --source, --output, --save, and --mode.\n')
        print('--source requires a valid path ending in a file with the suffix .xlsx. The first row of your source file must consist of headers.')
        print('--output requires a valid path ending in a file with the suffix .csv.')
        print('--save defaults to True. Setting it to False will print the results without saving.')
        print('--mode defaults to "w". Set it to "a" to append results to a pre-existing file.')
    except:
        pass
    if help == False:
        # Make sure there is a source file
        try:
            assert kwargs['source']
        except:
            print('Please supply a path to the source file using the --source flag.')
            valid = False
        # Make sure there is an output file
        try:
            kwargs['output'].endswith('.csv')
        except:
            print('Please supply a path to the output file using the --output flag. The file must end with ".csv".')
            valid = False
        # Ensure other command-line arguments are valid
        try:
            if kwarg['mode'] not in ['a', 'w']:
                print('The value of "mode" is not valid. Please use either "w" or "a".')
                valid = False
        except:
            pass
        try:
            if kwarg['save'] not in [True, False]:
                print('The value of "save" is not valid. Please use either "True" or "False" (without quotation marks).')
                valid = False
        except:
            pass
        # If command-line arguments are valid, execute the script
        if valid == True:
            execute(kwargs)

if __name__ == '__main__':
    fire.Fire(validate)
