import json
import requests
status = [200, 201, 202, 204, 206, 207, 208]
def leadsquared_create_lead(creds,params):
    """
    Create a lead in LeadSquared.

    :param dict cred:
        - apiHost (str): Host URL for LeadSquared API. (required)
        - accessKey (str): Access key for LeadSquared API. (required)
        - secretKey (str): Secret key for LeadSquared API. (required)

    :param list params: List of lead attributes and their values. At least one of the following must be provided:
        - {"Attribute": "EmailAddress", "Value": "example@example.com"} (required)
        - {"Attribute": "FirstName", "Value": "John"} (required)
        - {"Attribute": "LastName", "Value": "Doe"} (required)
        - {"Attribute": "Phone", "Value": "123456789"} (required)

    :return: JSON response containing information about the created lead.
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        url = f"https://{cred['apiHost']}/v2/LeadManagement.svc/Lead.Create"
        headers = {
            "Content-Type": "application/json",
            "x-LSQ-AccessKey": cred['accessKey'],
            "x-LSQ-SecretKey": cred['secretKey']
        }
        response = requests.post(url, headers=headers, json=params)
        if response.status_code in status:
            return response.json()
        else:
            raise Exception(f"Failed to create lead. Status code: {response.status_code}, Reason: {response.text}")
    except Exception as e :
        raise Exception(e)
    

def leadsquared_update_lead(creds,params):
    """
    Update a lead in LeadSquared.

    :param dict cred:
        - 'apiHost' (str): Host URL for LeadSquared API. (required)
        - 'accessKey' (str): Access key for LeadSquared API. (required)
        - 'secretKey' (str): Secret key for LeadSquared API. (required)

    :param list params: List of lead attributes and their values to be updated.
        - 'leadId' (str): Lead Id for LeadSquared API. (required)
        Each attribute-value pair should be in the format {"Attribute": "<attribute_name>", "Value": "<attribute_value>"}.

    :return: JSON response containing information about the updated lead.
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        lead_id = None
        for item in params:
            if item.get("Attribute") == "leadId":
                lead_id = item.get("Value")
                params.remove(item)
                break
        if not lead_id:
            raise Exception("LeadId not found")
        url = f"https://{cred['apiHost']}/v2/LeadManagement.svc/Lead.Update?leadId={lead_id}"
        headers = {
            "Content-Type": "application/json",
            "x-LSQ-AccessKey": cred['accessKey'],
            "x-LSQ-SecretKey": cred['secretKey']
        }
        response = requests.post(url, headers=headers, json=params)
        if response.status_code in status:
            return response.json()
        else:
            raise Exception(f"Failed to update lead. Status code: {response.status_code}, Reason: {response.text}")
    except Exception as e :
        raise Exception(e)
    
