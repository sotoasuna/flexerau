'''
Created on Nov 19, 2019

@author: SGeary
'''
import logging
import config
import FNCI.v6.project.copyProjectWithConfiguration

import FNCI.v6.project.changeProjectOwner
import FNCI.v7.users.searchUsers


logger = logging.getLogger(__name__)
#--------------------------------------------------------------------#

def create_v6_project(projectName, projectOwner):
    logger.debug("Entering create_v6_project for project %s which is owned by %s" %(projectName, projectOwner))
    
    admin_authToken = config.ADMIN_AUTHTOKEN
    v6_authToken = config.v6_AUTHTOKEN
    
    print("    - No matching project found in v6.  Creating project %s in v6" %projectName)
    v6_projectID = FNCI.v6.project.copyProjectWithConfiguration.create_cloned_project(config.v6_teamName, projectName, v6_authToken)
    print("        -- v6 ProjectID is %s" %v6_projectID) 

    # Get ID in v6 for project Owner of v7 project
    emailAddress = FNCI.v7.users.searchUsers.get_user_email_by_login(projectOwner, admin_authToken)
    v6_projectOwnerID = FNCI.v6.project.getUserId.get_user_id_from_email(emailAddress, v6_authToken)
    FNCI.v6.project.changeProjectOwner.change_project_owner(v6_projectID, v6_projectOwnerID, v6_authToken)
    
    logger.debug("v6 Project %s has an associated project ID of %s" %(projectName, v6_projectOwnerID))
    
    return v6_projectID