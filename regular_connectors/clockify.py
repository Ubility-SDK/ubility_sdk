import requests

valid_status_code = [200, 201, 202, 204, 206, 207, 208]
###########################################################################
############# CLIENT  ###################################
def Clockify_create_client(params, api_token):
    """
        Creates a client with properties passed in the parameters
     
    :param str api_token: (str,required) used for authentication purposes
    :param dict params: contains specific properties to be added to the client.
    
        :workspace_id: (str,required) the workspace of the client
        :name: (str,required) the name of the client
        :email: (str) a unique email of the client
        :address: (str)  address of the client (optional)
        :note: (str) additional note about the client (optional)
    :return: details about the created client
    :rtype: dict  
    """
    try:
        if "name" in params and "workspace_id" in params:
            client = {}
            for key, value in params.items():
                client[key] = value
            url = f"https://api.clockify.me/api/workspaces/{params['workspace_id']}/clients"
            headers = {"X-Api-Key": api_token, "Content-Type": "application/json"}
            response = requests.post(url, headers=headers, json=client)
            if response.status_code in valid_status_code:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)
    
def Clockify_get_client(params, api_token):
    """
        Returns a client of a specific id.
    
    :param str api_token: (str,required) used for authentication purposes.
    :param dict params:
    
      :id: (str,required) the id of the client to be returned
      :workspace_id: (str,required) the workspace of the client
    :return: details about the retrieved client(id,properties,..)
    :rtype: dict  
    """
    try:
        if "id" in params and "workspace_id" in params:
            api_url = f"https://api.clockify.me/api/v1/workspaces/{params['workspace_id']}/clients/{params['id']}"
            headers = {
               "X-Api-Key": api_token,
            }
            response = requests.get(api_url, headers=headers)
            if response.status_code in valid_status_code:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)
    
def Clockify_update_client(params, api_token):
    """
        Updates a client with properties passed in the parameters
     
    :param str api_token: (str,required) used for authentication purposes
    :param dict params: contains specific properties to be added(or modified) to the client.
    
        :id: (str,required) the id of the client whose properties are to be modified
        :workspace_id: (str,required) the workspace of the client
        :name: (str) the name of the client
        :email: (str) a unique email of the client
        :address: (str)  address of the client (optional)
        :note: (str) additional note about the client (optional)
    :return: details about the updated client
    :rtype: dict  
    """
    try:
        if "id" in params and "workspace_id" in params:
            client_id = params["id"]
            api_url = f"https://api.clockify.me/api/v1/workspaces/{params['workspace_id']}/clients/{client_id}"
            headers = {
                "X-Api-Key": api_token,
                "Content-Type": "application/json",
            }
            client = {}
            keys_to_skip = ["client_id"]
            for key, value in params.items():
                if key in keys_to_skip:
                    continue
                if value:
                    client[key] = value
            response = requests.put(api_url, headers=headers, json=client)
            if response.status_code in valid_status_code:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)
    
def Clockify_delete_client(params, api_token):
    """
        Deletes a client of a specific id.
    
    :param str api_token: (str,required) used for authentication purposes.
    :param dict params:
    
      :id: (str,required) the id of the client to be deleted
      :workspace_id: (str,required) the workspace of the client
    :return: details about the deleted client(id,properties,..)
    :rtype: dict  
    """
    try:
        if "id" in params and "workspace_id" in params:
            api_url = f"https://api.clockify.me/api/v1/workspaces/{params['workspace_id']}/clients/{params['id']}"
            headers = {
                "X-Api-Key": api_token,
            }
            response = requests.delete(api_url, headers=headers)
            if response.status_code in valid_status_code:
                return f"Deleted client with  ID: {params['id']}"
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)
    
