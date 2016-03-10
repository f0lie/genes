import csv
import os
import re
import pprint

def get_genes(file_extension='.anno', dir='.'):
    # gene_dict is a nested dict
    # First key is the filename
    # Second key is the PeakID
    # Values is the rest of the fields
    gene_dict = {}

    for file_name in os.listdir(dir):
        if file_name.endswith(file_extension):
            gene_dict[file_name] = {}

            with open(file_name) as file_anno:
                # PeakID field has extra 'junk' so extra processing is needed
                fields = file_anno.readline().split('\t')
                fields[0] = 'PeakID'
                
                reader = csv.DictReader(file_anno, fieldnames=fields, delimiter='\t')
                for row in reader:
                    # Get value of PeakID and remove it from values
                    key = row.pop('PeakID')
                    # PeakID : { Other Values }
                    gene_dict[file_name][key] = row

    return gene_dict

def search_word(search_words, gene_dict):
    # search_results is a nested dict
    # First key is the search word to find
    # Second key is the file name
    # Values is the number of hits
    search_results = {}

    for search_word in search_words:
        search_results[search_word] = {}

        for file_name, peak_ids in gene_dict.items():
            pattern = re.compile(search_word)
            hits = 0

            for fields in peak_ids.values():
                # Combine all values so it is a 'row'
                fields_str = ' '.join(fields.values())

                if pattern.search(fields_str) is not None:
                    hits += 1

            search_results[search_word][file_name] = hits

    return search_results

def search_field(gene_dict, field, value):
    # values_found is a dict of lists which contain the found value
    # First key is the filename
    # Lists is the found row with the matching value
    values_found = {}

    for file_name, peak_ids in gene_dict.items():
        values_found[file_name] = []
        for peak_id, fields in peak_ids.items():
            if value == fields[field]:
                values_found[file_name].append(peak_ids[peak_id])

    return values_found


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    gene_dict = get_genes()

    search_results = search_word(['non-coding',
                             'intergenic',
                             'intron',
                             'exon',
                             'promoter-TSS',
                             'TTS',
                             '5’ UTR',
                             '3’ UTR'],
                              gene_dict)

    search_gene_results = search_field(gene_dict, 'Gene Name', 'TPI1P3')
    
    pp.pprint(search_results)
    pp.pprint(search_gene_results)