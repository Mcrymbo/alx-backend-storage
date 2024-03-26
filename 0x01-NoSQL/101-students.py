#!/usr/bin/env python3
"""
returns all students sorted by average score
"""


def top_students(mongo_collection):
    """ function that returns all students sorted by av score """
    sorted_list = mongo_collection.aggregate([
         {
            "$project": {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {"$sort": {"averageScore": -1}}
    ])
    return sorted_list