def Clockify_get_all_clients(params, api_token):
    """
        Returns the clients with custom properties.
     
    :param str api_token: (str,required) used for authentication purposes
    :param dict params: filters the properties to be returned for each client.
    
      :workspace_id: (str,required) the workspace of the clients.
      :archived: (bool)  possible values are True or False.
      :name: (str) filtering the client name
      :sort-order: (str) One of ASCENDING, DESCENDING. Defaults to ASCENDING
        
    :return: The list of clients with the filtered properties.
    :rtype: dict
    """
    try:
        if "workspace_id" in params:
            api_url = f"https://api.clockify.me/api/v1/workspaces/{params['workspace_id']}/clients/"
            query_string = "&".join([f"{key}={value}" for key, value in params.items()])
            full_url = f"{api_url}?{query_string}"
            headers = {
                "X-Api-Key": api_token,
            }
            response = requests.get(full_url, headers=headers)
            if response.status_code in valid_status_code:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing workspace Id")
    except Exception as e:
        raise Exception(e)
############################ WORKSPACE AND USERS #########################################
def Clockify_get_all_users(params, api_token):
    """
        Returns the users with custom properties.
     
    :param str api_token: (str,required) used for authentication purposes
    :param dict params: filters the properties to be returned for each user.
    
      :workspace_id: (str,required) the workspace of the users.
      :status: (bool)  possible values are ACTIVE,INACTIVE,PENDING,DECLINED
      :name: (str) filtering the user name
      :email: (str) filtering the user email
      :sort-order: (str) One of ASCENDING, DESCENDING. Defaults to ASCENDING
      :sort-column: (str) One of email, name, and hourly-rate
    :return: The list of users with the filtered properties.
    :rtype: dict
    """
    try:
        if "workspace_id" in params:
            api_url = f"https://api.clockify.me/api/v1/workspaces/{params['workspace_id']}/users/"
            query_string = "&".join([f"{key}={value}" for key, value in params.items()])
            full_url = f"{api_url}?{query_string}"
            headers = {
                "X-Api-Key": api_token,
            }
            response = requests.get(full_url, headers=headers)
            if response.status_code in valid_status_code:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing input data")
    except Exception as e:
        raise Exception(e)
    
def Clockify_get_all_workspaces(api_token):
    """
        Returns the workspaces available
     
    :param str api_token: (str,required) used for authentication purposes
    :return: The list of available workspaces 
    :rtype: dict
    """
    api_url = f"https://api.clockify.me/api/v1/workspaces/"
    headers = {
        "X-Api-Key": api_token,
    }
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code in valid_status_code:
            return response.json()
        else:
            raise Exception(response.json())
    except Exception as error:
        raise Exception(error)
########################################################################################
############# PROJECT #######################################
def Clockify_create_project(params, api_token):
    """
        Creates a project with properties passed in the parameters
     
    :param str api_token: (str,required) used for authentication purposes
    :param dict params: contains specific properties to be added to the project.
    
        :workspace_id: (str,required) the workspace of the project
        :name: (str,required) the name of the project
        :billable: (bool)  possible values are True or False.
        :isPublic: (bool)  possible values are True or False.
        :estimate: (dict)  contains 'estimate' and 'type'(AUTO or MANUAL)
        :hourlyRate: (dict) contains fields 'amount',and 'since'
        :clientId: (str) the client of the project
        :color: (str) 
        :note: (str) additional note about the project 
    :return: details about the created project
    :rtype: dict  
    """
    try:
        if "name" in params and "workspace_id" in params:
            project = {}
            for key, value in params.items():
                project[key] = value
            url = f"https://api.clockify.me/api/workspaces/{params['workspace_id']}/projects"
            
            
            headers = {"X-Api-Key": api_token, "Content-Type": "application/json"}
            response = requests.post(url, headers=headers, json=project)
            if response.status_code in valid_status_code:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)
    
def Clockify_get_all_projects(params, api_token):
    """
        Returns the projects with custom properties.
     
    :param str api_token: (str,required) used for authentication purposes
    :param dict params: filters the properties to be returned for each project.
    
      :workspace_id: (str,required) the workspace of the projects.
      :archived: (bool)  possible values are True or False.
      :name: (str) filtering the project name
      :sort-order: (str) One of ASCENDING, DESCENDING. Defaults to ASCENDING
      :contains-client: (bool)  possible values are True or False.
      :client-status: (str) One of ARCHIVED, ACTIVE.
      :billable: (bool)  possible values are True or False.
      :contains-user: (bool)  possible values are True or False.
      :is-template: (bool)  possible values are True or False.
      :sort-column: (str) possible values are name,client name,duration
      :clients: (arr,str) clients of the project
      :users: (arr,str) users of the project
      :user-status: (str) One of ACTIVE, PENDING,DECLINED,INACTIVE,ALL
    :return: The list of projects with the filtered properties.
    :rtype: dict
    """
    try:
        if "workspace_id" in params:
            api_url = f"https://api.clockify.me/api/v1/workspaces/{params['workspace_id']}/projects/"
            query_string = "&".join([f"{key}={value}" for key, value in params.items()])
            full_url = f"{api_url}?{query_string}"
            headers = {
                "X-Api-Key": api_token,
            }
            response = requests.get(full_url, headers=headers)
            if response.status_code in valid_status_code:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing input data")
    except Exception as e:
        raise Exception(e)

