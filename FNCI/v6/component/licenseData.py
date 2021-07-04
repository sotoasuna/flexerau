'''
Created on Dec 11, 2019

@author: SGeary
'''
import logging
import requests
import json

import config


ENDPOINT_URL = config.v6_BASEURL + "component/licenseData"


logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------#
def get_license_data(licenseId, authToken):
    logger.debug("Entering get_license_data with licenseId %s" %(licenseId))
      
    headers = {'Content-Type': 'application/json', 'Authorization': authToken}  
    RESTAPI_URL = ENDPOINT_URL  + "?licenseIds=" + str(licenseId)
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL) 
    
    try:
        response = requests.get(RESTAPI_URL, headers=headers)
        #logger.debug(json.dumps(response.json(), indent=3))  
        
    except requests.exceptions.RequestException as e:
        print(e)
        logger.debug(e)
        logger.debug(response)
        logger.debug(response.text)
        return False
    
    # Check the response code and proceed accordingly
    if response.status_code == 200:
        # This returns a list since multiple licenses can be queried at one time
        # we this script only requests one at a time
        print(response.json()["Content"][0])
        return(response.json()["Content"][0])
        
    elif response.status_code == 404:
        print("Error code 404")
    
    elif response.status_code == 500:
        print("Internal Server Error")