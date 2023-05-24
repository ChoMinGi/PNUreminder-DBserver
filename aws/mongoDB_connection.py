from pymongo import MongoClient
from aws.db_info import mongo_db


def mongoDB_connection():
    client = MongoClient(f'mongodb://{mongo_db.USER_NAME}:{mongo_db.PASSWORD}@{mongo_db.HOST}:27017/')
    db = client['test_db']

    # 'test_collection'라는 이름의 컬렉션을 선택합니다. 이 컬렉션도 존재하지 않으면 새로 생성됩니다.
    collection = db['test_collection']

    # 컬렉션에 삽입할 간단한 데이터를 만듭니다.
    data = {'name': '민준쓰', 'age': 25, 'job': 'no-job'}

    # 데이터를 컬렉션에 삽입합니다.
    insert_result = collection.insert_one(data)
    print(f'Inserted data with id {insert_result.inserted_id}')

    # 컬렉션에서 이름이 'John'인 데이터를 검색합니다.
    query = {'name': 'John'}
    query_result = collection.find_one(query)
    print(query_result)
    return


mongoDB_connection()