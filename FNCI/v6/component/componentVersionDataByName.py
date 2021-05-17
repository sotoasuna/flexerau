'''
Created on Oct 25, 2019

@author: SGeary
'''
import logging
import requests
import json

import config


COMPONENT_VERSION_ENDPOINT_URL = config.v6_BASEURL + "component/componentVersionDataByName"


logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------#
def get_component_version_data_by_name(componentId, versionName, authToken):
    logger.debug("Entering get_component_version_data with componentId %s and versionName %s" %(componentId, versionName ))
      
    headers = {'Content-Type': 'application/json', 'Authorization': authToken}  
    RESTAPI_URL = COMPONENT_VERSION_ENDPOINT_URL  + "?componentId=" + str(componentId) + "&versionName=" + str(versionName)

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
        # The version Exists
        return(response.json()["Content"])
        
    elif response.status_code == 400:
        # The version is not there for the component
        logger.debug(response.json()["Message"])
        return False
    
    elif response.status_code == 500:
        logger.debug("Internal Server Error")
        return False

            
