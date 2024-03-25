#!/usr/bin/env python3
"""
a module that lists all document in a collection
"""


def list_all(mongo_collection):
    """ lists all documents in a collection """
    return [doc for doc in mongo_collection.find()]
