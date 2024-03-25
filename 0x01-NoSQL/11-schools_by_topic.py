#!/usr/bin/env python3
"""
module that list schols having a specific topic
"""


def schools_by_topic(mongo_collection, topic):
    """ function that returns list of school """
    return mongo_collection.find({'topics': topic})
