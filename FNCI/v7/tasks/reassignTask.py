'''
Created on Oct 22, 2019

@author: SGeary
'''
import logging
import requests
import json

import config


TASKCLOSE_ENDPOINT_URL = config.BASEURL + "tasks/"


logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------#
def reassign_task_by_taskID(taskId, owner, authToken):
    logger.debug("Entering reassign_task_by_taskID with task ID %s and new owner %s" %(taskId, owner))
      
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken}  
    
    RESTAPI_URL = TASKCLOSE_ENDPOINT_URL + str(taskId) + "/reassign?ownerId=" + owner
    
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)  
    response = requests.put(RESTAPI_URL, headers=headers)
             
    try:
        logger.debug(json.dumps(response.json(), indent=3))  
    except ValueError:
        # no JSON returned
        logger.debug(response)
        logger.debug(response.text)
        return  "FAILURE"
  
    
    # Now parse the results from the REST call
    if "message" in response.json(): 
        # The project ID was returned
        if (response.json()["message"]) == "Task has been reassigned successfully.":
            logger.debug("     Task has been reassigned successfully")
        else:
            print("Unknown Error.  Please see log for details.....")   

    else:
        # Lots of different errors are possible          
        print("Unknown Error.  Please see log for details.....")         
        
        
