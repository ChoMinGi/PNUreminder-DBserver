from aws.rds_connection import create_rds_session
from aws.rds_connection import connect_rds_pymysql

from datetime import datetime
from sqlalchemy import  Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



def annual_plan(annual_lists):
    Base = declarative_base()

    class AnnualPlan(Base):
        __tablename__ = 'annualplan'

        id = Column(Integer, primary_key=True)
        start_date = Column(DateTime)
        end_date = Column(DateTime)
        context = Column(String)
        state = Column(Integer)

    def convert_str_to_datetime(date_str):
        return datetime.strptime(date_str, '%Y.%m.%d')

    session = create_rds_session()

    for annual_list in annual_lists:
        new_plan = AnnualPlan(
            start_date=convert_str_to_datetime(annual_list[0]),
            end_date=convert_str_to_datetime(annual_list[1]),
            context=annual_list[2],
            state=annual_list[3]
        )
        # 객체를 세션에 추가하고 변경사항 커밋
        session.add(new_plan)

    session.commit()

    # 세션 종료
    session.close()



def importAnnualPlan(annualLists):

    connection = connect_rds_pymysql()

    with connection:
        with connection.cursor() as cursor:
            for annualList in annualLists:
                dbAnnualPlan = "INSERT INTO `annualplan` (`date`, `context`, `state`) VALUES (%s, %s, %s)"
                cursor.execute(dbAnnualPlan, (annualList[0], annualList[1], annualList[2]))

        connection.commit()
    return