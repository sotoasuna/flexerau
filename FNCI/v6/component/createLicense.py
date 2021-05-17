'''
Created on Nov 1, 2019

@author: SGeary
'''
import logging
import requests
import json

import config


CREATE_ENDPOINT_URL = config.v6_BASEURL + "component/createLicense/"


logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------#
def create_custom_license(licenseDetails, authToken):
    logger.debug("Entering create_custom_component with licenseDetails %s" %(licenseDetails))
    # this is expecting json details from the v7 license apu
           
    createCustomLicenseBody = get_createCustomLicenseBody(licenseDetails) 
    logger.debug("createCustomLicenseBody:  %s"  %createCustomLicenseBody)
    headers = {'Content-Type': 'application/json', 'Authorization': authToken}  
    RESTAPI_URL = CREATE_ENDPOINT_URL

    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL) 
    
    try:
        response = requests.post(RESTAPI_URL, data=createCustomLicenseBody, headers=headers)
        print(response.text)
        logger.debug(json.dumps(response.json(), indent=3))  
        
    except requests.exceptions.RequestException as e:
        print(e)
        logger.debug(e)
        logger.debug(response)
        logger.debug(response.text)
        return False
    
    # Check the response code and proceed accordingly
    if response.status_code == 200:
        # We created the license so grab the ID to return
        v6_componentLicenseId = response.json()["Id"]
        return v6_componentLicenseId
                
    elif response.status_code == 400:
        # Let's see if it is a duplicate and grab the ID if it is
        try:
            v6_componentLicenseId = response.json()["Error(s) "]["Id"]
            return v6_componentLicenseId
       
        except:
            
        
            return False
    
    elif response.status_code == 500:
        print("Internal Server Error")
        return False
        
        
        
def get_createCustomLicenseBody(licenseDetails): 
    logger.debug("Entering get_createCustomLicenseBody with licenseDetails %s" %(licenseDetails))
    

    name = licenseDetails["name"]
    licenseUrl = licenseDetails["url"]
    description = (licenseDetails["description"])
    text = licenseDetails["text"].replace('\n', '\\n')

    if licenseUrl == None:
        licenseUrl = "Not available"

    createCustomLicenseBody = '''   
        {
           "name" :"''' + name + '''",
           "text" :"''' + text + '''",
           "url" :"''' + licenseUrl + '''",
           "description" :"''' + description + '''"
        }'''    
    
  
    
    
    return createCustomLicenseBody    