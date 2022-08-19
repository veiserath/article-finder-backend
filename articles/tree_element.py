import json
from dataclasses import dataclass


@dataclass
class TreeElement:
    name: str
    url: str
    citation_count: str
    children: list

    def __init__(self, name, url, citation_count, children):
        self.name = name
        self.url = url
        self.citation_count = citation_count
        self.children = children

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)