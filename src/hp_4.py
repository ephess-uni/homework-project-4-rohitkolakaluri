# hp_4.py
#
import csv
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    reformatted_dates = []
    for date_str in old_dates:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        reformatted_date_str = date_obj.strftime('%d %b %Y')
        reformatted_dates.append(reformatted_date_str)

    return reformatted_dates


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str):
        raise TypeError("start must be a string")
    if not isinstance(n, int):
        raise TypeError("n must be an integer")

    dates = []
    current_date = datetime.strptime(start, '%Y-%m-%d')
    for i in range(n):
        dates.append(current_date)
        current_date += timedelta(days=1)
    return dates


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    if not isinstance(start_date, str):
        raise TypeError("start_date should be a string")
    if not isinstance(values, list):
        raise TypeError("values should be a list")
    if not values:
        return []
    dates = date_range(start_date, len(values))
    return list(zip(dates, values))


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    with open(infile, 'r') as csvfile, open(outfile, 'w', newline='') as outfile:
        reader = csv.DictReader(csvfile)
        writer = csv.DictWriter(outfile, fieldnames=['patron_id', 'late_fees'])
        writer.writeheader()
        fee_dict = {}
        for row in reader:
            patron_id = row['patron_id']
            date_due = datetime.strptime(row['date_due'], '%m/%d/%Y')
            date_returned = datetime.strptime(row['date_returned'], '%m/%d/%Y')
            if date_returned > date_due:
                days_late = (date_returned - date_due).days
                late_fee = 0.25 * days_late
                if patron_id in fee_dict:
                    fee_dict[patron_id] += late_fee
                else:
                    fee_dict[patron_id] = late_fee
        for patron_id, late_fee in fee_dict.items():
            writer.writerow({'patron_id': patron_id, 'late_fees': "{:.2f}".format(late_fee)})



# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
