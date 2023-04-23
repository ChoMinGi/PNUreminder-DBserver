import pandas
import os

from sqlalchemy.orm import relationship

from amazon_rds.rds_connection import connect_rds_pymysql
from amazon_rds.rds_connection import create_rds_session

from sqlalchemy.ext.declarative import declarative_base

from NearRoom.parse_time import parse_start
from NearRoom.parse_time import parse_runtime


def read_excel():
    dir_name = './2301table/listLecture2'
    file_list = os.listdir(dir_name)
    if len(file_list)==1:
        file_name = file_list[0]
    read_data = pandas.read_excel(dir_name + "/" + file_name)

    return read_data

def main(LectureRoom,Lecture):

    lecture_lists = read_excel().values
    session = create_rds_session()

    print(lecture_lists)

    for lecture_list in lecture_lists:
        # 강의실 정보를 찾거나 생성합니다.
        lecture_room = session.query(LectureRoom).filter_by(
            building_num=lecture_list[2], room_num=lecture_list[3]
        ).first()

        if lecture_room is None:
            lecture_room = LectureRoom(
                building_num=lecture_list[2], room_num=lecture_list[3]
            )
            session.add(lecture_room)
            session.flush()  # 이를 통해 데이터베이스에 LectureRoom 객체가 추가되고 id를 얻을 수 있습니다.

        new_lecture = Lecture(
            start_time=parse_start(lecture_list[0]),
            run_time=parse_runtime(lecture_list[1]),
            day_of_week=lecture_list[4],
            lecture_room_id=lecture_room.id  # 여기에 lecture_room_id를 설정합니다.
        )

        # 객체를 세션에 추가하고 변경사항 커밋
        session.add(new_lecture)

    session.commit()
def importNearRoomOne(read_data):

    connection = connect_rds_pymysql()
    db_name = "listLecture"

    # start, runtime, building, room
    try:
        with connection.cursor() as cursor:
            # Create a new record
            dbNearRoom = f"INSERT INTO {db_name} (`building_num`,`room_num`,`start_time`, `run_time`,`day_of_week`) VALUES (%s, %s, %s, %s, %s)"

        for i in read_data.index:
            td_start= parse_start(read_data['start'][i])
            td_runtime= parse_runtime(read_data['runtime'][i])

            cursor.execute(dbNearRoom, (read_data['building'][i], read_data['room'][i],td_start,td_runtime , read_data['day_of_week'][i]))

        connection.commit()
    finally:
        connection.close()

    print(f" >>{db_name}<< Auto Build COMPLETE")

