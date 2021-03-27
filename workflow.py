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
import FNCI.v7.projects.getProjectID
import FNCI.v7.projects.getProjectInventory
import FNCI.v6.project.getProjectID

#----------------------------------------------------------------------#
def main():

    projectName = "Workflow"
    authToken = config.AUTHTOKEN
    v6_authToken = config.v6_AUTHTOKEN
    
    
    # get the project ID for the project
    projectID = FNCI.v7.projects.getProjectID.get_project_id(projectName, authToken)
    print("v7 ProjectID is %s" %projectID) 
    
    # This is circular but in case we need to cycle via IDs
    
    projectName = FNCI.v7.projects.getProjectInventory.get_project_name_by_id(projectID, authToken)
    print("Project name is %s" %projectName)
    
    # get v6 project ID from the v7 project name
    
    v6_projectID = FNCI.v6.project.getProjectID.get_project_id(config.v6_teamName, projectName, v6_authToken)
    
    if v6_projectID == "No Matching Project Found":
        print("Logic to create a project to match the v7 project required")
        
        '''
            Copy a baseline project that has all of the workflow configuration already in place
            
                which one is needed?   with our without configuration?
            
                /project/copyProjectWithConfiguration/{sourceProjectName}/{groupName}/{destinationProjectName}
                /project/customProjectCopy/{sourceProjectName}/{groupName}/{destinationProjectName}
              
        '''
    else:
        print("v6 ProjectID is %s" %v6_projectID) 
  
#------------------------------------------------------------------#


if __name__ == "__main__":
    main() 
    