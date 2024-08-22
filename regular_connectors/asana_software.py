import asana
from asana.rest import ApiException
import json

def asana_get_many_project(cred,params):
    """
    Get multiple projects from Asana.

    :param str accessToken: Access token for authenticating with Asana API.
    :param dict params: Dictionary containing parameters.

        - :workspace: (str,required) - The workspace gid to filter projects on.
        - :team: (str,optional) - The team to filter projects on.
        - :archived: (bool,optional) - Only return projects whose archived field takes on the value of this parameter.

    Returns:
      list: A list of projects retrieved from Asana.

    """
    try:
        creds=json.loads(cred)
        if "workspace" in params and "accessToken" in creds:
            accessToken = creds["accessToken"]
            configuration = asana.Configuration()
            configuration.access_token = accessToken
            api_client = asana.ApiClient(configuration)
            projects_api_instance = asana.ProjectsApi(api_client)
            opts = {}
            for key, value in params.items():
                if value:
                    opts[key] = value
            api_response = projects_api_instance.get_projects(opts)
            projects = list(api_response)
            return projects
        else:
            raise Exception("Missing Input Data")
    except ApiException as e:
        raise Exception(json.loads(e.body))

def asana_get_project(cred,params):
    """
    Retrieve details of a specific project from Asana based on the provided project GID.

    :param str accessToken: Access token for authenticating with Asana API.
    :param dict params: Dictionary containing parameters.
    
        - :project_gid: (str,required) - Globally unique identifier for the project.

    Returns:
      dict: Details of the requested project.
    """

    try:
        creds=json.loads(cred)
        if "project_gid" in params and "accessToken" in creds:
            accessToken = creds["accessToken"]
            project_gid = params["project_gid"]
            configuration = asana.Configuration()
            configuration.access_token = accessToken
            api_client = asana.ApiClient(configuration)
            projects_api_instance = asana.ProjectsApi(api_client)
            opts = {}
            project = projects_api_instance.get_project(project_gid, opts)
            return project
        else:
            raise Exception("Missing Input Data")
    except ApiException as e:
        raise Exception(json.loads(e.body))


def asana_create_project(cred,params):
    """
    Create a project in Asana.

    :param str accessToken: Access token for authenticating with Asana API.
    :param dict params: Dictionary containing parameters.
    
        - :name: (str,required) - Name of the project to be created.
        - :workspace: (str,required) - The gid of a workspace.
        - :team: (str,required) - The team that this project is shared with.
        - :color: (str,optional) - Color of the project.
        - :due_on: (date,optional) - The day on which this project is due. This takes a date with format YYYY-MM-DD.
        - :notes: (str,optional) - Description of the project.

    Returns:
      dict: Details of the newly created project.

    """
    try:
        creds=json.loads(cred)
        if "name" in params and "workspace" in params and "team" in params and "accessToken" in creds:
            accessToken = creds["accessToken"]
            configuration = asana.Configuration()
            configuration.access_token = accessToken
            api_client = asana.ApiClient(configuration)
            projects_api_instance = asana.ProjectsApi(api_client)
            body_data = {}
            for key, value in params.items():
                body_data[key] = value
            body = {"data": body_data}
            opts = {}
            response = projects_api_instance.create_project(body, opts)
            return response
        else:
            raise Exception("Missing Input Data")
    except ApiException as e:
        raise Exception(json.loads(e.body))


