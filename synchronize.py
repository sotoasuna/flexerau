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

import FNCI.v7.projects.getProjectInventory
import FNCI.v6.project.getProjectID
import FNCI.v6.project.copyProjectWithConfiguration


import v7_Data.getTaskData
import v7_Data.getInventoryData
import RTI.RTIData  # this will be removed once it is supported in the inventory json data
import workflow.create_request
import workflow.update_request


#-------------------------------------------------#
def main():

    authToken = config.AUTHTOKEN
    v6_authToken = config.v6_AUTHTOKEN

    # Start to cycle through projects in v7 looking for open tasks
    # For now just the one project we have configured for testing
    for projectID in range(1,10):

        #------------------------------------------------------------------------------------------------------#
        projectName = FNCI.v7.projects.getProjectInventory.get_project_name_by_id(projectID, authToken)

        # As long on the above function did not return a value of False (valid project with inventory)
        if projectName.strip() == "NoProject":  # if False was not returned from the API call

            logger.debug("No project has a projectID of %s" %projectID)    
        
        else:
            print("\n") 
            print("Examining project %s for active manual review tasks." %projectName)

            # Get historical RTI ( Request/Task/Inventory Data) for project
            EXISTING_RTI_MAPPINGS = RTI.RTIData.get_historical_RTI_mappings(projectID)
                        
            # Get project Tasks and the inventory item they are associated with
            PROJECTTASKDATA = v7_Data.getTaskData.get_v7_task_data(projectID)

            # see if there are any tasks to worry about
            if PROJECTTASKDATA:
                print("    - There are active manual review tasks for this project")
                # See if there is a matching v6 project
                v6_projectID = FNCI.v6.project.getProjectID.get_project_id(config.v6_teamName, projectName, v6_authToken)
                
                if v6_projectID == "No Matching Project Found":
                    # Since there is no project in v6 one needs to be created                   
                    v6_projectID = FNCI.v6.project.copyProjectWithConfiguration.create_cloned_project(config.v6_teamName, projectName, v6_authToken)
                    print("    - No matching project found in v6.  Creating project %s in v6" %projectName)
                    print("        -- v6 ProjectID is %s" %v6_projectID) 

                else:
                    print("    - There is a corresponding project of name %s in v6" %projectName)
                    print("        -- v6 ProjectID is %s" %v6_projectID) 
                
    
                # Get the inventory from the project           
                PROJECTINVENTORYDATA = v7_Data.getInventoryData.get_v7_inventory_data(projectID)
              
                # Cycle though the tasks and get the inventory information for each one
                for taskId in PROJECTTASKDATA:
                    logger.debug("Check inventory for task with id %s" %taskId)
                    inventoryId = PROJECTTASKDATA[taskId]
                     
                    # For the task get the details for that project inventory item.
                    # What if a task has two items?  Could it?                 
                      
                    # get the data for the inventory item that the task is associated with  
                    if inventoryId in PROJECTINVENTORYDATA.keys():
                        
                        # print the component name to simplify tracking in console output
                        componentName = PROJECTINVENTORYDATA[inventoryId][3]
                        print("")
                        print("  ** Status for component: %s" %componentName)

                        if taskId in EXISTING_RTI_MAPPINGS.keys():
                            # There is a corresponding request in v6 for this task
                            v6RequestID = EXISTING_RTI_MAPPINGS[taskId][1]
                            
                            print("    - Task with ID %s already has a v6 requestId of %s associated with it." %(taskId, v6RequestID))
                            logger.debug("taskId %s already has a requestId %s associated with it." %(taskId, v6RequestID))
                            
                            workflow.update_request.get_update_for_existing_request(v6_projectID, taskId, v6RequestID )
                            
                        else:
                            # Create a new request
                            projectOwnerEmail = FNCI.v7.projects.getProjectInventory.get_project_owner_email_id(projectID, authToken)           
                            logger.debug("Project owner eMail Address is %s" %projectOwnerEmail)
                           
                            # Map the created Id value back to an email for v6 to determine the ID
                            # For now assume it is the same as the project owner
                            # TODO
                            requesterEmail = projectOwnerEmail                       
                            
                            v6RequestID = workflow.create_request.create_new_request(v6_projectID, taskId, projectOwnerEmail, requesterEmail, PROJECTINVENTORYDATA[inventoryId])
                            print("    - Task with ID taskId %s now has v6 requestId %s associated with it " %(taskId, v6RequestID))
                            
                            EXISTING_RTI_MAPPINGS[taskId] = [inventoryId, v6RequestID]
                            logger.debug("taskId %s now has requestId  %s associated with it " %(taskId, v6RequestID))
                            
                #--------------------------------------------------------------------------------------------------------------------------------#
                # Now update the json data file with any new requests that were created.
                # This will be removed once the inventory has the associated request ID
                RTI.RTIData.update_RTI_mappings(projectID, EXISTING_RTI_MAPPINGS)
                
            else:
                print("    - There are no tasks for this project")
            

          
    print("\n")
    print("Script Completed")
     
if __name__ == "__main__":
    main() 
    