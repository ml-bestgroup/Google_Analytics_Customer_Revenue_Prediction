import csv
from pathlib import Path
import json


def flatten_traffic_source(inputfile, outputfile, index):
    
    csvfilename = Path(inputfile)
    outputcsv = Path(outputfile)
    
    #Open files
    csvfile = open(csvfilename, "r")
    reader = csv.reader(csvfile)
    headers = reader.__next__() #get rid of header
    outputfile = open(outputcsv, "w")
    write = csv.writer(outputfile)
    
    keyset = set()

    #Grab set of all keys in traffic source
    for row in reader:
        temp_dict = json.loads(row[index])
        for key in temp_dict:
            keyset.add(key)
    
    #Create new header row
    new_headers = headers[0:index]
    for key in keyset:
        new_headers.append(key)
    new_headers = new_headers + headers[index+1:]
    write.writerow(new_headers)
    
    #Convert each row to flattened new headers
    csvfile = open(csvfilename, "r")
    reader = csv.reader(csvfile)
    throwout = reader.__next__()
    for row in reader:
        temp_dict = json.loads(row[index])
        flat_list_expansion=[]
        for key in keyset:
            if key in temp_dict: flat_list_expansion.append(temp_dict[key])
            else: flat_list_expansion.append("NA")
        newrow = row[0:index]
        newrow = newrow + flat_list_expansion
        newrow = newrow + row[index+1:]
        write.writerow(newrow)
    
    outputfile.close()
