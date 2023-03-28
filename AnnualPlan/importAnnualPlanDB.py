from AmazonRDSManage.connectRDS import connectRDS

def importAnnualPlan(annualLists):

    connection = connectRDS()

    with connection:
        with connection.cursor() as cursor:
            for annualList in annualLists:
                dbAnnualPlan = "INSERT INTO `annualplan` (`date`, `context`, `state`) VALUES (%s, %s, %s)"
                cursor.execute(dbAnnualPlan, (annualList[0], annualList[1], annualList[2]))

        connection.commit()
    return