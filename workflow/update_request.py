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
import FNCI.v7.tasks.reassignTask

logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------#
def get_update_for_existing_request(v6_projectID, taskId, workflow_requestId, requestURL):
    logger.debug("Entering get_update_for_existing_request")
    logger.debug("Update the  request for taskId: %s with details from workflow request ID %s" %(taskId, workflow_requestId))
    print("    - Update the request for task with ID %s with details from v6 workflow request %s" %(taskId, workflow_requestId))
    
    authToken = config.AUTHTOKEN
    v6_authToken = config.v6_AUTHTOKEN
    
    # Get workflow details from v6  
    REQUESTDETAILS = FNCI.v6.workflow.requestData.get_current_request_details(workflow_requestId, v6_authToken)   

    # Cycle through even thought there should only be one in the response
    for detail in REQUESTDETAILS:
        
        # Make sure the request has been submitted and is not in draft status   
        if detail["reviewStatus"] != "draft":
                
            # See if the request is still open    
            if detail["projectLevelDefinition"] != None:
                
                # It's still open so grab the necessary details for the update             
                updateDate = detail["updateDate"]
                currentReviewLevelName = detail["projectLevelDefinition"]["name"]
                
                # Get full details for the reviewer of the current request
                username, currentReviewer = FNCI.v6.workflow.reviewers.get_current_reviewer(workflow_requestId, v6_authToken)
                
                UPDATEDETAILS = [requestURL, workflow_requestId, updateDate, currentReviewLevelName, currentReviewer]
                
                print("        -- Updating v7 task id %s with latest request status of request Id %s" %(taskId, workflow_requestId))
                print("            --- Currently waiting for review by %s" %currentReviewer)
                logger.debug("Task Update Details: %s" %UPDATEDETAILS)
                 
                # Provide an update to the task with the data retrieved from the workflow item
                FNCI.v7.tasks.updateTask.update_task(taskId, UPDATEDETAILS, authToken)
                FNCI.v7.tasks.reassignTask.reassign_task_by_taskID(taskId, username, authToken)
                
      
            else:
                # Get the resolution from the request data
                reviewStatus = (detail["reviewStatus"]).upper()  # Get the status and capitalize it
                # Get the latest update time            
                updateDate = detail["updateDate"]
                
                # Update task contents as well with approval date and message
                UPDATEDETAILS = [requestURL, workflow_requestId, reviewStatus + " at " + updateDate, "None", "None"]
                # Provide an update to the task with the data retrieved from the workflow item
                FNCI.v7.tasks.updateTask.update_task(taskId, UPDATEDETAILS, authToken)
                FNCI.v7.tasks.closeTask.close_task_by_projectID(taskId, reviewStatus, authToken)
                print("        -- Request %s has been closed with a status of %s" %(workflow_requestId, reviewStatus)) 
                
        
        else:
            logger.debug("Request %s is still in a draft state" %workflow_requestId)
            print("        -- Request %s is currently in a draft state" %workflow_requestId)  
            # Update task contents as well with approval date and message
            UPDATEDETAILS = [requestURL, workflow_requestId, "N/A", "Request currently in Draft state", "N/A"]
            # Provide an update to the task with the data retrieved from the workflow item
            FNCI.v7.tasks.updateTask.update_task(taskId, UPDATEDETAILS, authToken)   

#-----------------------------------------------------------------------#

        
