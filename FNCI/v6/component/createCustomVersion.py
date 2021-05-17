'''
Created on Oct 25, 2019

@author: SGeary
'''
import logging
import requests
import json

import config


CREATE_ENDPOINT_URL = config.v6_BASEURL + "component/createCustomVersion/"


logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------#
def create_custom_component_version(componentID, componentVersionName, authToken):
    logger.debug("Entering create_custom_component_version with componentId: %s and componentVersionName: %s" %(componentID, componentVersionName))
      
    headers = {'Content-Type': 'application/json', 'Authorization': authToken}  
    RESTAPI_URL = CREATE_ENDPOINT_URL + str(componentID) + "/" +  str(componentVersionName)

    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL) 
    
    try:
        response = requests.post(RESTAPI_URL, headers=headers)
        logger.debug(json.dumps(response.json(), indent=3))  
        
    except requests.exceptions.RequestException as e:
        print(e)
        logger.debug(e)
        logger.debug(response)
        logger.debug(response.text)
        return False
    
    # Check the response code and proceed accordingly
    if response.status_code == 200:
        return True
                
    elif response.status_code == 404:
        print("Error code 404")
        return False
    
    elif response.status_code == 500:
        print("Internal Server Error")
        return False
        
