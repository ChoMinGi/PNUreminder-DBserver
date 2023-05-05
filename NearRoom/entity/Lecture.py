from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'mysql+mysqlconnector://username:password@localhost/db_name'

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class LectureRoom(Base):
    __tablename__ = 'lecture_rooms'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    building_number = Column(Integer)

class Lecture(Base):
    __tablename__ = 'lectures'
    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime)
    duration = Column(Integer)
    lecture_room_id = Column(Integer, ForeignKey('lecture_rooms.id'))
    lecture_room = relationship("LectureRoom")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
