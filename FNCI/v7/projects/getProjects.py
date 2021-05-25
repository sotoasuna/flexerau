'''
Created on Nov 13, 2019

@author: SGeary
'''
import logging
import requests

import config


logger = logging.getLogger(__name__)

ENDPOINT_URL = config.BASEURL + "projects"

#--------------------------------------------------------------------#
def get_project_list(authToken):
    logger.debug("Entering get_project_list")

    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken}  
    RESTAPI_URL = ENDPOINT_URL
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
        logger.debug(response.json()["data"])
        return(response.json()["data"])


    elif response.status_code == 401:
        print("Unauthorized")        
    
    elif response.status_code == 404:
        print("Bad Request")
    
    elif response.status_code == 500:
        print("Internal Server Error")
        