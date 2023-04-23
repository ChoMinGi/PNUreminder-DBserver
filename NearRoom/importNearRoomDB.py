import pandas
import os

from amazon_rds.rds_connection import connect_rds_pymysql

def importNearRoom():

    dir_name = './2301table'

    file_list = os.listdir(dir_name)
    print(file_list)
    for file_name in file_list:
        connection = connect_rds_pymysql()
        readData = pandas.read_excel(dir_name + "/" + file_name)
        db_name = file_name.rstrip(".xlsx")
        print(f" >>{db_name}<< Auto Build COMPLETE")
    # start, runtime, building, room
        try:
            with connection.cursor() as cursor:
                # Create a new record
                dbNearRoom = f"INSERT INTO {db_name} (`building_num`,`room_num`,`start_time`, `run_time`) VALUES (%s, %s, %s, %s)"

                for i in readData.index:
                    cursor.execute(dbNearRoom, (readData['building'][i], readData['room'][i],readData['start'][i], readData['runtime'][i]))

            connection.commit()

        finally:
            connection.close()

