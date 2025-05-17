import csv
import json

def csv_to_json(csv_file_path, json_file_path):
    with open(csv_file_path, mode='r') as csv_file:
        reader = csv.DictReader(csv_file)
        data = list(reader)
    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)
    
    return data

# Example usage:
if __name__ == "__main__":
    # Example usage of the csv_to_json function
    file_path = r'..\files\HackOxxo.csv'
    csv_to_json(file_path, 'output.json')