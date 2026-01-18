import os
import csv
import sys

def checkCSV(path, headers):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    if not os.path.exists(path): # if the file doesn't exist, create it
        print("Creating CSV storage file ...")
        with open(path, "w",newline="", encoding="utf-8") as f: #as f gives a name to the object returned by open(), it's effectively a file handle
            csv.writer(f).writerow(headers) #write the desired headers to the file handle
            (print("CSV storage file creation successful \n"))