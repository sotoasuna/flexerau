'''
Created on Oct 24, 2019

@author: SGeary
'''
import logging

import FNCI.v7.component.getComponent
import FNCI.v6.component.componentDataFiltered
import FNCI.v6.component.componentVersionDataByName
import v6_Data.create_custom_data

import config

logger = logging.getLogger(__name__)


v6_authToken = config.v6_AUTHTOKEN
authToken = config.AUTHTOKEN
#--------------------------------


#----------------------------------------------------------------------------------#
def check_v6_custom_component(INVENTORY_ITEM_DATA):
    logger.debug("Entering check_v6_custom_component")
    logger.debug("INVENTORY_ITEM_DATA: %s" %INVENTORY_ITEM_DATA)

    # INVENTORY_ITEM_DATA contains [componentId, componentVersionId, selectedLicenseId,
    #                                    name, componentName, componentVersionName ]  
    componentId = INVENTORY_ITEM_DATA[0] 
   
    # Get more details about the custom component to find the v6 component ID
    v7_component_details = FNCI.v7.component.getComponent.get_component_information_by_id(componentId, authToken)
    
    # See if the custom component already exists in the v6 database using the name and title from v7        
    v7_componentName = v7_component_details["name"]
    v7_componentTitle = v7_component_details["title"]
    
    v6_component_data = FNCI.v6.component.componentDataFiltered.get_filtered_component_data_by_name_and_title(v7_componentName, v7_componentTitle, v6_authToken)
    
    if v6_component_data["totalFound"] == 0:
        # There were no matches so create this component
        logger.debug("We need to create the component")
        v6_componentId = v6_Data.create_custom_data.create_v6_custom_component(v7_component_details)
    else:
        # So there is more than one match.  Do exact match for both name and title
        logger.debug("There is at least a match with the name but need to verify title")
    
        for component in v6_component_data["components"]:
            name = component["name"]
            title = component["title"]
            logger.debug("v7 Component Name: %s   v7 Component Title: %s" %(v7_componentName, v7_componentTitle))
            logger.debug("v6 Component Name: %s   v7 Component Title: %s" %(name, title))
           
            
            if name == v7_componentName and title == v7_componentTitle:
                # This is the one we want
                v6_componentId = component["id"]
                Match = True
                break
            else:
                Match = False

        if Match == False:
            # There was no exact match from the results so create a new component
            v6_componentId = v6_Data.create_custom_data.create_v6_custom_component(v7_component_details)

    logger.debug("    The ID for the custom component is %s" %v6_componentId)

    # We have both the component and version IDs now so return them
    return v6_componentId


#----------------------------------------------------------------------------------#
def check_v6_custom_version(componentID, componentVersionID, componentVersionName):
    logger.debug("Entering check_v6_custom_version")
    logger.debug("    componentID:  %s, componentVersionID:  %s" %(componentID, componentVersionID))

    # Query v6 for versions that are associated with the component already
    logger.debug("Check for custom version")
    v6_componentVersionData = FNCI.v6.component.componentVersionDataByName.get_component_version_data_by_name(componentID, componentVersionName, v6_authToken)
    
    
    if not v6_componentVersionData:
        # There was no version ID so we need to create the version
        logger.debug("Create custom version...")
        v6_componentVersionID = v6_Data.create_custom_data.create_v6_custom_version(componentID, componentVersionName)
    else:
        logger.debug("   The custom version was found")
        v6_componentVersionID = v6_componentVersionData["id"]
    
    # Return the ID that was retrieved or created
    return(v6_componentVersionID)

#----------------------------------------------------------------------------------#
def check_v6_custom_license(componentID, componentVersionID, componentLicenseId): 
    logger.debug("Entering check_v6_custom_license")
    logger.debug("    componentID:  %s, componentVersionID:  %s, componentLicenseId:  %s" %(componentID, componentVersionID, componentLicenseId))
    
    # For now the easiest way to check for a customer license is to try to create it again
    # If the license exists the error will return the license ID
    # If the license does not exist it will be created and the license ID will be returned
    v6_componentLicenseId = v6_Data.create_custom_data.create_v6_custom_license(componentID, componentVersionID, componentLicenseId)

    
    # Return the ID that was retrieved or created
    return(v6_componentLicenseId)
    
    
    
           
        