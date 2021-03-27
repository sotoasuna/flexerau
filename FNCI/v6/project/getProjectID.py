'''
Created on Sep 14, 2019

@author: SGeary
'''
import logging
import requests
import json

import config


ID_ENDPOINT_URL = config.v6_BASEURL + "project/projectId/"


logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------#
def get_project_id(teamName, projectName, authToken):
    logger.debug("Entering get_project_id with team name %s and project Name %s" %(teamName, projectName))
      
    headers = {'Content-Type': 'application/json', 'Authorization': authToken}  
    RESTAPI_URL = ID_ENDPOINT_URL + teamName +"/" + projectName
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
            
            projectId = (response.json()["Content"]["projectId"])
            logger.debug("     Project ID for %s is %s" %(projectName, projectId))
            return projectId
        
        elif HttpStatusCode == 400:
            
                    # Check the error message
            if  "Sorry, we could not find a Project named" in response.json()["Message"]:
                #  If it is already there should we just get the ID and return it??
                logger.info("The project name %s is not an existing project." %projectName)
                return "No Matching Project Found"
        
        else:
            # Unknown status code that needs to be investigated
            logger.error("Unknown HttpStatusCode: %s" %response.json()["Error: "])
            print("Unknown Error.  Please see log for details.....")   
            
            

      
