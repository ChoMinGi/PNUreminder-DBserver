import pandas
import os
import datetime

dir_name = './2301table'

now = datetime

file_list = os.listdir(dir_name)
print(file_list)
for name in file_list:
    readData = pandas.read_excel(dir_name+"/"+name)
# start, runtime, building, room
for i in readData.index:
    print(i, readData['start'][i], readData['runtime'][i], readData['building'][i], readData['room'][i])
    
def timeInfo(n,s,r):

