import csv
import os
import re
import pprint

# anno_dict is a nested dict
# First key is the filename
# Second key is the PeakID
# Values is the rest of the fields
anno_dict = {}

for file_name in os.listdir():
    if file_name.endswith(".anno"):
        anno_dict[file_name] = {}

        with open(file_name) as file_anno:
            # PeakID field has extra 'junk' so extra processing is needed
            fields = file_anno.readline().split('\t')
            fields[0] = 'PeakID'
            
            reader = csv.DictReader(file_anno, fieldnames=fields, delimiter='\t')
            for row in reader:
                # Get value of PeakID and remove it from values
                key = row.pop('PeakID')
                # PeakID : { Other Values }
                anno_dict[file_name][key] = row

# search_results is a nested dict
# First key is the search word to find
# Second key is the file name
# Values is the number of hits
search_results = {'non-coding':{},
                  'intergenic':{},
                  'intron':{},
                  'exon':{},
                  'promoter-TSS':{},
                  'TTS':{},
                  '5’ UTR':{},
                  '3’ UTR':{}}

for search_word in search_results.keys():
    for file_name, peak_ids in anno_dict.items():
        pattern = re.compile(search_word)
        hits = 0

        for fields in peak_ids.values():
            # Combine all values so it is a 'row'
            fields_str = ' '.join(fields.values())

            if pattern.search(fields_str) is not None:
                hits += 1

        search_results[search_word][file_name] = hits

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(search_results)
