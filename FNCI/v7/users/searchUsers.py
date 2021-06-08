'''
Created on Nov 13, 2019

@author: SGeary
'''
import logging
import json
import requests


import config


ENDPOINT_URL = config.BASEURL + "users/search"


logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------#
def get_user_email_by_id(userID, authToken):
    logger.debug("Entering get_user_email_by_id with userID %s" %userID)
    
    
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken}  
    RESTAPI_URL = ENDPOINT_URL + "?id=" + str(userID) 
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)  
       
    try:
        response = requests.get(RESTAPI_URL, headers=headers)
        logger.debug(json.dumps(response.json(), indent=3))  
        
    except requests.exceptions.RequestException as e:
        print(e)
        logger.debug(e)
        logger.debug(response)
        logger.debug(response.text)
        return False
    
    # Check the response code and proceed accordingly
    if response.status_code == 200:
        logger.debug(response.json()["data"]["email"])
        return(response.json()["data"]["email"])
        
    elif response.status_code == 404:
        print("User with id of %s was not found" %userID)
    
    elif response.status_code == 500:
        print("Internal Server Error")

#-----------------------------------------------------------------------#
def get_user_email_by_login(login, authToken):
    logger.debug("Entering get_user_email_by_login with login %s" %login)
    
    
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken}  
    RESTAPI_URL = ENDPOINT_URL + "?login=" + login 
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)  
       
    try:
        response = requests.get(RESTAPI_URL, headers=headers)
        logger.debug(json.dumps(response.json(), indent=3))  
        
    except requests.exceptions.RequestException as e:
        print(e)
        logger.debug(e)
        logger.debug(response)
        logger.debug(response.text)
        return False
    
    # Check the response code and proceed accordingly
    if response.status_code == 200:
        logger.debug(response.json()["data"]["email"])
        return(response.json()["data"]["email"])
        
    elif response.status_code == 404:
        print("User with login of %s was not found" %login)
    
    elif response.status_code == 500:
        print("Internal Server Error")

