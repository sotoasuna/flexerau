'''
Created on Sep 20, 2019

@author: SGeary
'''

import logging

import config
import FNCI.v7.tasks.getTasks


logger = logging.getLogger(__name__)


authToken = config.AUTHTOKEN
#------------------------------------------------------------------#

def get_v7_task_data(projectID):
    
    logger.debug("Entering get_v7_task_data with projectID: %s" %projectID)
    
    # Empty dict to hold the inventory item id and task id
    PROJECTTASKS = {}
    
    # Get the task data
    TASKS = FNCI.v7.tasks.getTasks.get_open_manual_review_tasks_by_projectID(projectID, authToken)

    # See if there were any tasks    
    if TASKS:
        # Cycle through the associated tasks for the project
        for task in TASKS:
            inventoryId = task["inventoryId"]
            taskId = task["id"]
            PROJECTTASKS[taskId] = inventoryId
            
        return PROJECTTASKS
    else:
        logger.debug("No tasks found for project with ID %s" %projectID)
        return {}