def asana_update_project(cred,params):
    """
    Update an Asana project based on provided information.

    :param str accessToken: Access token for authenticating with Asana API.
    :param dict params: Dictionary containing parameters.
    
        - :project_gid: (str,required) - Globally unique identifier for the project.
        - :workspace: (str,required) - The gid of a workspace.
        - :name: (str,optional) - Name of the project .
        - :team: (str,optional) - The team that this project is shared with.
        - :color: (str,optional) - Color of the project.
        - :due_on: (date,optional) - The day on which this project is due. This takes a date with format YYYY-MM-DD.
        - :notes: (str,optional) - Description of the project.
        - :owner: (str,optional) - The current owner of the project.
        
    Returns:
      dict: Updated project information.

    """
    try:
        creds=json.loads(cred)
        if "project_gid" in params and "workspace" in params and "accessToken" in creds:
            accessToken = creds["accessToken"]
            project_gid = params["project_gid"]
            configuration = asana.Configuration()
            configuration.access_token = accessToken
            api_client = asana.ApiClient(configuration)
            projects_api_instance = asana.ProjectsApi(api_client)
            body_data = {}
            for key, value in params.items():
                skip_keys = ["project_gid"]
                if key in skip_keys:
                    continue
                if value:
                    body_data[key] = value
            body = {"data": body_data}
            opts = {}
            response = projects_api_instance.update_project(
                body, project_gid, opts)
            return response
        else:
            raise Exception("Missing Input Data")
    except ApiException as e:
        raise Exception(json.loads(e.body))


def asana_delete_project(cred,params):
    """
    Delete a project in Asana based on provided parameters.

    :param str accessToken: Access token for authenticating with Asana API.
    :param dict params: Dictionary containing parameters.
    
        - :project_gid: (str,required) - Globally unique identifier for the project.

    Returns:
      dict: A message confirming the deletion of the project.

    """
    try:
        creds=json.loads(cred)
        if "project_gid" in params and "accessToken" in creds:
            accessToken = creds["accessToken"]
            project_gid = params["project_gid"]
            configuration = asana.Configuration()
            configuration.access_token = accessToken
            api_client = asana.ApiClient(configuration)
            projects_api_instance = asana.ProjectsApi(api_client)
            projects_api_instance.delete_project(project_gid)
            return {"message": f"Deleted project with ID {project_gid}"}
        else:
            raise Exception("Missing Input Data")
    except ApiException as e:
        raise Exception(json.loads(e.body))


def asana_create_project_from_template(cred,params):
    """
    Create a new project in Asana based on a specified template.

    :param str accessToken: Access token for authenticating with Asana API.
    :param dict params: Dictionary containing parameters.
    

        - :name: (str,required) - The name of the new project.
        - :project_template_gid: (str,required) - Globally unique identifier for the project template.
        - :public: (bool,optional) - Sets the project to public to its team.

    Returns:
      dict: Information about the newly created project.
    """
    try:
        creds=json.loads(cred)
        if "project_template_gid" in params and "name" in params and "accessToken" in creds:
            accessToken = creds["accessToken"]
            project_template_gid = params["project_template_gid"]
            configuration = asana.Configuration()
            configuration.access_token = accessToken
            api_client = asana.ApiClient(configuration)
            project_templates_api_instance = asana.ProjectTemplatesApi(
                api_client)
            body_data = {
                "public": False,
            }
            for key, value in params.items():
                skip_keys = ["project_template_gid"]
                if key in skip_keys:
                    continue
                if value:
                    body_data[key] = value
            opts = {"body": {"data": body_data}}
            api_response = project_templates_api_instance.instantiate_project(
                project_template_gid, opts
            )
            return api_response
        else:
            raise Exception("Missing Input Data")
    except ApiException as e:
        raise Exception(json.loads(e.body))


def asana_create_task(cred,params):
    """
    Create a new task in Asana

    :param str accessToken: Access token for authenticating with Asana API.
    :param dict params: Dictionary containing parameters.
    
        - :name: (str,required) - Name of the task to be created.
        - :workspace: (str,required) - Gid of a workspace.
        - :assignee: (str,optional) -   Assignee ID for the task (gid of user).
        - :assignee_status: (str,optional) -   Assignee status for the task (Inbox, Today, Upcoming, Later).
        - :completed: (bool,optional) - Indicates if the task is completed or not.
        - :liked: (bool,optional) - Indicates if the task is liked or not.
        - :due_on: (date,optional) - Due date of the task (format: YYYY-MM-DD or null).
        - :notes: (str,optional) - Description of the task.
        - :projects: (array , optional) - Array of project IDs where the task will be added.

    Returns:
      dict: Information about the created task.

    """
    try:
        creds=json.loads(cred)
        if "name" in params and "workspace" in params and "accessToken" in creds:
            accessToken = creds["accessToken"]
            configuration = asana.Configuration()
            configuration.access_token = accessToken
            api_client = asana.ApiClient(configuration)
            tasks_api_instance = asana.TasksApi(api_client)
            body_data = {}
            for key, value in params.items():
                if value:
                    body_data[key] = value
            body = {"data": body_data}
            opts = {}
            api_response = tasks_api_instance.create_task(body, opts)
            return api_response
        else:
            raise Exception("Missing Input Data")
    except ApiException as e:
        raise Exception(json.loads(e.body))


