""" open General Ledger from Excel, reformat into a database. """
import pandas as pd
import numpy as np
import argparse
from itertools import cycle
from time import sleep


columnNames = ["Account Description", "Type", "Date", "Num", "Name",
            "Memo", "Split", "Amount", "Balance"]


def format_file(df, columnNames=columnNames, columnsToBeMerged = [0,1,2,3,4]):

    df['Account Description'] = merge_columns(df[columnsToBeMerged])

    # clean up empty columns/rows
    df = df.drop(0)
    df = df.drop(columnsToBeMerged, axis=1)
    df = df.dropna(axis=0, thresh=6)
    df = df.dropna(axis=1, how='all')

    # Reindex Columns, move last column to first position
    cols = df.columns.tolist()
    df = df[cols[-1:] + cols[:-1]]
    df.columns = columnNames

    return df


def merge_columns(df):

    # Create single column from DataFrame argument. Value in the merged column
    # will be the first non-NaN value encountered in the row. If the entire row
    # is NaN, it will fill using the previous value in the merged column.

    temp_df = df.copy()
    temp_df = temp_df.replace(' ', np.nan)
    temp_df["mergeColumn"] = [np.nan for _ in df.index]

    for column in temp_df.columns:
        temp_df["mergeColumn"] = temp_df["mergeColumn"].fillna(temp_df[column])

    return temp_df["mergeColumn"].fillna(method='ffill')


def open_file(filename):

    # try to open filename as Pandas DataFrame, if error, quit.
    try:
        df = pd.read_excel(filename, index_col=None, header=None)
        return df
    except:
        print("Error with filename")
        quit()

# progress bar. Unnecessary for functionality and can be omitted.	
def progress(percent=0, width=30):
    left = width * percent // 100
    right = width - left
    print('\r[', '#' * left, ' ' * right, ']',
          f' {percent:.0f}%',
          sep='', end='', flush=True)


def main(file_location):

    file = format_file(open_file(file_location))
    print(f"Reformatting {file_location} in progress.")
    for i in range(101):
    	progress(i)
    	sleep(0.01)
    # consider using Path object for file location, to allow for
    # more accurate location saving.
    file.to_csv("modified_GL.csv", index=False)
    print("")
    print("File Successfully converted.")
    return file


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
                description='Location of Excel File to be formatted.')
    parser.add_argument('file_location', type=str, help='file location')
    args = parser.parse_args()

    main(args.file_location)
