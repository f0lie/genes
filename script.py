import csv

result = {}
with open('test') as file:
    fields = file.readline().split('\t')
    fields[0] = 'PeakID'
    
    reader = csv.DictReader(file, fieldnames=fields, delimiter='\t')
    for row in reader:
        key = row.pop('PeakID')
        result[key] = row

print(result)
    