def asana_get_task(cred,params):
    """
    Retrieve details of a specific task from Asana based on the provided task GID.

    :param str accessToken: Access token for authenticating with Asana API.
    :param dict params: Dictionary containing parameters.
    
        - :task_gid: (str,required) - Globally unique identifier for the task.

    Returns:
      dict: Details of the retrieved task.
    """
    try:
        creds=json.loads(cred)
        if "task_gid" in params and "accessToken" in creds:
            accessToken = creds["accessToken"]
            task_gid = params["task_gid"]
            configuration = asana.Configuration()
            configuration.access_token = accessToken
            api_client = asana.ApiClient(configuration)
            tasks_api_instance = asana.TasksApi(api_client)
            opts = {}
            api_response = tasks_api_instance.get_task(task_gid, opts)
            return api_response
        else:
            raise Exception("Missing Input Data")
    except ApiException as e:
        raise Exception(json.loads(e.body))


def asana_get_many_task(cred,params):
    """
    Retrieve multiple tasks from Asana based on specified parameters.

    :param str accessToken: Access token for authenticating with Asana API.
    :param dict params: Dictionary containing parameters.
    
        - :assignee: (str,optional) - The assignee to filter tasks on.*Note: If you specify `assignee`, you must also specify the `workspace` to filter on.*
        - :project: (str,optional) - The project to filter tasks on.
        - :section: (str,optional) - The section to filter tasks on.
        - :workspace: (str,optional) - The workspace to filter tasks on.
            *Note: If you specify `workspace`, you must also specify the `assignee` to filter on.*
        - :completed_since: (datetime,optional) - Only return tasks that are either incomplete or that have been completed since this time. 
        - :modified_since: (datetime,optional) - Only return tasks that have been modified since the given time. 

    Returns:
      list: List of tasks retrieved.
    """

    try:
        creds=json.loads(cred)
        if "accessToken" in creds:
            accessToken = creds["accessToken"]
            configuration = asana.Configuration()
            configuration.access_token = accessToken
            api_client = asana.ApiClient(configuration)
            tasks_api_instance = asana.TasksApi(api_client)
            opts = {}
            for key, value in params.items():
                if value:
                    opts[key] = value
            api_response = tasks_api_instance.get_tasks(opts)
            tasks = list(api_response)
            return tasks
        else:
            raise Exception("Missing Input Data")
    except ApiException as e:
        raise Exception(json.loads(e.body))


def asana_update_task(cred,params):
    """
    Update an Asana task based on provided information.

    :param str accessToken: Access token for authenticating with Asana API.
    :param dict params: Dictionary containing parameters.

        - :task_gid: (str,required) - Globally unique identifier for the task.
        - :name: (str,optional) - Name of the task to be updated.
        - :assignee: (str,optional) - Assignee ID for the task (gid of user).
        - :assignee_status: (str,optional) - Assignee status for the task (Inbox, Today, Upcoming, Later).
        - :completed: (bool,optional) - Indicates if the task is completed or not.
        - :liked: (bool,optional) - Indicates if the task is liked or not.
        - :due_on: (date,optional) : Due date of the task (format: YYYY-MM-DD or null).
        - :notes: (str,optional) - Description of the task.

    Returns:
        dict: Updated task information.

    """
    try:
        creds=json.loads(cred)
        if "task_gid" in params and "accessToken" in creds:
            accessToken = creds["accessToken"]
            task_gid = params["task_gid"]
            configuration = asana.Configuration()
            configuration.access_token = accessToken
            api_client = asana.ApiClient(configuration)
            tasks_api_instance = asana.TasksApi(api_client)
            body_data = {}
            for key, value in params.items():
                skip_keys = ["task_gid"]
                if key in skip_keys:
                    continue
                if value:
                    body_data[key] = value
            body = {"data": body_data}
            opts = {}
            api_response = tasks_api_instance.update_task(body, task_gid, opts)
            return api_response
        else:
            raise Exception("Missing Input Data")
    except ApiException as e:
        raise Exception(json.loads(e.body))


