import os

from pymongo import MongoClient

ARCUSD_DB_MONGO_URL = os.environ['ARCUSD_DB_MONGO_URL']

client = MongoClient(ARCUSD_DB_MONGO_URL)

arcusd = client.arcusd


def save_task_info(task_info: dict):
    arcusd.tasks.insert_one(task_info)


def update_task_info(query: dict, values: dict):
    arcusd.tasks.find_one_and_update(query, {'$set': values})


def get_task_info(query):
    return arcusd.tasks.find_one(query)
