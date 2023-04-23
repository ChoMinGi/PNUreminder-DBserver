from amazon_rds.rds_connection import create_rds_session
from amazon_rds.rds_connection import connect_rds_pymysql

from sqlalchemy import  Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



def annual_plan(annual_lists):
    Base = declarative_base()

    class AnnualPlan(Base):
        __tablename__ = 'annualplan'

        id = Column(Integer, primary_key=True)
        date = Column(String)
        context = Column(String)
        state = Column(Integer)

    session = create_rds_session()

    for annual_list in annual_lists:
        new_plan = AnnualPlan(
            date=annual_list[0],
            context=annual_list[1],
            state=annual_list[2]
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