def asana_delete_task(cred,params):
    """
    Delete a task in Asana based on provided parameters.

    :param str accessToken: Access token for authenticating with Asana API.
    :param dict params: Dictionary containing parameters.
    
        :task_gid: (str,required) - Globally unique identifier for the task.

    Returns:
      dict: A message confirming the deletion of the task.

    """
    try:
        creds=json.loads(cred)
        if "task_gid" in params and "accessToken" in creds:
            accessToken = creds["accessToken"]
            task_gid = params["task_gid"]
            configuration = asana.Configuration()
            configuration.access_token = accessToken
            api_client = asana.ApiClient(configuration)
            tasks_api_instance = asana.TasksApi(api_client)
            tasks_api_instance.delete_task(task_gid)
            return {"message": f"Deleted project with ID {task_gid}"}
        else:
            raise Exception("Missing Input Data")
    except ApiException as e:
        raise Exception(json.loads(e.body))


def asana_search_task(cred,params):
    """
    Search for tasks in Asana based on specified parameters.

    :param str accessToken: Access token for authenticating with Asana API.
    :param dict params: Dictionary containing parameters.
    
        - :workspace_gid: (str,required) - Globally unique identifier for the workspace or organization.
        - :text: (str,optional) - Performs full-text search on both task name and description
        - :completed: (bool,optional) - Filter to completed tasks

    Returns:
        list: List of tasks matching the search query.
    """
    try:
        creds=json.loads(cred)
        if "workspace_gid" in params and "accessToken" in creds:
            accessToken = creds["accessToken"]
            workspace_gid = params["workspace_gid"]
            configuration = asana.Configuration()
            configuration.access_token = accessToken
            api_client = asana.ApiClient(configuration)
            tasks_api_instance = asana.TasksApi(api_client)
            opts = {"completed": False}
            for key, value in params.items():
                skip_keys = ["workspace_gid"]
                if key in skip_keys:
                    continue
                if value:
                    opts[key] = value
            api_response = tasks_api_instance.search_tasks_for_workspace(
                workspace_gid, opts
            )
            tasks = list(api_response)
            return tasks
        else:
            raise Exception("Missing Input Data")
    except ApiException as e:
        raise Exception(json.loads(e.body))


def asana_duplicate_task(cred,params):
    """
    Duplicate a task in Asana.

    :param str accessToken: Access token for authenticating with Asana API.
    :param dict params: Dictionary containing parameters.
    
        - :task_gid: (str,required) - Globally unique identifier for the task to be duplicated.
        - :name: (str,required) - Name for the new duplicated task.
        - :include: (str,optional) - A comma-separated list of fields to be duplicated to the new task . 

            Available options for 'include' fields: assignee-attachments-dates-dependencies-followers-notes-parent-projects-subtasks-tags

    Returns:
        dict: Details of the duplicated task.
    """
    try:
        creds=json.loads(cred)
        if "task_gid" in params and "name" in params and "accessToken" in creds:
            accessToken = creds["accessToken"]
            task_gid = params["task_gid"]
            configuration = asana.Configuration()
            configuration.access_token = accessToken
            api_client = asana.ApiClient(configuration)
            tasks_api_instance = asana.TasksApi(api_client)
            body_data = {}
            for key, value in params.items():
                if value:
                    body_data[key] = value
            body = {"data": body_data}
            opts = {}
            api_response = tasks_api_instance.duplicate_task(
                body, task_gid, opts)
            return api_response
        else:
            raise Exception("Missing Input Data")
    except ApiException as e:
        raise Exception(json.loads(e.body))


