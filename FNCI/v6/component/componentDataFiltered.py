'''
Created on Oct 25, 2019

@author: SGeary
'''
import logging
import json
import requests


import config


COMPONENT_ENDPOINT_URL = config.v6_BASEURL + "component/componentDataFiltered"


logger = logging.getLogger(__name__)


#-----------------------------------------------------------------------#
def get_filtered_component_data_by_name_and_title(componentName, componentTitle, authToken):
    logger.debug("Entering get_filtered_component_data_by_name_and_title")
    logger.debug("    Component Name: %s    Component Title: %s" %(componentName, componentTitle))
      
    headers = {'Content-Type': 'application/json', 'Authorization': authToken}  

    RESTAPI_URL = COMPONENT_ENDPOINT_URL  + "?searchTerms=" + componentName + "&filter=componentNameMatchesExactly&titleContains=" + componentTitle
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL) 
    
    try:
        response = requests.get(RESTAPI_URL, headers=headers)
        logger.debug(json.dumps(response.json(), indent=3))  
        
    except requests.exceptions.RequestException as e:
        print(e)
        logger.debug(e)
        logger.debug(response)
        logger.debug(response.text)
        return False
    
    # Check the response code and proceed accordingly
    if response.status_code == 200:
        return(response.json()["Content"])
        
    elif response.status_code == 404:
        print("Error code 404")
    
    elif response.status_code == 500:
        print("Internal Server Error")