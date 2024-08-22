import requests
import json


def microsoft_todo_generate_access_token(creds):
    """
       Generates an access token that will be used for authentication purposes
    :param str client_id: Used for authentication purposes. 
    :param str client_secret: Used for authentication purposes. 
    :param str client_refresh_token: Used for authentication purposes. 

    :return: Returns an access token
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        token_endpoint="https://login.microsoftonline.com/common/oauth2/v2.0/token"
        request_body = {
            'client_id': cred['clientId'],
            'client_secret': cred['clientSecret'],
            'scope': ' '.join(['https://graph.microsoft.com/.default'] +['offline_access']),
            'refresh_token': cred['refreshToken'],
            "grant_type": "refresh_token",
        }
        response = requests.post(token_endpoint, data=request_body)
        response_json = response.json()
        if "access_token" in response_json:
            return response_json["access_token"]
        else:
            return {"access_token": "Invalid access_token"}
    except Exception as error:
        raise Exception(error)


###########################################################################################


def microsoft_todo_get_many_lists(access_token):
    """
       Get a list of the todoTaskList objects and their properties.
    :param str access_token: Used for authentication purposes. 

    :return: Returns a collection of todoTaskList objects in the response body.
    :rtype: dict
    """
    try:
        endpoint_url = f'https://graph.microsoft.com/v1.0/me/todo/lists'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        response = requests.get(endpoint_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(response.json())
    except Exception as e:
        raise Exception(e) 

def microsoft_todo_get_list(access_token,params):
    """
        Returns a todo list object with its properties
    :param str access_token: Used for authentication purposes. 
    :param dict params: Contains the Id of the list to be returned
    
       - :list_id: (str, Required) The Id of the list to be retrieved
    
    :return: a todoTaskList object in the response body.
    :rtype: dict
    """
    try:
        if 'list_id' in params:
            list_id=params["list_id"]
            endpoint_url = f'https://graph.microsoft.com/v1.0/me/todo/lists/{list_id}'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            response = requests.get(endpoint_url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing list id")
    except Exception as e:
        raise Exception(e) 

def microsoft_todo_create_list(access_token,params):
    """
     Create a new lists object.

    :param str access_token: Used for authentication purposes. 
    :param dict params: contains properties to be added to the created list
    
        - :displayName: (str, Required) tField indicating title of the task list.
        - :isOwner: (bool) 	True if the user is owner of the given task list.
        - :isShared: (bool) True if the task list is shared with other users
        - :wellknownListName: (str)  Possible values are: none, defaultList, flaggedEmails, unknownFutureValue.
       
        
    :return: Details about the created list
    :rtype: dict
    """
    try:
        if 'displayName' in params:
            list = {}
            for key, value in params.items():
             if key:
                list[key] = value
            endpoint_url = f'https://graph.microsoft.com/v1.0/me/todo/lists'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            response = requests.post(endpoint_url,json=list, headers=headers)
            if response.status_code == 201:
                return response.json()
            else:
                raise Exception(response.json())
        else:
         raise Exception("missing list name")
    except Exception as e:
        raise Exception(e) 

def microsoft_todo_update_list(access_token,params):
    """
     Updates a  lists object.

    :param str access_token: Used for authentication purposes. 
    :param dict params: contains properties to be added(modified) to the created list
    
        - :displayName: (str, Required) tField indicating title of the task list.
        - :isOwner: (bool) 	True if the user is owner of the given task list.
        - :isShared: (bool) True if the task list is shared with other users
        - :wellknownListName: (str)  Possible values are: none, defaultList, flaggedEmails, unknownFutureValue.
       
        
    :return: Details about the updated list
    :rtype: dict
    """
    try:
        if 'list_id' in params:
            list = {}
            key_to_skip=['list_id']
            for key, value in params.items():
             if key in key_to_skip:
                 continue
             if key:
                list[key] = value
            list_id=params["list_id"]
            endpoint_url = f'https://graph.microsoft.com/v1.0/me/todo/lists/{list_id}'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            response = requests.patch(endpoint_url,json=list, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.json())
        else:
         raise Exception("missing list id")
    except Exception as e:
        raise Exception(e) 
    
def microsoft_todo_delete_list(access_token,params):
    """
        Deletes a todo list object with its properties
    :param str access_token: Used for authentication purposes. 
    :param dict params: Contains the Id of the list to be deleted
    
       - :list_id: (str, Required) The Id of the channel to be deleted
    
    :return: a success/failure statement of the deletion of the list object.
    :rtype: dict
    """
    try:
        if 'list_id' in params:
            list_id=params["list_id"]
            endpoint_url = f'https://graph.microsoft.com/v1.0/me/todo/lists/{list_id}'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            response = requests.delete(endpoint_url, headers=headers)
            if response.status_code == 204:
                return f"List of id {list_id} deleted successfully"
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing list id")
    except Exception as e:
        raise Exception(e) 


def microsoft_todo_get_many_tasks(access_token,params):
    """
       Get a list of the todoTask objects and their properties.
    :param str access_token: Used for authentication purposes. 

    :return: Returns a collection of todoTask objects in the response body.
    :rtype: dict
    """
    try:
        if 'list_id' in params:
            list_id=params["list_id"]
            endpoint_url = f'https://graph.microsoft.com/v1.0/me/todo/lists/{list_id}/tasks'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            response = requests.get(endpoint_url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing list Id")
    except Exception as e:
        raise Exception(e) 
    

def microsoft_todo_get_task(access_token,params):
    """
        Returns a todo task object with its properties
    :param str access_token: Used for authentication purposes. 
    :param dict params: Contains properties of the task to be returned
    
       - :list_id: (str, Required) The Id of the list to which the task belongs
       - :task_id: (str, Required) The Id of the task to be returned
    
    :return: a todoTask object in the response body.
    :rtype: dict
    """
    try:
        required_params=['list_id','task_id']
        if all(param in params for param in required_params):
            list_id=params['list_id']
            task_id=params['task_id']
            endpoint_url = f'https://graph.microsoft.com/v1.0/me/todo/lists/{list_id}/tasks/{task_id}'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            response = requests.get(endpoint_url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing required paramters")
    except Exception as e:
        raise Exception(e) 


def microsoft_todo_update_task(access_token,params):
    """
     Updates properties of a task object in a specified todoTaskList.

    :param str access_token: Used for authentication purposes. 
    :param dict params: contains properties to be added(modified) to the created task
    
        - :list_id: (str, Required) the id of the list to which the task belongs 
        - :task_id: (str, Required) the id of the task to be modified
        - :title: (str) A brief description of the task.
        - :body: (dict) 	The task body that typically contains information about the task.
        - :dueDateTime: (dict) The date in the specified time zone that the task is to be finished.
        - :importance: (str) 	The importance of the task. Possible values are: low, normal, high.
        - :reminderDateTime: (dict) The date and time for a reminder alert of the task to occur.
        - :status: (str) 	Indicates the state or progress of the task. Possible values are: notStarted, inProgress, completed, waitingOnOthers, deferred.
        
    :return: Details about the updated task
    :rtype: dict
    :Examples:
    >>> params = {
        "task_id":"",
        "list_id":"",
        "title":"first task", 
        "body": {
            "content":"content", 
            "contentType":"text" 
        },
        "dueDateTime":  {
            "dateTime": "2024-02-11T00:00:00.0000000",
            "timeZone":"UTC"  
            },
         "reminderDateTime":{
            "dateTime": "2024-02-11T00:00:00.0000000",
            "timeZone":"UTC"  
            },
        "importance":"low",	
        "status":"completed" 
        }
    """
    try:
        required_params=['list_id','task_id']
        if all(param in params for param in required_params):
            task = {}
            for key, value in params.items():
             keys_to_skip=['list_id','task_id']
             if key in keys_to_skip:
                 continue
             else:
                task[key] = value
            list_id=params['list_id']
            task_id=params['task_id']
            endpoint_url = f'https://graph.microsoft.com/v1.0/me/todo/lists/{list_id}/tasks/{task_id}'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            response = requests.patch(endpoint_url, headers=headers,json=task)
            if response.status_code == 200:
                return response.json()
            else:
             raise Exception(response.json())
        else:
            raise Exception("missing required data")
    except Exception as e:
        raise Exception(e) 

def microsoft_todo_create_task(access_token,params):
    """
     Create a new task object in a specified todoTaskList.

    :param str access_token: Used for authentication purposes. 
    :param dict params: contains properties to be added to the created task
    
        - :list_id: (str, Required) the id of the list to which the task belongs 
        - :title: (str, Required) A brief description of the task.
        - :body: (dict) 	The task body that typically contains information about the task.
        - :dueDateTime: (dict) The date in the specified time zone that the task is to be finished.
        - :importance: (str) 	The importance of the task. Possible values are: low, normal, high.
        - :reminderDateTime: (dict) The date and time for a reminder alert of the task to occur.
        - :status: (str) 	Indicates the state or progress of the task. Possible values are: notStarted, inProgress, completed, waitingOnOthers, deferred.
        
    :return: Details about the created task
    :rtype: dict
    :Examples:
    >>> params = {
        "list_id":"",
        "title":"first task", 
        "body": {
            "content":"content", 
            "contentType":"text" 
        },
        "dueDateTime":  {
                    "dateTime": "2024-02-11T00:00:00.0000000",
                    "timeZone":"UTC"  
           },
        "reminderDateTime":  {
                    "dateTime": "2024-02-11T00:00:00.0000000",
                    "timeZone":"UTC"  
           },,
        "importance":"low",	
        "status":"completed" 
        }
    """
    try:
        required_params=['list_id','title']
        if all(param in params for param in required_params):
            task = {}
            for key, value in params.items():
             key_to_skip=['list_id']
             if key in key_to_skip:
                 continue
             else:
                task[key] = value
            list_id=params["list_id"]
            endpoint_url = f'https://graph.microsoft.com/v1.0/me/todo/lists/{list_id}/tasks'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            response = requests.post(endpoint_url, headers=headers,json=task)
            if response.status_code == 201:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing required data")
    except Exception as e:
        raise Exception(e) 
    

def microsoft_todo_delete_task(access_token,params):
    """
        Deletes a todo task object with its properties
    :param str access_token: Used for authentication purposes. 
    :param dict params: Contains properties of the task to be deleted
    
       - :list_id: (str, Required) The Id of the list to which the task belongs
       - :task_id: (str, Required) The Id of the task to be deleted
    
    :return: a statement declaring success / failure of the deletion process
    :rtype: dict
    """
    try:
        required_params=['list_id','task_id']
        if all(param in params for param in required_params):
            list_id=params["list_id"]
            task_id=params['task_id']
            endpoint_url = f'https://graph.microsoft.com/v1.0/me/todo/lists/{list_id}/tasks/{task_id}'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            response = requests.delete(endpoint_url, headers=headers)
            if response.status_code == 204:
                return f"task of id {task_id} deleted successfully"
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing required paramters")
    except Exception as e:
        raise Exception(e) 

def microsoft_todo_get_many_linkedresources(access_token,params):
    """
        Returns a list of linked resources in a partner application, based on which a specified task was created.
    :param str access_token: Used for authentication purposes. 
    :param dict params: Contains properties of the linked resources to be returned
    
       - :list_id: (str, Required) The Id of the list to which the resources belong
       - :task_id: (str, Required) The Id of the task to which the resources belong
    
    :return: a todoTask object in the response body.
    :rtype: dict
    """
    try:
        required_params=['list_id','task_id']
        if all(param in params for param in required_params):
            list_id=params["list_id"]
            task_id=params['task_id']
            endpoint_url = f'https://graph.microsoft.com/v1.0/me/todo/lists/{list_id}/tasks/{task_id}/linkedResources'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            response = requests.get(endpoint_url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing required paramteres")
    except Exception as e:
        raise Exception(e) 

def microsoft_todo_get_linkedresource(access_token,params):
    """
        Returns a linkedResource object in a partner application, based on which a specified task was created.
    :param str access_token: Used for authentication purposes. 
    :param dict params: Contains properties of the linked resource to be returned
    
       - :list_id: (str, Required) The Id of the list to which the resource belongs
       - :task_id: (str, Required) The Id of the task to which the resource belongs
       - :resource_id: (str, Required) The Id of the resource to be returned
    :return: a linked resource object in the response body.
    :rtype: dict
    """
    try:
        required_params=['list_id','task_id','resource_id']
        if all(param in params for param in required_params):
            list_id=params['list_id']
            task_id=params['task_id']
            resource_id=params['resource_id']
            endpoint_url = f'https://graph.microsoft.com/v1.0/me/todo/lists/{list_id}/tasks/{task_id}/linkedResources/{resource_id}'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            response = requests.get(endpoint_url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing required paramteres")
    except Exception as e:
        raise Exception(e) 

def microsoft_todo_create_linkedresource(access_token,params):
    """
        Creates a linkedResource object in a partner application, based on which a specified task was created.
    :param str access_token: Used for authentication purposes. 
    :param dict params: Contains properties of the linked resource to be created
    
       - :list_id: (str, Required) The Id of the list to which the resource belongs
       - :task_id: (str, Required) The Id of the task to which the resource belongs
       - :applicationName: (str, Required) Field indicating app name of the source that is sending the linked entity
       - :displayName: (str) Field indicating title of the linked entity.
       - :webUrl: (str) Deeplink to the linked entity
       - :externalId: (str) Id of the object that is associated with this task on the third-party/partner system
    :return: a linked resource object in the response body.
    :rtype: dict
    """
    try:
        required_params=['list_id','task_id','applicationName']
        if all(param in params for param in required_params):
            resource = {}
            for key, value in params.items():
             key_to_skip=['list_id','task_id']
             if key in key_to_skip:
                 continue
             else:
                resource[key] = value
            list_id=params['list_id']
            task_id=params['task_id']
            
            endpoint_url = f'https://graph.microsoft.com/v1.0/me/todo/lists/{list_id}/tasks/{task_id}/linkedResources'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            response = requests.post(endpoint_url, headers=headers,json=resource)
            if response.status_code == 201:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing required paramteres")
    except Exception as e:
        raise Exception(e) 

def microsoft_todo_update_linkedresource(access_token,params):
    """
        Updates a linkedResource object in a partner application, based on which a specified task was created.
    :param str access_token: Used for authentication purposes. 
    :param dict params: Contains properties of the linked resource to be modified
    
       - :list_id: (str, Required) The Id of the list to which the resource belongs
       - :task_id: (str, Required) The Id of the task to which the resource belongs
       - :resource_id: (str, Required) The Id of the resource to be modified
       - :applicationName: (str) Field indicating app name of the source that is sending the linked entity
       - :displayName: (str) Field indicating title of the linked entity.
       - :webUrl: (str) Deeplink to the linked entity
       - :externalId: (str) Id of the object that is associated with this task on the third-party/partner system
    :return: a linked resource object in the response body.
    :rtype: dict
    """
    try:
        required_params=['list_id','task_id','resource_id']
        if all(param in params for param in required_params):
            resource = {}
            for key, value in params.items():
             key_to_skip=['list_id','task_id','resource_id']
             if key in key_to_skip:
                 continue
             else:
                resource[key] = value
            list_id=params['list_id']
            task_id=params['task_id']
            resource_id=params['resource_id']
            endpoint_url = f'https://graph.microsoft.com/v1.0/me/todo/lists/{list_id}/tasks/{task_id}/linkedResources/{resource_id}'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            response = requests.patch(endpoint_url, headers=headers,json=resource)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing required paramteres")
    except Exception as e:
        raise Exception(e) 

def microsoft_todo_delete_linkedresource(access_token,params):
    """
        Delets a linkedResource object in a partner application, based on which a specified task was created.
    :param str access_token: Used for authentication purposes. 
    :param dict params: Contains properties of the linked resource to be deleted
    
       - :list_id: (str, Required) The Id of the list to which the resource belongs
       - :task_id: (str, Required) The Id of the task to which the resource belongs
       - :resource_id: (str, Required) The Id of the resource to be deleted
    :return: a success / failure of the deletion of the linked resource object
    :rtype: dict
    """
    try:
        required_params=['list_id','task_id','resource_id']
        if all(param in params for param in required_params):
            list_id=params['list_id']
            task_id=params['task_id']
            resource_id=params['resource_id']
            endpoint_url = f'https://graph.microsoft.com/v1.0/me/todo/lists/{list_id}/tasks/{task_id}/linkedResources/{resource_id}'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            response = requests.delete(endpoint_url, headers=headers)
            if response.status_code == 204:
                return f'linked resource with Id {resource_id} deleted successfully'
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing required paramteres")
    except Exception as e:
        raise Exception(e) 
    





