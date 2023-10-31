import os
import json
from multiprocessing import Lock

class JsonKeyValueStore:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = {}
        self.lock = Lock()
        self.load()

    def load(self):
        with self.lock:
            if os.path.exists(self.filepath):
                with open(self.filepath, 'r') as f:
                    try:
                        self.data = json.load(f)
                    except json.JSONDecodeError:
                        self.data = {}
            else:
                self.data = {}

    def save(self):
        with self.lock:
            with open(self.filepath, 'w') as f:
                json.dump(self.data, f)

    def get(self, key):
        with self.lock:
            return self.data.get(key)

    def set(self, key, value):
        with self.lock:
            self.data[key] = value


    def delete(self, key):
        with self.lock:
            if key in self.data:
                del self.data[key]
