'''
Created on Sep 21, 2019

@author: SGeary
'''
import logging
import requests
import sys

import config


ID_ENDPOINT_URL = config.v6_BASEURL + "project/copyProjectWithConfiguration/"


logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------#
def create_cloned_project(teamName, projectName, authToken):
    logger.debug("Entering create_project with team name %s and project Name %s" %(teamName, projectName))
      
    headers = {'Content-Type': 'application/json', 'Authorization': authToken}  
    RESTAPI_URL = ID_ENDPOINT_URL + config.v6_projectTemplatename + "/" + teamName +"/" + projectName
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)  
    
             
    try:
        response = requests.post(RESTAPI_URL, headers=headers)
    except ValueError:
        # no JSON returned
        logger.debug(response)
        logger.debug(response.text)
        
    # Check the response code and go from there
    if  response.status_code == 200:
        
        projectId = (response.json()["Content"])
        logger.debug("     Project ID for v6 project %s is %s" %(projectName, projectId))
        return projectId
    
    elif response.status_code == 400:
        logger.error("Error encountered while trying to clone template project")
        logger.error("RESPONSE DETAILS: %s" %(response.json()["Error(s) "]))
        print("Error encountered while trying to clone template project")
        print(response.json()["Error(s) "])
        print("Exiting script.....")
        sys.exit()   
        
    
    else:
        # Unknown status code that needs to be investigated
        logger.error("Unknown HttpStatusCode: %s" %response.json()["Error(s)"])
        print("Unknown Error.  Please see log for details.....")   
        
            

      
