# 필요한 패키지들
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 데이터베이스 연결 및 세션 생성
DATABASE_URL = "mysql+pymysql://username:password@host/db_name"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# 데이터베이스에 저장된 가장 최근 게시글의 제목을 가져오는 함수
def get_latest_title_from_db(session):
    result = session.query(Announcement).order_by(Announcement.id.desc()).first()
    if result:
        return result.title
    else:
        return None

# 웹 사이트에서 가장 최근 게시글의 제목을 가져오는 함수
def get_latest_title_from_web(driver):
    # 웹 사이트로부터 가장 최근 게시글의 제목을 크롤링하는 코드 작성
    pass

# 가장 오래된 게시글을 데이터베이스에서 삭제하는 함수
def delete_oldest_announcement(session):
    oldest_announcement = session.query(Announcement).order_by(Announcement.id).first()
    if oldest_announcement:
        session.delete(oldest_announcement)
        session.commit()

# 메인 코드
latest_title_from_db = get_latest_title_from_db(session)
latest_title_from_web = get_latest_title_from_web(driver)

if latest_title_from_db != latest_title_from_web:
    # 크롤링 진행 및 새로운 게시글을 데이터베이스에 추가하는 코드 작성
    pass

    # 가장 오래된 게시글을 데이터베이스에서 삭제
    delete_oldest_announcement(session)