def asana_upload_file_task(cred,params):
    """
    Upload a file to a task.

    :param str accessToken: Access token for authenticating with Asana API.
    :param dict params: Dictionary containing parameters.
    
        - :parent: (str,required) - Identifier of the parent task,
        - :url: (str,required) - The URL of the external resource being attached. 
        - :name: (str,required) - The name of the external resource being attached.

    Returns:
        dict: Details of the uploaded file attachment.
    """
    try:
        creds=json.loads(cred)
        if "parent" in params and "url" in params and "name" in params and "accessToken" in creds:
            accessToken = creds["accessToken"]
            configuration = asana.Configuration()
            configuration.access_token = accessToken
            api_client = asana.ApiClient(configuration)
            attachments_api_instance = asana.AttachmentsApi(api_client)
            opts = {
                "resource_subtype": "external",
            }
            for key, value in params.items():
                if value:
                    opts[key] = value
            api_response = attachments_api_instance.create_attachment_for_object(
                opts)
            return api_response
        else:
            raise Exception("Missing Input Data")
    except ApiException as e:
        raise Exception(json.loads(e.body))


def asana_get_user(cred,params):
    """
    Retrieve details of a user from Asana

    :param str accessToken: Access token for authenticating with Asana API.
    :param dict params: Dictionary containing parameters.
    
        - :user_gid: (str,required) - Globally unique identifier for the user.

    Returns:
        dict: Details of the user.
    """
    try:
        creds=json.loads(cred)
        if "user_gid" in params and "accessToken" in creds:
            accessToken = creds["accessToken"]
            user_gid = params["user_gid"]
            configuration = asana.Configuration()
            configuration.access_token = accessToken
            api_client = asana.ApiClient(configuration)
            users_api_instance = asana.UsersApi(api_client)
            opts = {}
            api_response = users_api_instance.get_user(user_gid, opts)
            return api_response
    except ApiException as e:
        raise Exception(json.loads(e.body))


def asana_get_many_user(cred,params):
    """
    Retrieve multiple users from Asana within a specified workspace.

    :param str accessToken: Access token for authenticating with Asana API.
    :param dict params: Dictionary containing parameters.
    
        - :workspace_gid: (str,required) - Globally unique identifier for the workspace or organization.

    Returns:
        list: List of users within the specified workspace.
    """
    try:
        creds=json.loads(cred)
        if "workspace_gid" in params and "accessToken" in creds:
            accessToken = creds["accessToken"]
            workspace_gid = params["workspace_gid"]
            configuration = asana.Configuration()
            configuration.access_token = accessToken
            api_client = asana.ApiClient(configuration)
            users_api_instance = asana.UsersApi(api_client)
            opts = {}
            api_response = users_api_instance.get_users_for_workspace(
                workspace_gid, opts)
            users = list(api_response)
            return users
        else:
            raise Exception("Missing Input Data")
    except ApiException as e:
        raise Exception(json.loads(e.body))

def asana_create_section_project(cred,params):
    """
    Create a section within a project in Asana.

    :param str accessToken: Access token for authenticating with Asana API.
    :param dict params: Dictionary containing parameters.
    
        - :project_gid: (str,required) - Globally unique identifier for the project.
        - :name: (str,required) - Name for the new section.
        - :insert_before: (str,optional) - An existing section within this project before which the added section should be inserted.
        - :insert_after: (str,optional) - An existing section within this project after which the added section should be inserted. Cannot be provided together with insert_before.

    Returns:
        dict: Details of the created section.
    """
    try:
        creds=json.loads(cred)
        if "project_gid" in params and "name" in params and "accessToken" in creds:
            accessToken = creds["accessToken"]
            project_gid = params["project_gid"]
            configuration = asana.Configuration()
            configuration.access_token = accessToken
            api_client = asana.ApiClient(configuration)
            sections_api_instance = asana.SectionsApi(api_client)
            body_data = {}
            for key, value in params.items():
                skip_keys = ["project_gid"]
                if key in skip_keys:
                    continue
                if value:
                    body_data[key] = value
            opts = {
                "body": {"data": body_data},
            }
            api_response = sections_api_instance.create_section_for_project(
                project_gid, opts)
            return api_response
        else:
            raise Exception("Missing Input Data")
    except ApiException as e:
        raise Exception(json.loads(e.body))

