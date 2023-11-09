import json
from pprint import pprint


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

    def add_record(self, id, word, artikel, ende, translate):
        self.content[id] = {'word': word, 'artikel': artikel, 'ende': ende, 'transtale': translate}

    def show(self):
        pprint(self.content, indent=4)


json_database = JSONFile('test.json')
json_database.add_record(1, 'cat', 'murzik')
json_database.add_record(2, 'dog', 'patron')
json_database.write_content()
json_database.read_content()
json_database.show()