'''
Created on Sep 25, 2019

@author: SGeary
'''
import logging
import pymysql

import config


logger = logging.getLogger(__name__)


authToken = config.AUTHTOKEN
#------------------------------------------------------------------#

def get_v7_user_date_from_mysqldb():
    
    logger.debug("Entering get_v7_user_date_from_mysqldb with projectID")
    
    # Open database connection
    db = pymysql.connect(config.mySQLHOST, config.mySQLUSER, config.mySQLPASSWORD, config.mySQLDATABASE)
        # prepare a cursor object using cursor() method
    cursor = db.cursor()
    
    sqlQuery = "SELECT ID_, LOGIN_, FIRST_NAME_, LAST_NAME_, EMAIL_  FROM 2019r3_82.pas_user;"
    
    try:
        # Execute the SQL command
        cursor.execute(sqlQuery)
        # Fetch all the rows in a list of lists.
        RESULTS = cursor.fetchall()

    except pymysql.InternalError as error:
        print(error)
        return None
    
    # create the empty dic for the user data that will have the ID as the key
    FNCIUSERS = {}

    for user in RESULTS:
        userID = user[0]
        login = user[1]
        firstName = user[2]
        lastName = user[3]
        emailAddress = user[4]
        
        
        FNCIUSERS[user[0]] = [login, emailAddress, firstName, lastName]
            
    return FNCIUSERS