def asana_get_section_project(cred,params):
    """
    Retrieve sections within a project in Asana

    :param str accessToken: Access token for authenticating with Asana API.
    :param dict params: Dictionary containing parameters.
     
        - :project_gid: (str,required) - Globally unique identifier for the project.

    Returns:
        list: List of sections within the specified project.
    """
    try:
        creds=json.loads(cred)
        if "project_gid" in params and "accessToken" in creds:
            accessToken = creds["accessToken"]
            project_gid = params["project_gid"]
            configuration = asana.Configuration()
            configuration.access_token = accessToken
            api_client = asana.ApiClient(configuration)
            sections_api_instance = asana.SectionsApi(api_client)
            opts = {}
            api_response = sections_api_instance.get_sections_for_project(
                project_gid, opts)
            sections = list(api_response)
            return sections
        else:
            raise Exception("Missing Input Data")
    except ApiException as e:
        raise Exception(json.loads(e.body))
    

def asana_move_task_to_section(cred,params):
    """
    Move a task to a specific section within a project in Asana.

    :param str accessToken: Access token for authenticating with Asana API.
    :param dict params: Dictionary containing parameters.
    
        - :section_gid: (str,required) - Globally unique identifier for the section.
        - :task: (str,required) - The task to add to this section.
             
    Returns:
        dict: A message confirming the moving of the task.
    """
    try:
        creds=json.loads(cred)
        if "section_gid" in params and "task" in params and "accessToken" in creds:
            accessToken = creds["accessToken"]
            section_gid = params["section_gid"]
            configuration = asana.Configuration()
            configuration.access_token = accessToken
            api_client = asana.ApiClient(configuration)
            sections_api_instance = asana.SectionsApi(api_client)
            body_data = {}
            for key, value in params.items():
                skip_keys = ["section_gid"]
                if key in skip_keys:
                    continue
                if value:
                    body_data[key] = value
            opts = {
                "body": {"data": body_data},
            }
            sections_api_instance.add_task_for_section(section_gid, opts)
            return {"message": f"Successfully Moved the task"}
        else:
            raise Exception("Missing Input Data")
    except ApiException as e:
        raise Exception(json.loads(e.body))
    

def asana_add_project_for_task(cred,params):
    """
    Add a project to a task in Asana.

    :param str accessToken: Access token for authenticating with Asana API.
    :param dict params: Dictionary containing parameters.
    
        - :task_gid: (str,required) - Globally unique identifier for the task.
        - :project: (str,required) - The project to add the task to.
        - :section: (str,optional) - A section in the project to insert the task into
        - :insert_after: (str,optional) - A task in the project to insert the task after.
        - :insert_before: (str,optional) - A task in the project to insert the task before.

    Returns:
        dict: A message confirming the addition of the project to the task.
    """
    try:
        creds=json.loads(cred)
        if "task_gid" in params and "project" in params and "accessToken" in creds:
            accessToken = creds["accessToken"]
            insert_after = params.get("insert_after")
            insert_before = params.get("insert_before")
            section = params.get("section")
            provided_params = [param for param in (
                insert_after, insert_before, section) if param is not None]
            if len(provided_params) < 1 or len(provided_params) == 1:
                task_gid = params["task_gid"]
                configuration = asana.Configuration()
                configuration.access_token = accessToken
                api_client = asana.ApiClient(configuration)
                tasks_api_instance = asana.TasksApi(api_client)
                body_data = {}
                for key, value in params.items():
                    skip_keys = ["task_gid"]
                    if key in skip_keys:
                        continue
                    if value:
                        body_data[key] = value
                body = {"data": body_data}
                tasks_api_instance.add_project_for_task(body, task_gid)
                return {"message": f"Successfully added the specified project to the task."}
            else:
                raise Exception(
                    "You can specify at most one of insert_after, insert_before, or section.")
        else:
            raise Exception("Missing Input Data")
    except ApiException as e:
        raise Exception(json.loads(e.body))


