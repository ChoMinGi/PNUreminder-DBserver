import pandas
import os

from AmazonRDSManage.connectRDS import connectRDS


def importBuildingLoaction():
    dir_name = './2301table'
    file_name = 'listBuilding.xlsx'
    connection = connectRDS()
    readData = pandas.read_excel(dir_name + "/" + file_name)
    db_name = file_name.rstrip(".xlsx")
    print(f" >>{db_name}<< Auto Build COMPLETE")
    # start, runtime, building, room
    try:
        with connection.cursor() as cursor:
            # Create a new record
            dbBuildingLocation = f"INSERT INTO {db_name} (`building_num`,`building_name`,`building_Lat`, `building_Lng`) VALUES (%s, %s, %s, %s)"

            for i in readData.index:
                cursor.execute(dbBuildingLocation, (readData['building_num'][i], readData['building_name'][i], readData['building_Lat'][i], readData['building_Lng'][i]))

        connection.commit()

    finally:
        connection.close()