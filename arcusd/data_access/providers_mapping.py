import os

from pymongo import MongoClient

from arcusd.exc import UnknownServiceProvider

ARCUSD_DB_MONGO_URL = os.environ['ARCUSD_DB_MONGO_URL']

client = MongoClient(ARCUSD_DB_MONGO_URL)

db = client.get_database()


def get_biller_id(service_provider_code: str) -> int:
    mapping = db.providers_mapping.find_one(
        dict(service_provider_code=service_provider_code)
    )
    if not mapping:
        raise UnknownServiceProvider(service_provider_code)
    return mapping['biller_id']


def get_service_provider_code(biller_id: int) -> str:
    mapping = db.providers_mapping.find_one(dict(biller_id=biller_id))
    if not mapping:
        raise UnknownServiceProvider(str(biller_id))
    return mapping['service_provider_code']


def add_mapping(service_provider_code: str, biller_id: int) -> None:
    db.providers_mapping.insert_one(
        dict(service_provider_code=service_provider_code, biller_id=biller_id)
    )
