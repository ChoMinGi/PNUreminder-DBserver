from amazon_rds.rds_connection import create_rds_session_for_announcement

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

def save_culedu_announce_to_rds(announcements):
    Base = declarative_base()

    class CuleduAnnounce(Base):
        __tablename__ = 'culedu_announce'

        id = Column(Integer, primary_key=True, autoincrement=True)
        title = Column(String)
        urls = Column(String)

    session = create_rds_session_for_announcement()
    # Create RDS session

    for announce in announcements:
        new_announce = CuleduAnnounce(
            title=announce['title'],
            urls=announce['urls']
        )
        session.add(new_announce)

    session.commit()

    # 세션 종료
    session.close()
