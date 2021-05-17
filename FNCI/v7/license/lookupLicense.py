'''
Created on Nov 1, 2019

@author: SGeary
'''
import logging
import requests
import json

import config



ENDPOINT_URL = config.BASEURL + "license/lookup"


logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------#
def lookup_license(licenseID, authToken):
    logger.debug("Entering lookup_license with licenseID: %s" %(licenseID))
      
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken}  
    RESTAPI_URL = ENDPOINT_URL + "?licenseId=" + str(licenseID)

    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)
    logger.debug("    headers: %s" %headers)  
    
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
        return response.json()["Content: "]
                
    elif response.status_code == 400:
        print("Error code 400")
        return False
    
    elif response.status_code == 401:
        print("Error code 401")
        print("Bad JWT?")

    
    
    elif response.status_code == 500:
        print("Internal Server Error")
        return False