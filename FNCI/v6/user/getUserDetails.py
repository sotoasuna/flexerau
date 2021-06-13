'''
Created on Nov 25, 2019

@author: SGeary
'''

import logging
import requests
import json

import config


ENDPOINT_URL = config.v6_BASEURL + "user/getUserDetails"


logger = logging.getLogger(__name__)

#-------------------------------------------------------------------------------------------#

def get_user_id_by_login(login, authToken):
    logger.debug("Entering get_user_id_by_login with login %s" %login)
    
    
    headers = {'Content-Type': 'application/json', 'Authorization':  authToken}  
    RESTAPI_URL = ENDPOINT_URL + "?userLogin=" + login 
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
        # Assume there is a single value since we are searching by login
        logger.debug(response.json()["Content"][0]["id"])
        return(response.json()["Content"][0]["id"])
        
    elif response.status_code == 404:
        print("User with login of %s was not found" %login)
    
    elif response.status_code == 500:
        print("Internal Server Error")