def leadsquared_add_activity(creds,params):
    """
    Add an activity for a prospect in LeadSquared.

    :param dict cred:
        - 'apiHost' (str): Host URL for LeadSquared API. (required)
        - 'accessKey' (str): Access key for LeadSquared API. (required)
        - 'secretKey' (str): Secret key for LeadSquared API. (required)

    :param dict params: Parameters for adding the activity.
        - 'RelatedProspectId' (str): ID of the prospect related to the activity. (required)
        - 'ActivityEvent' (int): ID of the activity event. (required)
        - 'ActivityDateTime' (str): Date and time of the activity in 'YYYY-MM-DD HH:MM:SS' format. (required)
        - 'ActivityNote' (str, optional): Note for the activity. (optional)

    :return: JSON response containing information about the added activity.
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        if 'RelatedProspectId' and 'ActivityEvent' and 'ActivityDateTime' in params:
            url = f"https://{cred['apiHost']}/v2/ProspectActivity.svc/Create"
            headers = {
                "Content-Type": "application/json",
                "x-LSQ-AccessKey": cred['accessKey'],
                "x-LSQ-SecretKey": cred['secretKey']
            }
            response = requests.post(url, headers=headers, json=params)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception(f"Failed to add activity. Status code: {response.status_code}, Reason: {response.text}")
        else:
            raise Exception("Missing Input Data")
    except Exception as e :
        raise Exception(e)
    
def leadsquared_add_task(creds,params):
    """
    Add a task in LeadSquared.

    :param dict cred:
        - 'apiHost' (str): Host URL for LeadSquared API. (required)
        - 'accessKey' (str): Access key for LeadSquared API. (required)
        - 'secretKey' (str): Secret key for LeadSquared API. (required)

    :param dict params: Parameters for adding the task.
        - 'TaskList' (list of dict): List containing task details.
            Each task dictionary should contain:
            - 'Name' (str): Name of the task. (required)
            - 'RelatedEntityId' (str): ID of the related entity. (required)
            - 'RelatedEntity' (str): Related entity type. (required)
            - 'Description' (str, optional): Description of the task. (optional)
            - 'DueDate' (str, optional): Due date of the task in 'YYYY-MM-DD HH:MM:SS' format. (optional)
            - 'OwnerEmailAddress' (str, optional): Email address of the task owner. (optional)
            - 'TaskType' (dict): Dictionary containing task type details.
                - 'Name' (str): Name of the task type. (required)

    :return: JSON response containing information about the added task.
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        if 'TaskList' in params:
            if "Name" and "RelatedEntityId" and "RelatedEntity" in params["TaskList"][0]:
                headers = {
                    "Content-Type": "application/json",
                    "x-LSQ-AccessKey": cred['accessKey'],
                    "x-LSQ-SecretKey": cred['secretKey']
                }
                task = params["TaskList"][0]
                lead_id = task['RelatedEntityId']
                lead_api = f"https://{cred['apiHost']}/v2/LeadManagement.svc/Leads.GetById?id={lead_id}"
                lead_response = requests.get(lead_api, headers=headers)
                if lead_response.status_code in status:
                    url = f"https://{cred['apiHost']}/v2/Task.svc/Bulk/Create"
                    response = requests.post(url, headers=headers, json=params)
                    if response.status_code in status:
                        return response.json()
                    else:
                        raise Exception(f"Failed to add task. Status code: {response.status_code}, Reason: {response.text}")
                else:
                    raise Exception(f"Incorect Lead Id. Status code: {lead_response.status_code}, Reason: {lead_response.text}")
            else:
                raise Exception("Missing Input Data")
        else:
            raise Exception("Missing Input Data")
    except Exception as e :
        raise Exception(e)
    
def leadsquared_add_sales_activity(creds,params):
    """
    Add a sales activity in LeadSquared.

    :param dict cred:
        - 'apiHost' (str): Host URL for LeadSquared API. (required)
        - 'accessKey' (str): Access key for LeadSquared API. (required)
        - 'secretKey' (str): Secret key for LeadSquared API. (required)

    :param dict params: Parameters for adding the sales activity.
        - 'ProspectId' (str): ID of the prospect associated with the sales activity. (required)
        - 'ProductSku' (str): SKU of the product. (required)
        - 'Status' (str): Status of the sales activity. (required)
        - 'Revenue' (str): Revenue generated from the sales activity. (required)
        - 'SalesOwnerEmail' (str): Email address of the sales owner. (required)
        - 'SalesDate' (str): Date and time of the sales activity in 'YYYY-MM-DD HH:MM:SS' format. (required)

    :return: JSON response containing information about the added sales activity.
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        if 'ProspectId' and 'ProductSku' and 'SalesOwnerEmail' and 'SalesDate' and 'Revenue' and 'Status' in params:
            url = f"https://{cred['apiHost']}/v2/SalesActivity.svc/Create"
            headers = {
                "Content-Type": "application/json",
                "x-LSQ-AccessKey": cred['accessKey'],
                "x-LSQ-SecretKey": cred['secretKey']
            }
            response = requests.post(url, headers=headers, json=params)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception(f"Failed to add sales activity. Status code: {response.status_code}, Reason: {response.text}")
        else:
            raise Exception("Missing Input Data")
    except Exception as e :
        raise Exception(e)
    
def leadsquared_get_activity_details(creds,params):
    """
    Retrieve details of a specific activity in LeadSquared.

    :param dict cred:
        - 'apiHost' (str): Host URL for LeadSquared API. (required)
        - 'accessKey' (str): Access key for LeadSquared API. (required)
        - 'secretKey' (str): Secret key for LeadSquared API. (required)

    :param dict params: Parameters for retrieving activity details.
        - 'activityId' (str): ID of the activity to retrieve details for. (required)

    :return: JSON response containing information about the specified activity.
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        if 'activityId' in params:
            url = f"https://{cred['apiHost']}/v2/ProspectActivity.svc/GetActivityDetails"
            headers = {
                "Content-Type": "application/json",
                "x-LSQ-AccessKey": cred['accessKey'],
                "x-LSQ-SecretKey": cred['secretKey']
            }
            response = requests.get(url, headers=headers,params=params)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception(f"Failed to get activity details. Status code: {response.status_code}, Reason: {response.text}")
        else:
            raise Exception("Missing Input Data")
    except Exception as e :
        raise Exception(e)
    
