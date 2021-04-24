'''
Created on Sep 15, 2019

@author: SGeary
'''
import logging
import requests
import json

import config


TASKSEARCH_ENDPOINT_URL = config.BASEURL + "tasks/search"


logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------#
def get_task_by_projectID(projectID, authToken):
    logger.debug("Entering get_task_by_projectID with project ID %s" %projectID)
      
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken}  
    
    RESTAPI_URL = TASKSEARCH_ENDPOINT_URL + "?projectId=" + str(projectID)
    
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
    if "data" in response.json(): 
        # The project ID was returned
        TASKDATA = (response.json()["data"])
        logger.debug("     Task data retrieved for project ID %s" %projectID)

        return TASKDATA
    
    elif "errors" in response.json():
        logger.debug(response.json()["errors"])
        # Return empty list to check len against
        return {}

        
    else:
        # Lots of different errors are possible          
        print("Unknown Error.  Please see log for details.....")         
        return {}

#-----------------------------------------------------------------------#
def get_open_manual_review_tasks_by_projectID(projectID, authToken):
    logger.debug("Entering get_manual_review_tasks_by_projectID with project ID %s" %projectID)
      
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken}  
    
    RESTAPI_URL = TASKSEARCH_ENDPOINT_URL + "?projectId=" + str(projectID) +"&status=OPEN&type=MANUAL_INVENTORY_REVIEW&priority=ALL"
    
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
    if "data" in response.json(): 
        # The project ID was returned
        TASKDATA = (response.json()["data"])
        logger.debug("     Task data retrieved for project ID %s" %projectID)

        return TASKDATA
    
    elif "errors" in response.json():
        logger.debug(response.json()["errors"])
        # Return empty list to check len against
        return {}

        
    else:
        # Lots of different errors are possible          
        print("Unknown Error.  Please see log for details.....")         
        return {}
