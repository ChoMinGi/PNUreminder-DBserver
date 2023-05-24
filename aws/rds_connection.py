#RDSmysql
import pymysql
import pymysql.cursors

#RDS imformation
from aws.db_info import dbsecurity
from aws.db_info import dbsecurity_for_announcement

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_rds_session(return_engine=None):

    dbsecurity_instance = dbsecurity()
    host = dbsecurity_instance.host
    port = 3306
    username = dbsecurity_instance.username
    password = dbsecurity_instance.password
    db_name = dbsecurity_instance.database

    # RDS 연결 문자열 생성
    database_uri = f'mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}'

    # 엔진 생성 및 세션 설정
    engine = create_engine(database_uri)
    Session = sessionmaker(bind=engine)

    if return_engine is None:
        return Session()
    else:
        return engine


def create_rds_session_for_announcement(return_engine=None):

    dbsecurity_instance = dbsecurity_for_announcement()
    host = dbsecurity_instance.host
    port = 3306
    username = dbsecurity_instance.username
    password = dbsecurity_instance.password
    db_name = dbsecurity_instance.database

    # RDS 연결 문자열 생성
    database_uri = f'mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}'

    # 엔진 생성 및 세션 설정
    engine = create_engine(database_uri)
    Session = sessionmaker(bind=engine)

    if return_engine is None:
        return Session()
    else:
        return engine

def connect_rds_pymysql():
    try:
        # RDS information
        ihost = dbsecurity.host
        iusername = dbsecurity.username
        ipassword = dbsecurity.password
        idatabase = dbsecurity.database

        connection = pymysql.connect(host=str(ihost),
                                     user=str(iusername),
                                     password=str(ipassword),
                                     database=str(idatabase),
                                     use_unicode=True,
                                     cursorclass=pymysql.cursors.DictCursor)
    except:
        print("RDS connection Error")
        exit(1)
    return connection
