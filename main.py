import pandas
import os

# Selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


from AnnualPlan.mainCrawlAnnual import crawlAnnualplan
from AnnualPlan.annual_plan import annual_plan

from BuildingLocation import building_location

from Lecture import lecture_function
from LectureRoom import lecture_room_function
from NearRoom import lecture_room_num


from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Time, DECIMAL, PrimaryKeyConstraint, \
    ForeignKeyConstraint

from amazon_rds.rds_connection import create_rds_session


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)



def crawlDropdown():
    # 웹 페이지 접속
    driver.get('https://onestop.pusan.ac.kr/page?menuCD=000000000000368')
    driver.implicitly_wait(3)
    dropdown = Select(driver.find_elements(By.XPATH,'//*[@id="SCH_BLD_CD"]'))
    items=dropdown.select_by_index(1)
    return items

def checkFirstElement():
    # db 앞 원소 비교후 바뀐 내용이 없으면 후처리 작동제한
    return

def main():
    Base = declarative_base()

    class Building(Base):
        __tablename__ = 'building_location'

        building_num = Column(Integer, primary_key=True)
        building_name = Column(String(40), nullable=False)
        building_lat = Column(DECIMAL(20, 15), nullable=False)
        building_lng = Column(DECIMAL(20, 15), nullable=False)


    class LectureRoom(Base):
        __tablename__ = 'lecture_room'

        id = Column(Integer, primary_key= True,autoincrement=True)
        room_num = Column(String(40), nullable=False)
        building_num = Column(Integer, ForeignKey('building_location.building_num'))


    class Lecture(Base):
        __tablename__ = 'lecture'

        id = Column(Integer, primary_key=True, autoincrement=True)
        start_time = Column(Time, nullable=False)
        run_time = Column(Time, nullable=False)
        day_of_week = Column(Integer, nullable=False)
        lecture_room_id = Column(Integer, ForeignKey('lecture_room.id'))




    Building.lecture_rooms = relationship("LectureRoom", back_populates="building")
    LectureRoom.building = relationship("Building", back_populates="lecture_rooms")

    LectureRoom.lectures = relationship("Lecture", back_populates="lecture_room")
    Lecture.lecture_room = relationship("LectureRoom", back_populates="lectures")


    engine = create_rds_session(1)
    Base.metadata.create_all(engine)


    # For Building annualPlan
    #     annualLists=crawlAnnualplan(driver)
    #     annual_plan(annualLists)

    building_location.main(Building)
    # lecture_function.main(Lecture)
    # lecture_room_function.main(LectureRoom)

    lecture_room_num.main(LectureRoom,Lecture)




    return

main()
