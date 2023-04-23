import pandas
import os


from amazon_rds.rds_connection import connect_rds_pymysql
from amazon_rds.rds_connection import create_rds_session

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


def read_excel():
    dir_name = './2301table/listBuilding'
    file_list = os.listdir(dir_name)
    if len(file_list)==1:
        file_name = file_list[0]
    read_data = pandas.read_excel(dir_name + "/" + file_name)

    return read_data

def main(Building):

    building_lists = read_excel().values
    Base = declarative_base()

    session = create_rds_session()

    print(building_lists)

    for building_list in building_lists:
        print(building_list)
        new_building_list = Building(
            building_num=building_list[0],
            building_name=building_list[1],
            building_lat=building_list[2],
            building_lng=building_list[3]
        )


        # 객체를 세션에 추가하고 변경사항 커밋
        session.merge(new_building_list)

    session.commit()



def import_building(read_data):
    connection = connect_rds_pymysql()
    db_name = "building_location"
    # start, runtime, building, room
    try:
        with connection.cursor() as cursor:
            # Create a new record
            db_building = f"INSERT INTO {db_name} (`building_num`,`building_name`,`building_lat`, `building_lng`) VALUES (%s, %s, %s, %s)"

            for i in read_data.index:
                cursor.execute(db_building, (read_data['building_num'][i], read_data['building_name'][i],read_data['building_lat'][i], read_data['building_lng'][i]))

        connection.commit()
        print(f" >>{db_name}<< Auto Build COMPLETE")
    finally:
        connection.close()



