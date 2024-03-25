#!/usr/bin/env python3
"""
Provides some stats about Nginx logs
"""
from pymongo import MongoClient


if __name__ == '__main__':
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client['logs']
    collection = db['nginx']

    no_docs = collection.count_documents({})
    print(f"{no_docs} logs")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    print("Methods:")
    for method in methods:
        count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    docs_get = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{docs_get} status check")
