import pandas
import os

from amazon_rds.rds_connection import create_rds_session


def read_excel():
    dir_name = './2301table/listLecture1/room'
    file_list = os.listdir(dir_name)
    if len(file_list)==1:
        file_name = file_list[0]
    read_data = pandas.read_excel(dir_name + "/" + file_name)

    return read_data

def main(LectureRoom):

    lecture_lists = read_excel().values

    session = create_rds_session()

    print(lecture_lists)

    for lecture_list in lecture_lists:
        print(lecture_list)
        # `building_num`, `room_num`
        new_lecture_room = LectureRoom(
            building_num=lecture_list[0],
            room_num=lecture_list[1]
        )



        # 객체를 세션에 추가하고 변경사항 커밋
        session.add(new_lecture_room)

    session.commit()