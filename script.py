import csv
import os
import re
import pprint
import collections

def get_genes(file_extension='.anno', dir='.'):
    # gene_dict is a nested dict
    # First key is the filename
    # Second key is the PeakID
    # Values is the rest of the fields
    gene_dict = collections.defaultdict(dict)

    for file_name in os.listdir(dir):
        if file_name.endswith(file_extension):
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
    # First key is the file name
    # Second key is the searched term
    # Values is the number of hits
    search_results = collections.defaultdict(dict)

    for search_word in search_words:
        for file_name, peak_ids in gene_dict.items():
            search_results[file_name][search_word] = 0

            for fields in peak_ids.values():
                # Combine all values so it is a 'row'
                fields_str = ' '.join(fields.values())

                if re.search(search_word, fields_str) is not None:
                    search_results[file_name][search_word] += 1

    return search_results

def search_field(gene_dict, field, value):
    # values_found is a dict of lists which contain the found value
    # First key is the filename
    # Lists is the found row with the matching value
    values_found = collections.defaultdict(list)

    for file_name, peak_ids in gene_dict.items():
        for peak_id, fields in peak_ids.items():
            if value == fields[field]:
                values_found[file_name].append(peak_ids[peak_id])

    return values_found


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    gene_dict = get_genes()

    search_words = ['non-coding',
                    'intergenic',
                    'intron',
                     'exon',
                     'promoter-TSS',
                     'TTS',
                     '5’ UTR',
                     '3’ UTR']
    search_results = search_word(search_words, gene_dict)

    search_gene_results = search_field(gene_dict, 'Gene Name', 'TPI1P3')

    with open('search_results.txt', 'w') as out_file:
        writer = csv.DictWriter(out_file, delimiter='\t',
                                fieldnames=['filename'] + search_words)
        writer.writeheader()
        for filename, results in search_results.items():
            results['filename'] = filename
            writer.writerow(results)

    with open('search_gene_results.txt', 'w') as out_file:
        fields = list(list(search_gene_results.values())[0][0].keys())
        writer = csv.DictWriter(out_file, delimiter='\t',
                                fieldnames=['filename'] + fields)
        writer.writeheader()
        for filename, results in search_gene_results.items():
            for result in results:
                result['filename'] = filename
                writer.writerow(result)
