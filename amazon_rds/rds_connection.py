#RDSmysql
import pymysql
import pymysql.cursors

#RDS imformation
from amazon_rds.db_info import dbsecurity
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_rds_session(return_engine=None):

    host = dbsecurity.host
    port = 3306
    username = dbsecurity.username
    password = dbsecurity.password
    db_name = dbsecurity.database

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
