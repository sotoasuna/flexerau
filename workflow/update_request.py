'''
Copyright 2020 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Created on Sep 17, 2019

@author: SGeary
'''

import logging

import config
import FNCI.v6.workflow.requestData
import FNCI.v6.workflow.reviewers
import FNCI.v7.inventories.createWorkflowDetails
import FNCI.v7.inventories.getWorkflowDetails
import FNCI.v7.tasks.updateTask
import FNCI.v7.tasks.closeTask
import FNCI.v7.tasks.reassignTask

logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------#
def get_update_for_existing_request(v6_projectID, inventoryId, taskId, workflow_requestId, requestURL):
    logger.debug("Entering get_update_for_existing_request")
    logger.debug("Update the  request for taskId: %s with details from workflow request ID %s" %(taskId, workflow_requestId))
    print("    - Update the request for task with ID %s with details from v6 workflow request %s" %(taskId, workflow_requestId))
    
    authToken = config.AUTHTOKEN
    v6_authToken = config.v6_AUTHTOKEN
    
    # Get workflow details from v6  
    REQUESTDETAILS = FNCI.v6.workflow.requestData.get_current_request_details(workflow_requestId, v6_authToken)   
    
    # Cycle through even thought there should only be one in the response
    for detail in REQUESTDETAILS:

        updateDate = detail["updateDate"]

        # Does it need to be updated?  Check current task data to compare against the last update from v6
        WORKFLOWDETAILS = FNCI.v7.inventories.getWorkflowDetails.get_inventory_workflow_details(inventoryId, authToken)

        if WORKFLOWDETAILS == "Does Not Exist":
            # This is the first time so the information does not exist
            lastUpdated = "N/A"
        else:
            lastUpdated = WORKFLOWDETAILS["information"][2]["value"]
           

        # Based on how we constructed the list the Last Activity is the last item                   
        if updateDate != lastUpdated:
            # They are not equal so process the update

            # Make sure the request has been submitted and is not in draft status   
            if detail["reviewStatus"] != "draft":
                    
                # See if the request is still open    
                if detail["projectLevelDefinition"] != None:
                    # It's still open so grab the necessary details for the update             
                    currentReviewLevelName = detail["projectLevelDefinition"]["name"]
                    
                    # Get full details for the reviewer of the current request
                    reviewerList =  FNCI.v6.workflow.reviewers.get_current_reviewer(workflow_requestId, v6_authToken)

                    # There is only one active reviewer so get details from response
                    login = reviewerList[0]["login"]
                    firstName = reviewerList[0]["firstName"]
                    lastName = reviewerList[0]["lastName"]
                    email = reviewerList[0]["email"]

                    # Create the details dictionary for the task view and the inventory workflow details display
                    UPDATEDETAILS = {"Request URL": requestURL}
                    UPDATEDETAILS.update({"Workflow Request ID": workflow_requestId})
                    UPDATEDETAILS.update({"Last Activity": updateDate})
                    UPDATEDETAILS.update({"Current Review Level": currentReviewLevelName})
                    UPDATEDETAILS.update({"Current Reviewer Name": firstName + " " + lastName})
                    UPDATEDETAILS.update({"Current Reviewer eMail": email})

                    print("        -- Updating v7 task id %s with latest request status of request Id %s" %(taskId, workflow_requestId))
                    print("            --- Currently waiting for review by %s %s" %(firstName, lastName))
                    logger.debug("Task Update Details: %s" %UPDATEDETAILS)
                    
                    # Provide an update to the task with the data retrieved from the workflow item
                    if config.FNCI_VERSION >= "2020R1":
                        FNCI.v7.inventories.createWorkflowDetails.update_inventory_workflow_details(inventoryId, UPDATEDETAILS, authToken)
    
                    FNCI.v7.tasks.updateTask.update_task(taskId, UPDATEDETAILS, authToken)
                    FNCI.v7.tasks.reassignTask.reassign_task_by_taskID(taskId, login, authToken)
                    
        
                else:
                    # Get the resolution from the request data
                    reviewStatus = (detail["reviewStatus"]).upper()  # Get the status and capitalize it
                    # Get the latest update time            
                    updateDate = detail["updateDate"]
                    
                    # Update task contents as well with approval date and message
                    UPDATEDETAILS = {"Request URL": requestURL}
                    UPDATEDETAILS.update({"Workflow Request ID": workflow_requestId})
                    UPDATEDETAILS.update({"Request Resolution ": reviewStatus + " at " + updateDate})

                    # Provide an update to the task with the data retrieved from the workflow item
                    if config.FNCI_VERSION >= "2020R1":
                        FNCI.v7.inventories.createWorkflowDetails.update_inventory_workflow_details(inventoryId, UPDATEDETAILS, authToken)

                    # Provide an update to the task with the data retrieved from the workflow item
                    FNCI.v7.tasks.updateTask.update_task(taskId, UPDATEDETAILS, authToken)
                    FNCI.v7.tasks.closeTask.close_task_by_projectID(taskId, reviewStatus, authToken)
                    print("        -- Request %s has been closed with a status of %s" %(workflow_requestId, reviewStatus)) 
                    
            
            else:
                logger.debug("Request %s is still in a draft state" %workflow_requestId)
                print("        -- Request %s is currently in a draft state" %workflow_requestId)  
                # Update task contents as well with approval date and message
                UPDATEDETAILS = {"Request URL": requestURL}
                UPDATEDETAILS.update({"Workflow Request ID": workflow_requestId})
                UPDATEDETAILS.update({"Last Activity": updateDate})
                UPDATEDETAILS.update({"Current Review Level": "Request currently unsubmitted and in a draft state."})

                if lastUpdated != "None":

                    # Provide an update to the task with the data retrieved from the workflow item
                    if config.FNCI_VERSION >= "2020R1":
                        FNCI.v7.inventories.createWorkflowDetails.update_inventory_workflow_details(inventoryId, UPDATEDETAILS, authToken)
                    # Provide an update to the task with the data retrieved from the workflow item
                    FNCI.v7.tasks.updateTask.update_task(taskId, UPDATEDETAILS, authToken) 
                else:
                    logger.debug("There has been no activity since last update so no processing required")
                    print("             - No new activity since last update.")

        else:
            logger.debug("There has been no activity since last update so no processing required")
            print("        - No new activity since last update.")

#-----------------------------------------------------------------------#

        