def Clockify_get_project(params, api_token):
    """
        Returns a project of a specific id.
    
    :param str api_token: (str,required) used for authentication purposes.
    :param dict params:
    
      :id: (str,required) the id of the project to be returned
      :workspace_id: (str,required) the workspace of the project
    :return: details about the retrieved project(id,properties,..)
    :rtype: dict  
    """
    try:
        if "id" in params and "workspace_id" in params:
            api_url = f"https://api.clockify.me/api/v1/workspaces/{params['workspace_id']}/projects/{params['id']}"
            headers = {
                "X-Api-Key": api_token,
            }
            response = requests.get(api_url, headers=headers)
            if response.status_code in valid_status_code:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)
    
def Clockify_update_project(params, api_token):
    """
        Updates a project with properties passed in the parameters
     
    :param str api_token: (str,required) used for authentication purposes
    :param dict params: contains specific properties to be added(or modified) to the project.
    
        :workspace_id: (str,required) the workspace of the project
        :id: (str,required) the id of the project
         :name: (str) the name of the project
        :billable: (bool)  possible values are True or False.
        :isPublic: (bool)  possible values are True or False.
        :estimate: (dict)  contains 'estimate' and 'type'(AUTO or MANUAL)
        :hourlyRate: (dict) contains fields 'amount',and 'since'
        :clientId: (str) the client of the project
        :color: (str) 
        :note: (str) additional note about the project 
    :return: details about the updated project
    :rtype: dict  
    """
    try:
        if "id" in params and "workspace_id" in params:
            project_id = params["id"]
            api_url = f"https://api.clockify.me/api/v1/workspaces/{params['workspace_id']}/projects/{project_id}"
            headers = {
                "X-Api-Key": api_token,
                "Content-Type": "application/json",
            }
            project = {}
            keys_to_skip = ["project_id"]
            for key, value in params.items():
                if key in keys_to_skip:
                    continue
                if value:
                    project[key] = value
            response = requests.put(api_url, headers=headers, json=project)
            if response.status_code in valid_status_code:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)

def Clockify_delete_project(params, api_token):
    """
        Deletes a project of a specific id.
    
    :param str api_token: (str,required) used for authentication purposes.
    :param dict params:
    
      :id: (str,required) the id of the project to be deleted
      :workspace_id: (str,required) the workspace of the project
    :return: details about the deleted project(id,properties,..)
    :rtype: dict  
    """
    try:
        if "id" in params and "workspace_id" in params:
            api_url = f"https://api.clockify.me/api/v1/workspaces/{params['workspace_id']}/projects/{params['id']}"
            headers = {
                "X-Api-Key": api_token,
            }
            response = requests.delete(api_url, headers=headers)

            if response.status_code in valid_status_code:
                return f"Deleted project with  ID: {params['id']}"
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing input data")

    except Exception as error:
        raise Exception(error)
