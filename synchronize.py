'''
Created on Sep 14, 2019

@author: SGeary
'''

import sys
import logging
import json

###################################################################################
# Test the version of python to make sure it's at least the version the script
# was tested on, otherwise there could be unexpected results
if sys.version_info <= (3, 5):
    raise "Script created/tested against python version 3.5"
else:
    pass

###################################################################################
#  Set up logging handler to allow for different levels of logging to be capture

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', datefmt='%Y-%m-%d:%H:%M:%S',

filename="_workflow.log", filemode='w',level=logging.DEBUG)

logger = logging.getLogger(__name__)

import config

import FNCI.v7.projects.getProjectInventory
import FNCI.v6.project.getProjectID
import FNCI.v7.tasks.getTasks
import workflow.create_request
import workflow.update_request

#-------------------------------------------------#
def main():
    projectName = "Workflow"
    authToken = config.AUTHTOKEN
    v6_authToken = config.v6_AUTHTOKEN

    # Start to cycle through projects in v7 looking for open tasks
    # For now just the one project we have configured for testing
    for projectID in range(1,2):   
        # This is circular but in case we need to cycle via IDs
        projectName = FNCI.v7.projects.getProjectInventory.get_project_name_by_id(projectID, authToken)

        if projectName != "False":  # if False was not returned from the API call
            logger.debug("This should not be printed unless it's a good proejct ID")
            # This will be needed to create a project in v6 to find the associated ID for project creation
            projectOwnerEmail = FNCI.v7.projects.getProjectInventory.get_project_owner_email_id(projectID, authToken)
           
            print("Project name is %s" %projectName)
            print("Project owner eMail Address is %s" %projectOwnerEmail)
            
            # Since this is a valid ID get the associated tasks for the project
            
            # Get project Tasks
            
            
            # TODO
            
            
        else:
            logger.debug("No project has a projectID of %s" %projectID)

    
    #------------------------------------------------------------------------
    # This should only be done if there is an open task for a disclosed item in the v7 project
    # so it should be moved....
    
    # get v6 project ID from the v7 project name
    v6_projectID = FNCI.v6.project.getProjectID.get_project_id(config.v6_teamName, projectName, v6_authToken)
    
    
    if v6_projectID == "No Matching Project Found":
        print("Logic to create a project to match the v7 project required")
        
        '''
        # TODO
        
            Copy a baseline project that has all of the workflow configuration already in place
            
                which one is needed?   with our without configuration?
            
                /project/copyProjectWithConfiguration/{sourceProjectName}/{groupName}/{destinationProjectName}
                /project/customProjectCopy/{sourceProjectName}/{groupName}/{destinationProjectName}
                
                v6_ProjectID is the return value
              
        '''
    else:
        print("There is a corresponding project of name %s in v6" %projectName)
        print("    v6 ProjectID is %s" %v6_projectID) 
  

    
    #--------------------------------------------------------------------------#  
    # Create a dictionary from the JSON data containing the current PITR mappings
    # from previous script runs
    # Once the inventory data has the request ID associated with it this will be
    # removed
    #
    # TODO
    #---------------------------------------------------------------------------#
    
    # Project/Inventory/Task/Request Mappings - Filled in below
    PITR_MAPPINGS = {}
    PITR_MAPPINGS["requests"] = []

    # Set up a dictionary to hold a mapping between v7 tasks and v7 workflow
    INVENTORYITEM_REQUESTS = {}    
    try:
        PREVIOUS_REQUESTS = json.loads(open(config.PITR_MAPPINGS_FILE).read())
        logger.debug("Opening %s file for request that are currently being tracked" %config.PITR_MAPPINGS_FILE)
    
        for existing_request in PREVIOUS_REQUESTS["requests"]:
            # For now just focus on the specific project
            if existing_request["v7_projectId"] == projectID:
                # Add the entry to the dictionary
                INVENTORYITEM_REQUESTS[existing_request["v7_inventoryId"]] =  existing_request["v6_request"] 
    
            # Make sure to update the file with the current data as well
            PITR_MAPPINGS['requests'].append({
                'v7_projectId': existing_request["v7_projectId"],
                'v7_inventoryId': existing_request["v7_inventoryId"],
                'v7_taskId': existing_request["v7_taskId"],
                'v6_request': existing_request["v6_request"]
                })
  
    
    
    except:
        # The script so far has not run with any tasks to process
        logger.debug("%s file does not exist currently" %config.PITR_MAPPINGS_FILE)
    
    # Get the full inventory to create a dict of the inventoryid to componentIds
    COMPONENT_MAPPINGS= {}
    v7_INVENTORY = FNCI.v7.projects.getProjectInventory.get_project_inventory(projectID, authToken)
    #--------------------------------------------------------------------------#    
    # Create a dictionary containing key information about the inventory item    
    for inventoryITEM in v7_INVENTORY:
        inventoryItemId = inventoryITEM["id"]
        componentId = inventoryITEM["componentId"]
        componentVersionId = inventoryITEM["componentVersionId"]
        selectedLicenseId = inventoryITEM["selectedLicenseId"]
        disclosed = inventoryITEM["disclosed"]
        
        # was the item disclosed?
        if disclosed == True:
        
            # Use INVENTORYITEM_REQUESTS dict until the item is added to the response
            # see if the ID has a mapped request in the dictionary
            if inventoryItemId in INVENTORYITEM_REQUESTS:
                requestId = INVENTORYITEM_REQUESTS[inventoryItemId]
            else:
                requestId = ""  # Assume a blank value is what the response JSON will contain if it does not exist
                
            # Is this all we care about from the inventory item itself?           
            COMPONENT_MAPPINGS[inventoryItemId] = [requestId, componentId, componentVersionId, selectedLicenseId]
        else:
            print("This was not disclosed")
    #------------------------------------------------------------------------------------------------------------#
    print("")
    print("Get the project tasks")
    TASKS = FNCI.v7.tasks.getTasks.get_task_by_projectID(projectID, authToken)
    
    # Cycle through the associated tasks for the project
    for task in TASKS:
        inventoryId = task["inventoryId"]
        workflowTaskType = task["workflowTaskType"]

        
        # We only care about task of type MANUAL_INVENTORY_REVIEWw
        if workflowTaskType == "MANUAL_INVENTORY_REVIEW":
            taskId = task["id"]
            
            # Find any task mapped to the inventory ID
            if inventoryId in COMPONENT_MAPPINGS.keys():
                
                # Does this item have a valid workflow request ID?
                if COMPONENT_MAPPINGS[inventoryId][0] == "":
                    
                    createdById = task["createdById"]
                    logger.debug("Task was created by user with ID: %s" %createdById)
                    # Map the created Id value back to an email for v6 to determine the ID
                    # For now assume it is the same as the project owner
                    # TODO
                    requesterEmail = projectOwnerEmail
                                  
                    newRequestID = workflow.create_request.create_new_request(v6_projectID, taskId, projectOwnerEmail, requesterEmail, COMPONENT_MAPPINGS[inventoryId])
                    print("Request %s created for v7 Inventory Item %s - task %s" %(newRequestID, inventoryId, taskId))
                    
                    # Update the dictionary with the newly created request                    
                    PITR_MAPPINGS['requests'].append({
                        'v7_projectId': projectID,
                        'v7_inventoryId': inventoryId,
                        'v7_taskId': taskId,
                        'v6_request': newRequestID
                        }) 
                    
                else:
                    workflow.update_request.get_update_for_existing_request(v6_projectID, taskId, COMPONENT_MAPPINGS[inventoryId][0] )
            else:
                logger.debug("Inventory item with id %s has no review tasks" %inventoryId)
                


    # Now write the data back out to the file        
    with open(config.PITR_MAPPINGS_FILE, 'w') as outfile:
        json.dump(PITR_MAPPINGS, outfile, indent=3)


    print("Script Complete")
#------------------------------------------------------------------#


if __name__ == "__main__":
    main() 
    