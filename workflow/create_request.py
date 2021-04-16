'''
Created on Sep 17, 2019

@author: SGeary
'''

import logging

import config
import FNCI.v6.project.getUserId
import FNCI.v6.workflow.createRequest


logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------#
def create_new_request(v6_projectID, taskId, projectOwnerEmail, requesterEmail, INVENTORYDETAILS):
    logger.debug("Entering create_new_request")
    logger.debug("    Create a new request for taskId: %s" %taskId)
    
    v6_authToken = config.v6_AUTHTOKEN
    
    # Get the associated user IDs from the passed email address
    projectOwnerId = FNCI.v6.project.getUserId.get_user_id_from_email(projectOwnerEmail, v6_authToken)
    requesterId = FNCI.v6.project.getUserId.get_user_id_from_email(requesterEmail, v6_authToken)
    
    # Break apart the list for the component/version/license ids
    componentId = INVENTORYDETAILS[0]
    componentVersionId = INVENTORYDETAILS[1]
    selectedLicenseId = INVENTORYDETAILS[2]
   
    # Group the data together in a list to pass it to the RESTAPI
    REQUESTDETAILS = [v6_projectID, requesterId, projectOwnerId, componentId, componentVersionId, selectedLicenseId ]
    
    # Create request in v6
    requestId = FNCI.v6.workflow.createRequest.create_workflow_request(REQUESTDETAILS, v6_authToken)
  
    return requestId
    
    
    
    
    
    
    
    