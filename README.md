
# sca-codeinsight-workflow-v6

This python based script allows users to synchronize Code Insight v7 manual review tasks with Code Insight v6 requests for advanced workflow requirements.   

The process starts with creating an inventory item in v7 and marking it as disclosed.  A Manual Review Task is required as well which can be automatically created by enabling the "Manual Review Option" settings within the Projects Review and Remediation Settings Tab.  This task can also be manually created for each component if desired.

As the request goes through the workflow approval process, each time the script is executed the current status is updated with in the associated task.

Once the request has reached its completion the inventory item in v7 is approved/rejected and the task is closed.

This script can be manually executed or run via a cron job at selected intervals.

### Basic Script Flow

**Initial Synchronization**
 - Cycles through each project 
 - Project status != “Project Completed”
 - Cycle through each inventory item 
	 - Disclosed == “True” 
	 - Active Manual Review Task 
 - Create v6 project is required 
	 - v7 project name + v7 project ID
	 
 **Review Task w/out workflow association** 
 - Create draft request 
 - Update inventory item workflow url with newly created request details 

 **Review Task w/ workflow association** 
  - Update v7 task with latest workflow
	  - Current review level 
	  - Task owner to currently assigned reviewer 
  - If request has reached workflow termination 
	  - Close task
	  - Inventory item approved/rejected

------------

### Script Requirements


***pip install -r requirements.txt***


should install any missing dependencies which really is only requests since that will install the rest.

------------

### Script Configuration

In config.py please update all of the variables defined there to reflect the values for the v6 and v7 instances that are being synchronized.

**For FNCI v6 (Workflow System)**
```python
v6_FNCI_HOST = "localhost"  # IP Address of Workflow System
v6_FNCI_PORT = "8880" # Port for Workflow System
v6_BASEURL = "http://" + v6_FNCI_HOST + ":" + v6_FNCI_PORT + "/palamida/api/"
v6_REQUESTURL = "http://" + v6_FNCI_HOST + ":" + v6_FNCI_PORT + "/palamida/RequestDetails.htm?rid="
# Token for Workflow Admin User - This user must own the template project!
v6_AUTHTOKEN = "*****"
v6_teamName = "Engineering"
v6_projectTemplatename = "Workflow Template"  # Must be owned by user with Auth Token above
```
**For FNCI v7 (Scanning System)**
```python
FNCI_HOST = "localhost" # IP Address of Scanning System
FNCI_PORT = "8888" # Port for Scanning System
BASEURL = "http://" + FNCI_HOST + ":" + FNCI_PORT + "/codeinsight/api/"
# Token for Workflow Admin User ( must be added to project to update task)
ADMIN_AUTHTOKEN = "*****"
AUTHTOKEN = "*****"
```
In v7 the ADMIN_AUTHTOKEN is required for a few of the API calls that need admin rights. If the standard project owner does not have admin rights enter the token for an admin user

Finally specify the v7 vesion of FNCI to allow for future additions to the script based on functionality being added as time goes on.
```python
# To allow for changes in script that are release specific
FNCI_VERSION = "2020R1"
```

## License
[MIT](LICENSE.TXT)