import csv
import json
import re

def ParseCSV(csv_file):    
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    
    data = clean_data(data)

    with open('./data/parsed.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def clean_data(data):
    cleaned_data = []
    for record in data:
        cleaned_record = {re.sub(r'[^\x00-\x7F]+', '', key): value for key, value in record.items()}
        cleaned_data.append(cleaned_record)
    return cleaned_data

