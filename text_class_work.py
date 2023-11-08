import csv
import json
from pprint import pprint


class CSVFile:
    fieldnames = ['id', 'animal_type', 'name']

    def __init__(self, filename):
        self.filename = filename
        self.content = {}

    def read_content(self):
        with open(self.filename, 'r') as f:
            reader = csv.DictReader(f)
            for line in reader:
                record_id = int(line.pop('id'))
                self.content[record_id] = line

    def write_content(self):
        with open(self.filename, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()
            for idx, record in self.content.items():
                writer.writerow({'id': idx, **record})

    def add_record(self, id, animal_type, name):
        self.content[id] = {'animal_type': animal_type, 'name': name}

    def show(self):
        pprint(self.content, indent=4)


csv_database = CSVFile('test.csv')
csv_database.add_record(1, 'cat', 'murzik')
csv_database.add_record(2, 'dog', 'patron')
csv_database.write_content()
csv_database.read_content()
csv_database.show()


class JSONFile:
    def __init__(self, filename):
        self.filename = filename
        self.content = {}

    def read_content(self):
        with open(self.filename) as f:
            content = json.load(f)
            for record_id, record in content.items():
                record_id = int(record_id)
                self.content[record_id] = record


    def write_content(self):
        with open(self.filename, 'w') as f:
            json.dump(self.content, f, indent=4)

    def add_record(self, id, animal_type, name):
        self.content[id] = {'animal_type': animal_type, 'name': name}

    def show(self):
        pprint(self.content, indent=4)

json_database = JSONFile('test.json')
json_database.add_record(1, 'cat', 'murzik')
json_database.add_record(2, 'dog', 'patron')
json_database.write_content()
json_database.read_content()
json_database.show()