'''
Created on Nov 19, 2019

@author: SGeary
'''
import logging
import requests

import config

ENDPOINT_URL = config.v6_BASEURL + "project/userLogin/"

logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------#
def get_user_login_by_email(emailAddress, authToken):
    logger.debug("Enteringget_user_login_by_emailchange_project_owner")
   
             
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken}  
    RESTAPI_URL = ENDPOINT_URL + emailAddress
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)  
       
    try:
        response = requests.get(RESTAPI_URL, headers=headers)
        
    except requests.exceptions.RequestException as e:
        print(e)
        logger.debug(e)
        logger.debug(response)
        logger.debug(response.text)
        return False
    
    # Check the response code and proceed accordingly
    if response.status_code == 200:
        logger.debug("Project owner changed")

        userLogin = (response.json()["Content"])
        logger.debug("     User login for %s is %s" %(emailAddress, userLogin))
        return userLogin



    elif response.status_code == 401:
        print("Unauthorized")        
    
    elif response.status_code == 404:
        print("Bad Request")
    
    elif response.status_code == 500:
        print("Internal Server Error")