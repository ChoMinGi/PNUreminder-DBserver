import pandas
import os

from AmazonRDSManage.connectRDS import connectRDS
from NearRoom.parse_time import parse_start
from NearRoom.parse_time import parse_runtime

def importNearRoomOne():

    dir_name = './2301table/listLecture1'

    file_list = os.listdir(dir_name)
    print(file_list)
    for file_name in file_list:
        connection = connectRDS()
        readData = pandas.read_excel(dir_name + "/" + file_name)
        db_name = file_name.rstrip(".xlsx")
        # start, runtime, building, room
        try:
            with connection.cursor() as cursor:
                # Create a new record
                dbNearRoom = f"INSERT INTO {db_name} (`building_num`,`room_num`,`start_time`, `run_time`,`day_of_week`) VALUES (%s, %s, %s, %s, %s)"

                for i in readData.index:
                    td_start= parse_start(readData['start'][i])
                    td_runtime= parse_runtime(readData['runtime'][i])

                    cursor.execute(dbNearRoom, (readData['building'][i], readData['room'][i],td_start,td_runtime , readData['day_of_week'][i]))

            connection.commit()
        finally:
            connection.close()

        print(f" >>{db_name}<< Auto Build COMPLETE")

