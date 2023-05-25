from pymongo import MongoClient
from aws.db_info import mongo_db


def mongoDB_connection():
    client = MongoClient(f'mongodb://{mongo_db.USER_NAME}:{mongo_db.PASSWORD}@{mongo_db.HOST}:27017/')
    return client


mongoDB_connection()