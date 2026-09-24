import json
import math
import string
import re
import random
import sys
import traceback
import functools
from collections import OrderedDict, defaultdict
from dataclasses import dataclass, replace
from datetime import datetime, timedelta

import numpy
import sortedcontainers


@dataclass
class File:
    size: str
    time: str
    ttl: int | None = None


class fileSystem:
    def __init__(self):
        # self.fileDict = defaultdict(dict)
        self.fileDict = {}

    def file_upload_at(self, timestamp, file_name, file_size, ttl):
        if file_name in self.fileDict:
            raise RuntimeError()
        else:
            # self.fileDict[file_name]["size"] = file_size
            # self.fileDict[file_name]["time"] = timestamp
            # self.fileDict[file_name]["ttl"] = ttl
            self.fileDict[file_name] = File(file_size, timestamp, ttl)


    def is_alive(self, file_name, timestamp):
        # ttl = self.fileDict[file_name]['ttl']
        file = self.fileDict[file_name]
        if file.ttl is None:
            return True
        # uploaded = datetime.fromisoformat(self.fileDict[file_name]['time'])
        uploaded = datetime.fromisoformat(file.time)
        expires = uploaded + timedelta(seconds=int(file.ttl))
        return uploaded <= datetime.fromisoformat(timestamp) < expires

    def file_get_at(self, timestamp, file_name):
        if file_name in self.fileDict and self.is_alive(file_name, timestamp):
            # return self.fileDict[file_name]['size']
            return self.fileDict[file_name].size
        else:
            return None


    def file_copy_at(self, timestamp, source, dest):
        if dest in self.fileDict:
            del self.fileDict[dest]
            # self.fileDict[dest] = self.fileDict[source]
            # self.fileDict[dest]['time'] = timestamp
            self.fileDict[dest] = replace(self.fileDict[source], time=timestamp)
        elif source not in self.fileDict:
            raise RuntimeError()
        else:
            # self.fileDict[dest] = self.fileDict[source]
            # self.fileDict[dest]["time"] = timestamp
            self.fileDict[dest] = replace(self.fileDict[source], time=timestamp)

    def file_search_at(self, timestamp, prefix):
        matches = [name for name in self.fileDict
                   if name.startswith(prefix) and self.is_alive(name, timestamp)]
        descending = sorted(matches,
                            # key = lambda name: self.fileDict[name]['size'],
                            key = lambda name: self.fileDict[name].size,
                            reverse=True)
        return descending[:10]

    def rollback(self, timestamp):
        for name in self.fileDict:
            # self.fileDict[name]['time'] = timestamp
            self.fileDict[name].time = timestamp



    

def simulate_coding_framework(list_of_lists):
    """
    Simulates a coding framework operation on a list of lists of strings.

    Parameters:
    list_of_lists (List[List[str]]): A list of lists containing strings.
    """
    fs = fileSystem()
    results = []

    for entry in list_of_lists:
        operation = entry[0]
        args = entry[1:]

        if operation == "FILE_UPLOAD":
            fs.file_upload(args[0], args[1])
            results.append(f"uploaded {args[0]}")

        elif operation == "FILE_GET":
            fs.file_get(args[0])
            results.append(f"got {args[0]}")

        elif operation == "FILE_COPY":
            fs.file_copy(args[0], args[1])
            results.append(f"copied {args[0]} to {args[1]}")

        elif operation == "FILE_SEARCH":
            found = fs.file_search(args[0])
            results.append(f"found [{', '.join(found)}]")

        elif operation == "FILE_UPLOAD_AT":
            ttl = args[3] if len(args) > 3 else None
            fs.file_upload_at(args[0], args[1], args[2], ttl)
            results.append(f"uploaded at {args[1]}")

        elif operation == "FILE_GET_AT":
            size = fs.file_get_at(args[0], args[1])
            if size is None:
                results.append("file not found")
            else:
                results.append(f"got at {args[1]}")

        elif operation == "FILE_COPY_AT":
            fs.file_copy_at(args[0], args[1], args[2])
            results.append(f"copied at {args[1]} to {args[2]}")

        elif operation == "FILE_SEARCH_AT":
            found = fs.file_search_at(args[0], args[1])
            results.append(f"found at [{', '.join(found)}]")

        elif operation == "ROLLBACK":
            fs.rollback(args[0])
            results.append(f"rollback to {args[0]}")

    return results
    


