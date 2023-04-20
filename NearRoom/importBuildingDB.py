import pandas
import os


from AmazonRDSManage.connectRDS import connectRDS

def import_building():
    dir_name = './2301table/listBuilding'

    file_list = os.listdir(dir_name)
    print(file_list)
    for file_name in file_list:
        connection = connectRDS()
        read_data = pandas.read_excel(dir_name + "/" + file_name)
        db_name = file_name.rstrip(".xlsx")
        print(f" >>{db_name}<< Auto Build COMPLETE")
        # start, runtime, building, room
        try:
            with connection.cursor() as cursor:
                # Create a new record
                db_building = f"INSERT INTO building_loaction (`building_num`,`building_name`,`building_lat`, `building_lng`) VALUES (%s, %s, %s, %s)"

                for i in read_data.index:
                    cursor.execute(db_building, (read_data['building_num'][i], read_data['building_name'][i],read_data['building_lat'][i], read_data['building_lng'][i]))

            connection.commit()

        finally:
            connection.close()