def asana_remove_project_for_task(cred,params):
    """
    Remove a project from a task in Asana.

    :param str accessToken: Access token for authenticating with Asana API.
    :param dict params: Dictionary containing parameters.
    
        - :task_gid: (str,required) - Globally unique identifier for the task.
        - :project: (str,required) - The project to remove the task from.

    Returns:
        dict: A message confirming the removal of the project from the task.
   
    """
    try:
        creds=json.loads(cred)
        if "task_gid" in params and "project" in params and "accessToken" in creds:
            accessToken = creds["accessToken"]
            task_gid = params["task_gid"]
            configuration = asana.Configuration()
            configuration.access_token = accessToken
            api_client = asana.ApiClient(configuration)
            tasks_api_instance = asana.TasksApi(api_client)
            body_data = {}
            for key, value in params.items():
                skip_keys = ["task_gid"]
                if key in skip_keys:
                    continue
                if value:
                    body_data[key] = value
            body = {"data": body_data}
            tasks_api_instance.remove_project_for_task(body, task_gid)
            return {"message": f"Successfully removed the specified project from the task."}
        else:
            raise Exception("Missing Input Data")
    except ApiException as e:
        raise Exception(json.loads(e.body))


def asana_get_tasks_for_project(cred,params):
    """
    Retrieve tasks associated with a specific project in Asana

    :param str accessToken: Access token for authenticating with Asana API.
    :param dict params: Dictionary containing parameters.
    
        - :project_gid: (str,required) - Globally unique identifier for the project.
        - :completed_since: (datetime,optional) - Only return tasks that are either incomplete or that have been completed since this time. 
        
    Returns:
        list: List of tasks associated with the specified project.
    """
    try:
        creds=json.loads(cred)
        if "project_gid" in params and "accessToken" in creds:
            accessToken = creds["accessToken"]
            project_gid = params["project_gid"]
            configuration = asana.Configuration()
            configuration.access_token = accessToken
            api_client = asana.ApiClient(configuration)
            tasks_api_instance = asana.TasksApi(api_client)
            opts = {}
            for key, value in params.items():
                skip_keys = ["project_gid"]
                if key in skip_keys:
                    continue
                if value:
                    opts[key] = value
            api_response = tasks_api_instance.get_tasks_for_project(
                project_gid, opts)
            tasks = list(api_response)
            return tasks
        else:
            raise Exception("Missing Input Data")
    except ApiException as e:
        raise Exception(json.loads(e.body))


def asana_create_subtask(cred,params):
    """
    Create a new subtask in Asana

    :param str accessToken: Access token for authenticating with Asana API.
    :param dict params: Dictionary containing parameters.
    
        - :task_gid: (str,required) - Globally unique identifier for the task.
        - :name: (str,required) - Name of the task.
        - :workspace: (str,required) - Gid of a workspace.
        - :assignee: (str,optional) - Gid of a user.
        - :assignee_status: (str,optional) - Assignee status for the task (Inbox, Today, Upcoming, Later).
        - :completed: (bool,optional) - Indicates if the task is completed or not.
        - :liked: (bool,optional) - Indicates if the task is liked or not.
        - :due_on: (date,optional) - Due date of the task (format: YYYY-MM-DD or null).
        - :notes: (str,optional) - Description of the task.

    Returns:
      dict: Information about the created subtask.

    """
    try:
        creds=json.loads(cred)
        if "task_gid" in params and "name" in params and "accessToken" in creds:
            accessToken = creds["accessToken"]
            task_gid = params["task_gid"]
            configuration = asana.Configuration()
            configuration.access_token = accessToken
            api_client = asana.ApiClient(configuration)
            tasks_api_instance = asana.TasksApi(api_client)
            body_data = {}
            for key, value in params.items():
                skip_keys = ["task_gid"]
                if key in skip_keys:
                    continue
                if value:
                    body_data[key] = value
            body = {"data": body_data}
            opts = {}
            api_response = tasks_api_instance.create_subtask_for_task(
                body, task_gid, opts)
            return api_response
        else:
            raise Exception("Missing Input Data")
    except ApiException as e:
        raise Exception(json.loads(e.body))
    
