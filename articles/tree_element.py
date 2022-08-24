import json
from dataclasses import dataclass


@dataclass
class TreeElement:
    name: str
    url: str
    attributes = dict
    children: list

    def __init__(self, name, url, date, publisher, citation_count, references_count, children):
        self.name = name
        self.url = url
        self.attributes = {'date': str(date), 'publisher': publisher, 'citations': citation_count, 'references': references_count}
        self.children = children

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          indent=4)