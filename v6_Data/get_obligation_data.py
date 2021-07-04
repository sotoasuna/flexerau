'''
Created on Dec 11, 2019

@author: SGeary
'''

import logging
import FNCI.v6.component.licenseData


logger = logging.getLogger(__name__)
#--------------------------------------------------------------------#

def get_v6_license_obligation_data(licenseID, v6_authToken):
    logger.debug("Entering get_v6_license_obligation_data for license with ID:  %s" %(licenseID))

    LICENSEDATA = FNCI.v6.component.licenseData.get_license_data(licenseID, v6_authToken)
    
    # Extract the required data from the full set of license data
    licenseName = LICENSEDATA["name"]
    OBLIGATIONS = LICENSEDATA["obligations"]
    
    # Create a dict with the needed obligation data
    OBLIGATIONDATA = {}
    
    for obligation in OBLIGATIONS:
        obligationID = obligation["id"]
        instruction = obligation["instruction"]
        obligationType = obligation["type"]["name"]
        triggerAction = obligation["triggerAction"]["name"]
        
        OBLIGATIONDATA[obligationID] = [obligationType, triggerAction, instruction]
        

    return licenseName, OBLIGATIONDATA