# `bias_scraper.py`

This is a quick and dirty script designed to scrape some data from `allsides.com`, which tracks media bias. The website does not keep a handy historical archive for study, but it is possible to track their bias ratings over time by looking at copies of their site archived on Wayback Machine. This script accepts an Excel spreadsheet of urls on Wayback machine, downloads the output, and parses out the names of the news sources and their biases. It outputs the results in a CSV file.

## Requirements

 - Python 3.x
 - python-fire (install with `pip install fire`)
 - python-tabulator (install with `pip install tabulator`)
 - An Excel file with input data and the headers `url` and `date` in the first row

## Usage

The script is run off the command line as follows:

```python
python bias_scraper.py --source=path_to_excel_file --output=path_to_output_csv_file
```

Other command flags are

- `--help`: A list of all arguments and their usage
- `--save`: If `False`, the script will output the CSV data to the terminal but will not save it as a file. Default is `True`
- `--mode`: If `a`, the script will append the output to a previously existing output file instead of creating a new one. Default is `w`.