def asana_get_many_subtask(cred,params):
    """
    Retrieve subtasks of a task in Asana.

    :param str accessToken: Access token for authenticating with Asana API.
    :param dict params: Dictionary containing parameters.
    
        - :task_gid: (str,required) - Globally unique identifier for the task.

    Returns:
        list: List of subtasks belonging to the specified task.
    """
    try:
        creds=json.loads(cred)
        if "task_gid" in params and "accessToken" in creds:
            accessToken = creds["accessToken"]
            task_gid = params["task_gid"]
            configuration = asana.Configuration()
            configuration.access_token = accessToken
            api_client = asana.ApiClient(configuration)
            tasks_api_instance = asana.TasksApi(api_client)
            opts = {}
            api_response = tasks_api_instance.get_subtasks_for_task(
                task_gid, opts)
            subtasks = list(api_response)
            return subtasks
        else:
            raise Exception("Missing Input Data")
    except ApiException as e:
        raise Exception(json.loads(e.body))

def asana_add_task_comment(cred,params):
    """
    Add a comment to a task in Asana.

    :param str accessToken: Access token for authenticating with Asana API.
    :param dict params: Dictionary containing parameters.
    
        - :task_gid: (str,required) - Globally unique identifier for the task.
        - :text: (str,optional) - The plain text of the comment to add.
        - :html_text: (str,optional) - HTML formatted text for a comment. e.g <body>This is a comment.</body> 
        - :is_pinned: (bool,optional) - Conditional. Whether the story should be pinned on the resource.

    Returns:
        dict: Details of the added comment.
    """
    try:
        creds=json.loads(cred)
        if "task_gid" in params and "accessToken" in creds:
            accessToken = creds["accessToken"]
            if "text" in params or "html_text" in params:
                task_gid = params["task_gid"]
                configuration = asana.Configuration()
                configuration.access_token = accessToken
                api_client = asana.ApiClient(configuration)
                stories_api_instance = asana.StoriesApi(api_client)
                body_data = {}
                for key, value in params.items():
                    skip_keys = ["task_gid"]
                    if key in skip_keys:
                        continue
                    if value:
                        body_data[key] = value
                body = {"data": body_data}
                opts = {}
                api_response = stories_api_instance.create_story_for_task(
                    body, task_gid, opts)
                return api_response
            else:
                raise Exception(
                    "Must specify either text or html_text of comment")
        else:
            raise Exception("Missing Input Data")
    except ApiException as e:
        raise Exception(json.loads(e.body))


def asana_remove_task_comment(cred,params):
    """
    remove a comment to a task in Asana.

    :param str accessToken: Access token for authenticating with Asana API.
    :param dict params: Dictionary containing parameters.
    
        - :story_gid: (str,required) - Globally unique identifier for the story.

    Returns:
       dict: A message confirming the deletion of the comment.
    """
    try:
        creds=json.loads(cred)
        if "story_gid" in params and "accessToken" in creds:
            accessToken = creds["accessToken"]
            story_gid = params["story_gid"]
            configuration = asana.Configuration()
            configuration.access_token = accessToken
            api_client = asana.ApiClient(configuration)
            stories_api_instance = asana.StoriesApi(api_client)
            stories_api_instance.delete_story(story_gid)
            return {"message": f"Successfully deleted the specified comment."}
        else:
            raise Exception("Missing Input Data")
    except ApiException as e:
        raise Exception(json.loads(e.body))

