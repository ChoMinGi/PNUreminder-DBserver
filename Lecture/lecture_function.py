import pandas
import os

from sqlalchemy.orm import relationship

from aws.rds_connection import connect_rds_pymysql
from aws.rds_connection import create_rds_session

from sqlalchemy.ext.declarative import declarative_base

from NearRoom.parse_time import parse_start
from NearRoom.parse_time import parse_runtime


def read_excel():
    dir_name = './2301table/listLecture1/lecture'
    file_list = os.listdir(dir_name)
    if len(file_list)==1:
        file_name = file_list[0]
    read_data = pandas.read_excel(dir_name + "/" + file_name)

    return read_data

def main(Lecture):

    lecture_lists = read_excel().values

    session = create_rds_session()

    print(lecture_lists)

    for lecture_list in lecture_lists:

        new_lecture = Lecture(
            start_time= parse_start(lecture_list[0]),
            run_time= parse_runtime(lecture_list[1]),
            day_of_week=lecture_list[2]
        )

        # 객체를 세션에 추가하고 변경사항 커밋
        session.add(new_lecture)

    session.commit()


