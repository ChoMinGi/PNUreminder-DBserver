#RDSmysql
import pymysql
import pymysql.cursors

#RDS imformation
from AmazonRDSManage.dbinfo import dbsecurity

def connectRDS():
    try:
        # RDS information
        ihost = dbsecurity.host
        iusername = dbsecurity.username
        ipassword = dbsecurity.password
        idatabase = dbsecurity.database

        connection = pymysql.connect(host=str(ihost),
                                     user=str(iusername),
                                     password=str(ipassword),
                                     database=str(idatabase),
                                     use_unicode=True,
                                     cursorclass=pymysql.cursors.DictCursor)
    except:
        print("RDS connection Error")
        exit(1)
    return connection
