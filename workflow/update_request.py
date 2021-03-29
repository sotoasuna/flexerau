'''
Created on Sep 17, 2019

@author: SGeary
'''

import logging

import config
import FNCI.v6.workflow.requestData
import FNCI.v6.workflow.reviewers
import FNCI.v7.tasks.updateTask
import FNCI.v7.tasks.closeTask


logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------#
def get_update_for_existing_request(v6_projectID, taskId, workflow_requestId):
    logger.debug("update_existing_request")
    print("update the  request for taskId: %s with details from workflow request ID %s" %(taskId, workflow_requestId))
    
    authToken = config.AUTHTOKEN
    v6_authToken = config.v6_AUTHTOKEN
    
    # Get workflow details from v6
    
    REQUESTDETAILS = FNCI.v6.workflow.requestData.get_current_request_details(workflow_requestId, v6_authToken)
    
    requestURL = "http://" + config.v6_FNCI_HOST + ":8888/palamida/RequestDetails.htm?rid" + str(workflow_requestId) + "&projectId=" + str(v6_projectID) + "&from=requests"

    
    for detail in REQUESTDETAILS:
                
        # See if the request is still open    
        if detail["projectLevelDefinition"] != None:
                        # it's still open so grab the necessary details for the update 
        
        
            updateDate = detail["updateDate"]
            currentReviewLevelName = detail["projectLevelDefinition"]["name"]
            
            # Get full details for the reviewer of the current request
            currentReviewer = FNCI.v6.workflow.reviewers.get_current_reviewer(workflow_requestId, v6_authToken)
            
            UPDATEDETAILS = [requestURL, workflow_requestId, updateDate, currentReviewLevelName, currentReviewer]
            
            logger.debug("Task Update Details: %s" %UPDATEDETAILS)
             
            # Provide an update to the task with the data retrieved from the workflow item
            FNCI.v7.tasks.updateTask.update_task(taskId, UPDATEDETAILS, authToken)
            
  
        else:
            # Get the resolution from the request data
            reviewStatus = (detail["reviewStatus"]).upper()  # Get the status and capitalize it
            
            # Update task contents as well with approval date and message
            #UPDATEDETAILS = [requestURL, workflow_requestId, updateDate, currentReviewLevelName, currentReviewer]
            FNCI.v7.tasks.closeTask.close_task_by_projectID(taskId, reviewStatus, authToken)
            
        
    

    

    
    # update task in v7
    
    '''  PUT /tasks/{taskID}
    
    {
      "summary": "Summary for the task",
      "priority": "MEDIUM",
      "details": "Details of the task"
    }'''