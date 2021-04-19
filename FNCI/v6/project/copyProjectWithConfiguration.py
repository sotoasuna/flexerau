'''
Created on Sep 21, 2019

@author: SGeary
'''
import logging
import requests
import json

import config


ID_ENDPOINT_URL = config.v6_BASEURL + "project/copyProjectWithConfiguration/"


logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------#
def create_cloned_project(teamName, projectName, authToken):
    logger.debug("Entering create_project with team name %s and project Name %s" %(teamName, projectName))
      
    headers = {'Content-Type': 'application/json', 'Authorization': authToken}  
    RESTAPI_URL = ID_ENDPOINT_URL + config.v6_projectTemplatename + "/" + teamName +"/" + projectName
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)  
    response = requests.post(RESTAPI_URL, headers=headers)
             
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
            
            projectId = (response.json()["Content"]["Content"])
            logger.debug("     Project ID for v6 project %s is %s" %(projectName, projectId))
            return projectId
        
        elif HttpStatusCode == 400:
            logger.error("HttpStatusCode: %s" %response.json()["Error(s) "])
            print("Unknown Error.  Please see log for details.....")   
            
        
        else:
            # Unknown status code that needs to be investigated
            logger.error("Unknown HttpStatusCode: %s" %response.json()["Error(s) "])
            print("Unknown Error.  Please see log for details.....")   
            
            

      
