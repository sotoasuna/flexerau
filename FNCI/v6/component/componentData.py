'''
Created on Oct 23, 2019

@author: SGeary
'''
import logging
import requests
import json

import config


WORKFLOW_ENDPOINT_URL = config.v6_BASEURL + "component/componentData"


logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------#
def get_component_data(componentId, authToken):
    logger.debug("Entering get_component_data with componentId %s" %(componentId))
      
    headers = {'Content-Type': 'application/json', 'Authorization': authToken}  
    RESTAPI_URL = WORKFLOW_ENDPOINT_URL  + "?componentIds=" + str(componentId) + "&summaryOnly=on"
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
        print(response.json()["Content"])
        
    elif response.status_code == 404:
        print("Error code 404")
    
    elif response.status_code == 500:
        print("Internal Server Error")

            
#-----------------------------------------------------------------------#
def get_component_versions(componentId, authToken):
    logger.debug("Entering get_component_data with componentId %s" %(componentId))
    
    # Create an empty list to hold the versions that we know about in v6 of the component
    versions = []
      
    headers = {'Content-Type': 'application/json', 'Authorization': authToken}  
    RESTAPI_URL = WORKFLOW_ENDPOINT_URL  + "?componentIds=" + str(componentId) + "&summaryOnly=on"
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)  
    response = requests.get(RESTAPI_URL, headers=headers)
             
    try:
        logger.debug(json.dumps(response.json(), indent=3))  
    except ValueError:
        # no JSON returned
        logger.debug(response)
        logger.debug(response.text)
        return  "FAILURE"
        
    # Now parse the results from the REST call
    if "HttpStatusCode" in response.json():
        HttpStatusCode = (response.json()["HttpStatusCode"]) 
        
        if  HttpStatusCode == 200:
            
            for component in response.json()["Content"]:
                for version in component["versions"]:
                    versions.append(version["id"])

            return (versions)


        elif HttpStatusCode == 400:           
            logger.info(response.json()["Message"])

        else:
            # Unknown status code that needs to be investigated
            print("Unknown Error.  Please see log for details.....")               

        return(False)