################ TAGS ##############################################################
def Clockify_create_tag(params, api_token):
    """
        Creates a tag with properties passed in the parameters
     
    :param str api_token: (str,required) used for authentication purposes
    :param dict params: contains specific properties to be added to the tag.
    
        :workspace_id: (str,required) the workspace of the tag
        :name: (str,required) the name of the tag
    :return: details about the created tag
    :rtype: dict  
    """
    try:
        if "name" in params and "workspace_id" in params:
            tag = {}
            for key, value in params.items():
                tag[key] = value
            url = (
                f"https://api.clockify.me/api/workspaces/{params['workspace_id']}/tags"
            )
            headers = {"X-Api-Key": api_token, "Content-Type": "application/json"}
            response = requests.post(url, headers=headers, json=tag)
            if response.status_code in valid_status_code:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def Clockify_get_tag(params, api_token):
    """
        Returns a tag of a specific id.
    
    :param str api_token: (str,required) used for authentication purposes.
    :param dict params:
    
      :id: (str,required) the id of the tag to be returned
      :workspace_id: (str,required) the workspace of the tag
    :return: details about the retrieved tag(id,properties,..)
    :rtype: dict  
    """
    try:
        if "id" in params and "workspace_id" in params:
            api_url = f"https://api.clockify.me/api/v1/workspaces/{params['workspace_id']}/tags/{params['id']}"
            headers = {
                "X-Api-Key": api_token,
            }
            response = requests.get(api_url, headers=headers)
            if response.status_code in valid_status_code:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def Clockify_get_all_tags(params, api_token):
    """
        Returns the tags with custom properties.
     
    :param str api_token: (str,required) used for authentication purposes
    :param dict params: filters the properties to be returned for each tag.
    
      :workspace_id: (str,required) the workspace of the tags.
      :archived: (bool)  possible values are True or False.
      :name: (str) filtering the tag name
      :sort-order: (str) One of ASCENDING, DESCENDING. Defaults to ASCENDING
      :sort-column: (str) possible values are NAME
    :return: The list of tags with the filtered properties.
    :rtype: dict
    """
    try:
        if "workspace_id" in params:
            api_url = f"https://api.clockify.me/api/v1/workspaces/{params['workspace_id']}/tags/"
            query_string = "&".join([f"{key}={value}" for key, value in params.items()])
            full_url = f"{api_url}?{query_string}"
            headers = {
                "X-Api-Key": api_token,
            }
            response = requests.get(full_url, headers=headers)
            if response.status_code in valid_status_code:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def Clockify_update_tag(params, api_token):
    """
        Update a tag with properties passed in the parameters
     
    :param str api_token: (str,required) used for authentication purposes
    :param dict params: contains specific properties to be added(or modified) to the tag.
    
        :workspace_id: (str,required) the workspace of the tag
        :id: (str,required) the id of the tag to be updated
        :name: (str) the name of the tag
    :return: details about the updated tag
    :rtype: dict  
    """
    try:
        if "id" in params and "workspace_id" in params:
            tag_id = params["id"]
            api_url = f"https://api.clockify.me/api/v1/workspaces/{params['workspace_id']}/tags/{tag_id}"
            headers = {
                "X-Api-Key": api_token,
                "Content-Type": "application/json",
            }
            tag = {}
            keys_to_skip = ["tag_id"]
            for key, value in params.items():
                if key in keys_to_skip:
                    continue
                if value:
                    tag[key] = value
            response = requests.put(api_url, headers=headers, json=tag)
            if response.status_code in valid_status_code:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)

