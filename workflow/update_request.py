'''
Created on Sep 17, 2019

@author: SGeary
'''

import logging

import config
import FNCI.v6.workflow.requestData
import FNCI.v6.workflow.reviewers
import FNCI.v7.tasks.updateTask


logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------#
def get_update_for_existing_request(taskId, workflow_requestId):
    logger.debug("update_existing_request")
    print("update the  request for taskId: %s with details from workflow request ID %s" %(taskId, workflow_requestId))
    
    authToken = config.AUTHTOKEN
    v6_authToken = config.v6_AUTHTOKEN
    
    # Get workflow details from v6
    
    REQUESTDETAILS = FNCI.v6.workflow.requestData.get_current_request_details(workflow_requestId, v6_authToken)
    
    for detail in REQUESTDETAILS:
        
        updateDate = detail["updateDate"]
        currentReviewLevelName = detail["projectLevelDefinition"]["name"]
        # How to get contact name?
        
        currentReviewer = FNCI.v6.workflow.reviewers.get_current_reviewer(workflow_requestId, v6_authToken)
        
        UPDATEDETAILS = [workflow_requestId, updateDate, currentReviewLevelName, currentReviewer]
        
        logger.debug("Task Update Details: %s" %UPDATEDETAILS)
         
        # Provide an update to the task with the data retrieved from the workflow item
        FNCI.v7.tasks.updateTask.update_task(taskId, UPDATEDETAILS, authToken)
        
    

    

    
    # update task in v7
    
    '''  PUT /tasks/{taskID}
    
    {
      "summary": "Summary for the task",
      "priority": "MEDIUM",
      "details": "Details of the task"
    }'''