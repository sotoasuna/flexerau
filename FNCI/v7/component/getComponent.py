'''
Created on Oct 24, 2019

@author: SGeary
'''
import logging
import json
import requests


import config


COMPONENT_ENDPOINT_URL = config.BASEURL + "components/"


logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------#
def get_component_information_by_id(componentID, authToken):
    logger.debug("Entering get_component_information_by_id with componentID %s" %componentID)
    
    
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken}  
    RESTAPI_URL = COMPONENT_ENDPOINT_URL + str(componentID) 
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
        return(response.json()["data"])
        
    elif response.status_code == 404:
        print("Component with id of %s was not found" %componentID)
    
    elif response.status_code == 500:
        print("Internal Server Error")