def leadsquared_get_many_users(creds):
    """
    Retrieve details of many users from LeadSquared.

    :param dict cred:
        - 'apiHost' (str): Host URL for LeadSquared API. (required)
        - 'accessKey' (str): Access key for LeadSquared API. (required)
        - 'secretKey' (str): Secret key for LeadSquared API. (required)

    :return: JSON response containing information about the users.
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        url = f"https://{cred['apiHost']}/v2/UserManagement.svc/Users.Get"
        headers = {
            "Content-Type": "application/json",
            "x-LSQ-AccessKey": cred['accessKey'],
            "x-LSQ-SecretKey": cred['secretKey']
        }
        response = requests.get(url, headers=headers)
        if response.status_code in status:
            return response.json()
        else:
            raise Exception(f"Failed to get users. Status code: {response.status_code}, Reason: {response.text}")
    except Exception as e :
        raise Exception(e)
    
def leadsquared_find_lead(creds,params):
    """
    Find a lead in LeadSquared based on provided parameters.

    :param dict cred:
        - 'apiHost' (str): Host URL for LeadSquared API. (required)
        - 'accessKey' (str): Access key for LeadSquared API. (required)
        - 'secretKey' (str): Secret key for LeadSquared API. (required)

    :param dict params: Parameters for finding the lead.
        - 'id' (str): Retrieve lead by ID. (required)
        - 'EmailAddress' (str): Retrieve lead by email address. (required)
        - 'Parameter' (dict): Retrieve lead by custom parameters. (required)
            - 'LookupName' (str): Name of the attribute to search for. (required)
            - 'LookupValue' (str): Value of the attribute to search for. (required)
            - 'SqlOperator' (str): SQL operator for comparison. (required)

    :return: JSON response containing information about the found lead.
    :rtype: dict

    Note: One of 'id', 'EmailAddress', or 'Parameter' must be provided to search for a lead.
    """
    try:
        cred=json.loads(creds)
        headers = {
            "Content-Type": "application/json",
            "x-LSQ-AccessKey": cred['accessKey'],
            "x-LSQ-SecretKey": cred['secretKey']
        }
        if 'id' in params:
            url = f"https://{cred['apiHost']}/v2/LeadManagement.svc/Leads.GetById"
            response = requests.get(url, headers=headers,params=params)
        elif 'EmailAddress' in params:
            url = f"https://{cred['apiHost']}/v2/LeadManagement.svc/Leads.GetByEmailaddress"
            response = requests.get(url, headers=headers,params=params)
        elif 'Parameter' in params:
            url = f"https://{cred['apiHost']}/v2/LeadManagement.svc/Leads.Get"
            response = requests.post(url, headers=headers,json=params)
        else:
            raise Exception("Missing input data")
        if response.status_code in status:
            return response.json()
        else:
            raise Exception(f"Failed to find lead. Status code: {response.status_code}, Reason: {response.text}")
    except Exception as e:
        raise Exception(e)