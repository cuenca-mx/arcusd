import os

from pymongo import MongoClient

ARCUSD_DB_MONGO_URL = os.environ['ARCUSD_DB_MONGO_URL']

client = MongoClient(ARCUSD_DB_MONGO_URL)

db = client.get_database()


def save_task_info(task_info: dict):
    db.tasks.insert_one(task_info)


def update_task_info(query: dict, values: dict):
    db.tasks.find_one_and_update(query, {'$set': values})


def get_task_info(query):
    return db.tasks.find_one(query)