def Clockify_delete_tag(params, api_token):
    """
        Deletes a tag of a specific id.
    
    :param str api_token: (str,required) used for authentication purposes.
    :param dict params:
    
      :id: (str,required) the id of the tag to be deleted
      :workspace_id: (str,required) the workspace of the tag
    :return: details about the deleted tag(id,properties,..)
    :rtype: dict  
    """
    try:
        if "id" in params and "workspace_id" in params:
            api_url = f"https://api.clockify.me/api/v1/workspaces/{params['workspace_id']}/tags/{params['id']}"
            headers = {
                "X-Api-Key": api_token,
            }
            response = requests.delete(api_url, headers=headers)
            if response.status_code in valid_status_code:
                return f"Deleted tag with  ID: {params['id']}"
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)
####################### TASKS ######################################
def Clockify_create_task(params, api_token):
    """
        Creates a task with properties passed in the parameters
     
    :param str api_token: (str,required) used for authentication purposes
    :param dict params: contains specific properties to be added to the task.
    
        :workspace_id: (str,required) the workspace of the task
        :project_id: (str,required) the project of the task
        :name: (str,required) the name of the task
        :status: (str) possible values are ACTIVE,DONE
        :assigneeIds: (arr of str)
        :esimate: (str) 
        
    :return: details about the created task
    :rtype: dict  
    """
    try:
        if "name" in params and "projectId" in params and "workspace_id" in params:
            task = {}
            keys_to_skip = ["projectId"]
            for key, value in params.items():
                if key in keys_to_skip:
                    continue
                if value:
                    task[key] = value
            url = f"https://api.clockify.me/api/workspaces/{params['workspace_id']}/projects/{params['projectId']}/tasks"
            headers = {"X-Api-Key": api_token, "Content-Type": "application/json"}
            response = requests.post(url, headers=headers, json=task)
            if response.status_code in valid_status_code:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def Clockify_get_task(params, api_token):
    """
        Returns a task of a specific id.
    
    :param str api_token: (str,required) used for authentication purposes.
    :param dict params:
    
      :id: (str,required) the id of the task to be returned
      :workspace_id: (str,required) the workspace of the task
      :project_id: (str,required) the project of the task
    :return: details about the retrieved task(id,properties,..)
    :rtype: dict  
    """
    try:
        if "id" in params and "projectId" in params and "workspace_id" in params:
            api_url = f"https://api.clockify.me/api/v1/workspaces/{params['workspace_id']}/projects/{params['projectId']}/tasks/{params['id']}"
            headers = {
                "X-Api-Key": api_token,
            }
            response = requests.get(api_url, headers=headers)
            if response.status_code in valid_status_code:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def Clockify_get_all_tasks(params, api_token):
    """
        Returns the tasks with custom properties.
     
    :param str api_token: (str,required) used for authentication purposes
    :param dict params: filters the properties to be returned for each task.
    
      :workspace_id: (str,required) the workspace of the tasks.
      :project_id: (str,required) the project of the tasks.
      :is_active: (bool)  possible values are True or False.
      :name: (str) filtering the task name
      :sort-order: (str) One of ASCENDING, DESCENDING. Defaults to ASCENDING
      :sort-column: (str) possible values are NAME
    :return: The list of tasks with the filtered properties.
    :rtype: dict
    """
    try:
        if "projectId" in params and "workspace_id" in params:
            api_url = f"https://api.clockify.me/api/v1/workspaces/{params['workspace_id']}/projects/{params['projectId']}/tasks/"
            headers = {
                "X-Api-Key": api_token,
            }
            response = requests.get(api_url, headers=headers)
            if response.status_code in valid_status_code:
                return response.json()
            else:
                raise Exception(response)
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def Clockify_update_task(params, api_token):
    """
        Updates a task with properties passed in the parameters
     
    :param str api_token: (str,required) used for authentication purposes
    :param dict params: contains specific properties to be added(or modified) to the task.
    
        :workspace_id: (str,required) the workspace of the task
        :project_id: (str,required) the project of the task
        :amount: (int)
        :since: (str)
        
    :return: details about the updated task
    :rtype: dict  
    """
    try:
        if "projectId" in params and "workspace_id" in params:
            task = {}
            keys_to_skip = ["projectId", "id"]
            for key, value in params.items():
                if key in keys_to_skip:
                    continue
                if value:
                    task[key] = value
            url = f"https://api.clockify.me/api/workspaces/{params['workspace_id']}/projects/{params['projectId']}/tasks/{params['id']}"
            headers = {"X-Api-Key": api_token, "Content-Type": "application/json"}
            response = requests.put(url, headers=headers, json=task)
            if response.status_code in valid_status_code:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def Clockify_delete_task(params, api_token):
    """
        Deletes a task of a specific id.
    
    :param str api_token: (str,required) used for authentication purposes.
    :param dict params:
    
      :id: (str,required) the id of the task to be deleted
      :workspace_id: (str,required) the workspace of the task
      :project_id: (str,required) the project of the task
    :return: details about the deleted task(id,properties,..)
    :rtype: dict  
    """
    try:
        if "id" in params and "projectId" in params and "workspace_id" in params:
            api_url = f"https://api.clockify.me/api/v1/workspaces/{params['workspace_id']}/projects/{params['projectId']}/tasks/{params['id']}"
            headers = {
                "X-Api-Key": api_token,
            }
            response = requests.delete(api_url, headers=headers)
            if response.status_code in valid_status_code:
                return f"Deleted task with  ID: {params['id']}"
            else:
                raise Exception(response.json())
        raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)
