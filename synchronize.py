'''
Created on Sep 14, 2019

@author: SGeary
'''

import sys
import logging

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

import FNCI.v7.projects.getProjects

import FNCI.v6.project.getProjectID

import FNCI.v7.users.searchUsers
import FNCI.v7.inventories.getInventoryItemDetails
import FNCI.v7.inventories.updateInventory


import v7_Data.getTaskData
import v7_Data.getInventoryData
import v7_Data.update_guidance_data
import v6_Data.manage_custom_data
import v6_Data.create_project
import v6_Data.get_obligation_data

import workflow.create_request
import workflow.update_request


#-------------------------------------------------#
def main():

    authToken = config.AUTHTOKEN
    admin_authToken = config.ADMIN_AUTHTOKEN
    v6_authToken = config.v6_AUTHTOKEN

    print("###############################################################################")
    # Start to cycle through projects in v7 looking for open tasks
    PROJECTS = FNCI.v7.projects.getProjects.get_project_list(admin_authToken)
    
    # Cycle through each project
    for project in PROJECTS:
        
        projectID = project["id"]
        projectName = project["name"]
        projectStatus = project["status"]
        projectOwner = project["owner"]
        
        # Only check for tasks/requests if the project is not "complete"
        if projectStatus != "Project Completed":
        
            print("\n") 
            print("Examining project %s for active manual review tasks." %projectName)
                        
            # Get project Tasks and the inventory item they are associated with
            PROJECTTASKDATA = v7_Data.getTaskData.get_v7_task_data(projectID)
    
            # see if there are any tasks to worry about
            if PROJECTTASKDATA:
                print("    - There are %s active manual review tasks for this project" %(len(PROJECTTASKDATA)))
                # See if there is a matching v6 project
                v6_projectID = FNCI.v6.project.getProjectID.get_project_id(config.v6_teamName, projectName, v6_authToken)
                
                if v6_projectID == "No Matching Project Found":
                    # Since there is no project in v6 one needs to be created                   
                    v6_projectID = v6_Data.create_project.create_v6_project(projectName, projectOwner)
                    
                else:
                    print("    - There is a corresponding project of name %s in v6" %projectName)
                    print("        -- v6 ProjectID is %s" %v6_projectID) 
                
              
                # Cycle though the tasks and get the inventory information for each one
                for taskId in PROJECTTASKDATA:
                    logger.debug("Check inventory for task with id %s" %taskId)
                    inventoryId = PROJECTTASKDATA[taskId][0]
                    logger.debug("    Inventory ID %s" %inventoryId)
                    
                    # See if there is an existing workflowURL for the inventory item associated to this task
                    workflowURL = FNCI.v7.inventories.getInventoryItemDetails.get_inventory_item_workflowURL_by_id(inventoryId, authToken)
    
                    # Is there a workflow request already in play?
                    if workflowURL == "None":
                        # There is no workflow item so create it
                        # Get the component details from the inventory Item
                        INVENTORYDATA = v7_Data.getInventoryData.get_v7_inventory_item_data(inventoryId, authToken)
                        
                        if len(INVENTORYDATA) > 0:
                            # This was disclosed so create the request
                            # No current mapping so create a new request
                            print("    - No previous mapping for task with ID:  %s" %taskId)
                            
                            # What is being requested for use?
                            componentId = INVENTORYDATA["componentId"] 
                            componentVersionId = INVENTORYDATA["componentVersionId"]
                            componentLicenseId = INVENTORYDATA["selectedLicenseId"]
                            
                            # See if there is any custom data within the request
                            if (componentId > 1000000000) or (componentVersionId > 1000000000) or (componentLicenseId > 1000000000):
                                # At least one item is custom
                                INVENTORYITEMDATA = v6_Data.manage_custom_data.determine_custom_data(INVENTORYDATA) 
                            
                            else:
                                # This is all stock data from the PDL
                                INVENTORYITEMDATA = [componentId, componentVersionId, componentLicenseId]
                            
                            # Users IDs associated with the task
                            ownerId = PROJECTTASKDATA[taskId][1]
                            createdById = PROJECTTASKDATA[taskId][2]
                            # Use the ID within the task data to get the user's email address which is needed
                            # on the v6 side to create the request
                            projectOwnerEmail = FNCI.v7.users.searchUsers.get_user_email_by_id(ownerId, admin_authToken)
                            requesterEmail = FNCI.v7.users.searchUsers.get_user_email_by_id(createdById, admin_authToken)
      
                            
                            logger.debug("Project owner eMail Address is %s" %projectOwnerEmail)
                            logger.debug("Requester eMail Address is %s" %requesterEmail)              
                            
                            v6RequestID = workflow.create_request.create_new_request(v6_projectID, taskId, projectOwnerEmail, requesterEmail, INVENTORYITEMDATA)
                            print("    - Task with ID taskId %s now has v6 requestId %s associated with it " %(taskId, v6RequestID))
                            
                            # Update Inventory Item with URL
                            requestURL = config.v6_REQUESTURL + str(v6RequestID) + "&projectId=" + str(v6_projectID) + "&from=requests"
                            
                            FNCI.v7.inventories.updateInventory.update_inventory_item_workflowURL(inventoryId, requestURL, authToken)
                            
                            '''
                            print("    - Updating Usage Guidance for inventory item with ID of %s" %(inventoryId))
                            # Update v7 Inventory Item with License Obligation Data from v6 
                            
                            componentLicenseId = INVENTORYITEMDATA[2]
                            licenseName, OBLIGATIONDATA = v6_Data.get_obligation_data.get_v6_license_obligation_data(componentLicenseId, v6_authToken)
                            
                            v7_Data.update_guidance_data.update_v7_guidance_notes(inventoryId, licenseName, OBLIGATIONDATA, authToken)
                           '''                                                        
                            # Update Task with info
                            workflow.update_request.get_update_for_existing_request(v6_projectID, inventoryId, taskId, v6RequestID, requestURL)
                        else:
                            logger.debug("No Inventory Data") 
    
                    else:
                        # This is an existing request so update the task with the latest information
                        # Get the v6RequestID from the workflowURL           
                        v6RequestID = workflowURL.split("=")[1].split("&")[0]
                        print("    - Task with ID %s already has a v6 requestId of %s associated with it." %(taskId, v6RequestID))
                        logger.debug("taskId %s already has a requestId %s associated with it." %(taskId, v6RequestID))    
                        workflow.update_request.get_update_for_existing_request(v6_projectID, inventoryId, taskId, v6RequestID, workflowURL)
                
            else:
                print("    - There are no tasks for this project")
            
            print("")
            print("###############################################################################")
            
        else:
            # The project is marked as completed
            print("\n") 
            print("Project %s has a status of %s so no action taken" %(projectName, projectStatus))
            print("")
            print("###############################################################################")
          
    print("\n")
    print("Script Completed")
     
if __name__ == "__main__":
    main() 
    