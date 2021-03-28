'''
Created on Sep 17, 2019

@author: SGeary
'''
import logging
import requests
import json

import config


WORKFLOW_ENDPOINT_URL = config.v6_BASEURL + "workflow/reviewers"


logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------#
def get_current_reviewer(requestId, authToken):
    logger.debug("Entering get_current_reviewer with requestId %s" %(requestId))
      
    headers = {'Content-Type': 'application/json', 'Authorization': authToken}  
    RESTAPI_URL = WORKFLOW_ENDPOINT_URL  + "?requestId=" + str(requestId)
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
            
            for contact in response.json()["Content"]:            
                firstName = contact["firstName"]
                lastName = contact["lastName"]
                email = contact["email"]
            
            currentReviewer = "%s %s (%s)" %(firstName, lastName, email)
             
            return currentReviewer

        elif HttpStatusCode == 400:           
            logger.info(response.json()["Message"])
        else:
            # Unknown status code that needs to be investigated
            print("Unknown Error.  Please see log for details.....")   
            
            

      