################## TIME ENTRY ##################################################
def Clockify_create_time_entry(params, api_token):
    """
        Creates a time-entry with properties passed in the parameters
     
    :param str api_token: (str,required) used for authentication purposes
    :param dict params: contains specific properties to be added to the time-entry.
    
        :workspace_id: (str,required) the workspace of the time-entry
        :start: (string <date-time>,required) the start time of the time-entry
        :end: (string <date-time>) the end time of the time-entry
        :billable: (str) possible values are ACTIVE,DONE
        :projectId: (str)
        :tagIds: (arr of str) 
        :taskId: (str) 
        :description: (str) description of the time entry
        :customFields: (arr of dict) each dict contains customFieldId,sourceType,value
        
    :return: details about the created time-entry
    :rtype: dict  
    """
    try:
        if "start" in params and "workspace_id" in params:
            time_entry = {}
            for key, value in params.items():
                time_entry[key] = value
            url = f"https://api.clockify.me/api/v1/workspaces/{params['workspace_id']}/time-entries/"
            headers = {"X-Api-Key": api_token, "Content-Type": "application/json"}
            response = requests.post(url, headers=headers, json=time_entry)
            if response.status_code in valid_status_code:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)
    
def Clockify_delete_time_entry(params, api_token):
    """
        Deletes a time-entry of a specific id.
    
    :param str api_token: (str,required) used for authentication purposes.
    :param dict params:
    
      :id: (str,required) the id of the time-entry to be deleted
      :workspace_id: (str,required) the workspace of the time-entry
    :return: details about the deleted time-entry(id,properties,..)
    :rtype: dict  
    """
    try:
        if "id" in params and "workspace_id" in params:
            api_url = f"https://api.clockify.me/api/v1/workspaces/{params['workspace_id']}/time-entries/{params['id']}"
            headers = {
                "X-Api-Key": api_token,
            }
            response = requests.delete(api_url, headers=headers)
            if response.status_code in valid_status_code:
                return f"Deleted time entry  with  ID: {params['id']}"
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def Clockify_update_time_entry(params, api_token):
    """
        Updates a time-entry with properties passed in the parameters
     
    :param str api_token: (str,required) used for authentication purposes
    :param dict params: contains specific properties to be added(or modified) to the time-entry.
    
        :id: (str,required) the id of the time entry to be updated
        :workspace_id: (str,required) the workspace of the time-entry
        :start: (string <date-time>) the start time of the time-entry
        :end: (string <date-time>) the end time of the time-entry
        :billable: (str) possible values are ACTIVE,DONE
        :projectId: (str)
        :tagIds: (arr of str) 
        :taskId: (str) 
        :description: (str) description of the time entry
        :customFields: (arr of dict) each dict contains customFieldId,sourceType,value
        
    :return: details about the updated time-entry
    :rtype: dict  
    """
    try:
        if "id" in params and "workspace_id" in params:
            time_entry = {}
            keys_to_skip = {"id"}
            for key, value in params.items():
                if key in keys_to_skip:
                    continue
                if value:
                    time_entry[key] = value
            url = f"https://api.clockify.me/api/v1/workspaces/{params['workspace_id']}/time-entries/{params['id']}"
            headers = {"X-Api-Key": api_token, "Content-Type": "application/json"}
            response = requests.put(url, headers=headers, json=time_entry)
            if response.status_code in valid_status_code:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def Clockify_get_time_entry(params, api_token):
    """
        Returns a time-entry of a specific id.
    
    :param str api_token: (str,required) used for authentication purposes.
    :param dict params:
    
      :id: (str,required) the id of the time-entry to be returned
      :workspace_id: (str,required) the workspace of the time-entry
    :return: details about the retrieved time-entry(id,properties,..)
    :rtype: dict  
    """
    try:
        if "id" in params and "workspace_id" in params:
            api_url = f"https://api.clockify.me/api/v1/workspaces/{params['workspace_id']}/time-entries/{params['id']}"
            headers = {
                "X-Api-Key": api_token,
            }
            response = requests.get(api_url, headers=headers)
            if response.status_code in valid_status_code:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)
