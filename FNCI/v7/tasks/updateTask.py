'''
Created on Sep 17, 2019

@author: SGeary
'''
import logging
import requests
import json

import config


TASKUPDATE_ENDPOINT_URL = config.BASEURL + "tasks/"


logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------#
def update_task(taskId, UPDATEINFORMATION, authToken):
    logger.debug("Entering update_task with task ID %s" %taskId)
      
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken}     
    
    RESTAPI_URL = TASKUPDATE_ENDPOINT_URL  + str(taskId)   
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)  
    
    taskUpdateBody = get_taskUpdateBody(UPDATEINFORMATION) 
    
    response = requests.put(RESTAPI_URL, data=taskUpdateBody, headers=headers)
             
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
        if (response.json()["message"]) == "Task has been updated successfully.":
            logger.debug("     The task was updated")


        
    else:
        # Lots of different errors are possible          
        print("Unknown Error.  Please see log for details.....")         
      


#--------------------------------------------------------# 
def get_taskUpdateBody(UPDATEINFORMATION): 
    
    workflow_requestId = UPDATEINFORMATION[0] 
    updateDate = UPDATEINFORMATION[1] 
    currentReviewLevelName = UPDATEINFORMATION[2]
    currentAssigneeName = UPDATEINFORMATION[3] 
    
    currentRequestIdText = "RequestID: " + str(workflow_requestId) + "<br>"
    lastUpdateText = "Last Activity: " + updateDate + "<br>"
    currentReviewLevelText = "Current Review Level: :  " + currentReviewLevelName + "<br>"
    currentAssigneeText = "Current Assignee:  " + currentAssigneeName
    
    updateText = currentRequestIdText + lastUpdateText + currentReviewLevelText + currentAssigneeText
    

    taskUpdateBody = '''{ 
        "details": "''' + updateText + '''"
    } '''
        
    return taskUpdateBody  