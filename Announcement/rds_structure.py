from aws.rds_connection import create_rds_session_for_announcement

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

def save_culedu_announce_to_rds(datas, tablename):
    Base = declarative_base()

    class CuleduAnnounce(Base):
        __tablename__ = str(tablename)

        id = Column(Integer, primary_key=True, autoincrement=True)
        title = Column(String)
        urls = Column(String)
        date = Column(String)
        keyword = Column(String)

    session = create_rds_session_for_announcement()
    # Create RDS session

    for data in datas:
        new_announce = CuleduAnnounce(
            title=data['title'],
            urls=data['urls'],
            date=data['date'],
            keyword=data['keyword']
        )
        session.add(new_announce)

    session.commit()

    # 세션 종료
    session.close()
