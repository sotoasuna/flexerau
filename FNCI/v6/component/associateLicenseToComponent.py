'''
Created on Nov 1, 2019

@author: SGeary
'''
import logging
import requests
import json

import config


ENDPOINT_URL = config.v6_BASEURL + "component/associateLicenseToComponent/"


logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------#
def associate_license_to_component(componentID, componentLicenseId, authToken):
    logger.debug("Entering associate_license_to_component with componentId: %s and componentLicenseId: %s" %(componentID, componentLicenseId))
      
    headers = {'Content-Type': 'application/json', 'Authorization': authToken}  
    RESTAPI_URL = ENDPOINT_URL + str(componentID) + "/" +  str(componentLicenseId)

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
                
    elif response.status_code == 400:
        logger.debug("Error code 400 - associate_license_to_component ")
        return False
    
    elif response.status_code == 500:
        print("Internal Server Error")
        return False
        
