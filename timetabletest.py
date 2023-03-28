import pandas
import os

def importNearRoomDB():
    dir_name = './2301table'

    file_list = os.listdir(dir_name)
    print(file_list)
    for name in file_list:
        readData = pandas.read_excel(dir_name+"/"+name)
    # start, runtime, building, room
    for i in readData.index:
        print(i, readData['start'][i], readData['runtime'][i], readData['building'][i], readData['room'][i])


# s= str("15")
# dt_classStart= datetime.strptime(s,"%H")
# now = datetime.strptime(now,"%H%M")
# print(dt_classStart,now)
# diff=dt_classStart-now
# print(diff)
# def checkEmpty(now, s, e):
#     print(now,s,e)
#     return