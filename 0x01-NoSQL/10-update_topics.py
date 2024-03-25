#!/usr/bin/env python3
"""
module that changes all topics of school document
"""


def update_topics(mongo_collection, name, topics):
    """ a function that updates of a document of a collection """

    mongo_collection.update_many(
            {"name": name},
            {"$set": {"topics": topics}}
    )
