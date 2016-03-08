import csv
import os
import re
import pprint

# Result is a nested dict
# First key is the filename
# Second key is the PeakID
# Values is the rest of the fields
result = {}

for file_name in os.listdir():
    if file_name.endswith(".anno"):
        result[file_name] = {}

        with open(file_name) as file_anno:
            # PeakID field has extra 'junk' so extra processing is needed
            fields = file_anno.readline().split('\t')
            fields[0] = 'PeakID'
            
            reader = csv.DictReader(file_anno, fieldnames=fields, delimiter='\t')
            for row in reader:
                # Get value of PeakID and remove it from values
                key = row.pop('PeakID')
                # PeakID : { Other Values }
                result[file_name][key] = row

