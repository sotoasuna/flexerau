'''
Created on Mar 11, 2019

@author: SGeary
'''
import logging
import requests
import json

import config


ID_ENDPOINT_URL = config.BASEURL + "project/id"


logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------#
def get_project_id(projectName, authToken):
    logger.debug("Entering get_project_id with project name %s" %projectName)
      
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken}  
    RESTAPI_URL = ID_ENDPOINT_URL + "?projectName=" + projectName
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
    if "Content: " in response.json(): 
        # The project ID was returned
        projectID = (response.json()["Content: "])
        logger.debug("     Project ID for %s is %s" %(projectName, projectID))

        return projectID

    elif "Error: " in response.json():
        
        # Check the error message
        if  "The project name entered was not found" in response.json()["Error: "]:
            #  If it is already there should we just get the ID and return it??
            logger.info("The project name %s is not an existing project." %projectName)
            return  False
        
        else:
            # Lots of different errors are possible          
            logger.error("Unknown Error: %s" %response.json()["Error: "])
            print("Unknown Error.  Please see log for details.....")         
      
