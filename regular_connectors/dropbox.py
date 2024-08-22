import requests,json
import base64


def dropbox_create_access_token(creds):
    """
       Creates an access token that will be used for authorization purposes.
    
    :param str app_key: (str,required) used for authentication
    :param str app_secret: (str,required) for the calendar, it's 'calendar'
    :param str refresh_token: (str,required) the version used is v3  
    :return: access token 
    :rtype: dict  
    """
    credential = json.loads(creds)
    refresh_token = credential['refreshToken']
    app_key = credential['appKey']
    app_secret = credential['appSecret']
    data = {
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }
    auth_header = base64.b64encode(f"{app_key}:{app_secret}".encode()).decode('utf-8')
    headers = {
        "Authorization": f"Basic {auth_header}",
    }
    try:
        response = requests.post("https://api.dropbox.com/oauth2/token", data=data, headers=headers)
        response_data = response.json()
        if response.status_code == 200:
            new_access_token = response_data["access_token"]
            return new_access_token
        else:
            return f"Error: {response_data.get('error_description')}"
    except Exception as e:
         raise Exception(e)
     
     
     
####################################### Folder Operations #######################################
     


def dropbox_create_folder(access_token,params):
    """
     Creates a dropbox folder with custom properties if added

    :param str access_token: (str, required) Used for authentication.
    :param dict params: contains properties to be added to the created folder
    
        - :path: (str, Required) Path in the user's Dropbox to create.
        - :autorename: (bool) If there's a conflict, have the Dropbox server try to autorename the
                  folder to avoid the conflict.
    :return: Details about the created folder
    :rtype: dict
    """
    try:
        if 'path' in params:
            create_folder_url = "https://api.dropboxapi.com/2/files/create_folder_v2"
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
        
            response = requests.post(create_folder_url, headers=headers, json=params)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.text) 
        else:
            raise Exception("missing folder path") 
    except Exception as e:
        raise Exception(e)

def dropbox_list_folder(access_token,params):
    """
    Returns the contents of a folder.

    :param str access_token: (str, required) Used for authentication.
    :param dict params: Filters the properties to be returned for each event.

        - :path: (str, Required) A unique identifier for the file.
        - :include_deleted: (bool) If true, the results will include entries for files and folders
                            that used to exist but were deleted.
        - :include_has_explicit_shared_members: (bool) a flag for each file indicating whether that
                                                file has any explicit members.
        - :include_mounted_folders: (bool) includes entries under mounted folders,which
                                    includes app folders, shared folders, and team folders.
        - :include_non_downloadable_files: (bool) includes files that are not downloadable.
        - :recursive: (bool) If true, the list folder operation will be applied recursively to all
                    subfolders, and the response will contain contents of all subfolders.

    :return: Details about the folder content.
    :rtype: dict
    """
    try:
        if 'path' in params:
            copy_folder_url = "https://api.dropboxapi.com/2/files/list_folder"
            headers = {'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'}
            response = requests.post(copy_folder_url, headers=headers, json=params)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.text)
        else:
            raise Exception("missing folder path")
    except Exception as e:
        raise Exception(e)

def dropbox_copy_folder(access_token,params):
    """
     Copies a folder to a different location in the user's Dropbox

    :param str access_token: (str, required) Used for authentication.
    :param dict params: Filters the properties to be returned for each event.
    
        - :from_path: (str, Required) Path in the user's Dropbox to be copied or moved.
        - :to_path: (str, Required) Path in the user's Dropbox that is the destination
        - :allow_ownership_transfer: (bool) Allow moves by owner even if it would
                                       result in an ownership transfer 
                                       for the content being moved
        - :autorename: (bool) If there's a conflict, have the Dropbox server 
                               try to autorename the file to avoid the conflict
    :return: Details about the copied folder
    :rtype: dict
    """
    try:
        if 'from_path' in params and 'to_path' in params:
            copy_folder_url = "https://api.dropboxapi.com/2/files/copy_v2"
            headers = {'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'}
            response = requests.post(copy_folder_url, headers=headers, json=params)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.text)
        else:
            raise Exception("missing required data")
    except Exception as e:
        raise Exception(e)

def dropbox_move_folder(access_token,params):
    """
     Moves a  folder to a different location in the user's Dropbox

    :param str access_token: (str, required) Used for authentication.
    :param dict params: Filters the properties to be returned for each event.
    
        - :from_path: (str, Required) Path in the user's Dropbox to be moved.
        - :to_path: (str, Required) Path in the user's Dropbox that is the destination
        - :allow_ownership_transfer: (bool) Allow moves by owner even if it would
                                       result in an ownership transfer 
                                       for the content being moved
        - :autorename: (bool) If there's a conflict, have the Dropbox server 
                               try to autorename the file to avoid the conflict
    :return: Details about the copied folder
    :rtype: dict
    """
    try:
        if 'from_path' in params and 'to_path' in params:
            move_folder_url = "https://api.dropboxapi.com/2/files/move_v2"
            headers = {'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'}
            response = requests.post(move_folder_url, headers=headers, json=params)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.text)
        else:
            raise Exception("missing required data")
    except Exception as e:
        raise Exception(e)

def dropbox_delete_folder(access_token,params):
    """
     Deletes a folder at a given path with all its contents
    :param str access_token: (str, required) Used for authentication.
    :param dict params: Filters the properties to be returned for each event.
    
        - :path: (str, Required) Path in the user's Dropbox to delete.
    :return: Details about the deleted folder
    :rtype: dict
    """
    try:
        if 'path' in params:
            delete_folder_url = "https://api.dropboxapi.com/2/files/delete_v2"
            headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
            response = requests.post(delete_folder_url, headers=headers, json=params)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.text)
        else:
            raise Exception("missing folder path")
    except Exception as e:
        raise Exception(e)
    

##################################### File Operations #####################################

def dropbox_copy_file(access_token,params):
    """
     Copies a file to a different location in the user's Dropbox

    :param str access_token: (str, required) Used for authentication.
    :param dict params: Filters the properties to be returned for each event.
    
        - :from_path: (str, Required) Path in the user's Dropbox to be copied or moved.
        - :to_path: (str, Required) Path in the user's Dropbox that is the destination
        - :allow_ownership_transfer: (bool) Allow moves by owner even if it would
                                       result in an ownership transfer 
                                       for the content being moved
        - :autorename: (bool) If there's a conflict, have the Dropbox server 
                               try to autorename the file to avoid the conflict
    :return: Details about the copied file
    :rtype: dict
    """
    try:
        if 'from_path' in params and 'to_path' in params:
            copy_folder_url = "https://api.dropboxapi.com/2/files/copy_v2"
            headers = {'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'}
            response = requests.post(copy_folder_url, headers=headers, json=params)
            if response.status_code == 200:
             return response.json()
            else:
             raise Exception(response.text)
        else:
            raise Exception("missing required data")
        
    except Exception as e:
        raise Exception(e)

def dropbox_move_file(access_token,params):
    """
     Moves a  file to a different location in the user's Dropbox

    :param str access_token: (str, required) Used for authentication.
    :param dict params: Filters the properties to be returned for each event.
    
        - :from_path: (str, Required) Path in the user's Dropbox to be moved.
        - :to_path: (str, Required) Path in the user's Dropbox that is the destination
        - :allow_ownership_transfer: (bool) Allow moves by owner even if it would
                                       result in an ownership transfer 
                                       for the content being moved
        - :autorename: (bool) If there's a conflict, have the Dropbox server 
                               try to autorename the file to avoid the conflict
    :return: Details about the copied file
    :rtype: dict
    """
    try:
        if 'from_path' in params and 'to_path' in params:
            move_file_url = "https://api.dropboxapi.com/2/files/move_v2"
            headers = {'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'}
            response = requests.post(move_file_url, headers=headers, json=params)
            if response.status_code == 200:
             return response.json()
            else:
             raise Exception(response.text)
        else:
            raise Exception("missing required data")
    except Exception as e:
        raise Exception(e)

def dropbox_delete_file(access_token,params):
    """
     Deletes a file at a given path.
    :param str access_token: (str, required) Used for authentication.
    :param dict params: Filters the properties to be returned for each event.
    
        - :path: (str, Required) Path in the user's Dropbox to delete.
    :return: Details about the deleted file
    :rtype: dict
    """
    try:
        if 'path' in params:
            delete_folder_url = "https://api.dropboxapi.com/2/files/delete_v2"
            headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
            response = requests.post(delete_folder_url, headers=headers, json=params)
            if response.status_code == 200:
             return response.json()
            else:
             raise Exception(response.text)
        else:
            raise Exception("missing file path")
    except Exception as e:
        raise Exception(e)

def dropbox_get_file_metadata(access_token,params):
    
    '''
    Retrieves metadata for a file at a given path in the user's Dropbox.

    :param str access_token: (str, required) Used for authentication to the Dropbox API.
    :param dict params: (str, Required) A dictionary containing the file path and actions to be returned.

        - :path: (str,required) Path in the user's Dropbox from which to retrieve file metadata.
        
    :return: Metadata details about the file.
    :rtype: dict
    
    '''
    
    
    try:
        if "file" in params:
            file_metadata_url = "https://api.dropboxapi.com/2/sharing/get_file_metadata"
            headers  ={
                "Authorization":f"Bearer {access_token}",
                "Content-Type":"application/json",
            }
            response = requests.post(url=file_metadata_url,headers=headers,json=params)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.text)
        else:
            raise Exception("Missing file path")     
    except Exception as e:
        raise Exception(e)
    
    
def dropbox_upload_file(access_token,params):
    
    '''
    Uploads a file to Dropbox.

    :param str access_token: (str, required) The OAuth 2 access token for authenticating the API request.
    :param dict params: (dict, required) Parameters for the upload operation.

        - :file_content: (str, required) The file content to upload, encoded in base64.
        - :path: (str, required) The path in Dropbox where the file will be uploaded.
        - :mode: (str, optional) Selects what to do if the file already exists. Default is 'add'.
        - :autorename: (bool, optional) If there's a conflict, have Dropbox automatically rename the file. Default is False.
        - :mute: (bool, optional) Normally, users are notified of file modifications. This will cause notifications not to be generated. Default is False.
        - :strict_conflict: (bool, optional) Be more strict about how each 'write' request is processed. Default is False.

    :return: A dictionary containing metadata about the uploaded file if the upload is successful.
    :rtype: dict
    '''
    
    try:
            upload_file_url = "https://content.dropboxapi.com/2/files/upload"
            _, encoded = params['file_content'].split(",", 1)
            file_data = base64.b64decode(encoded)
            upload_args = {}
            for key,value in params.items():
                if key != "file_content":
                    upload_args[key]= value
            # Parse dictionary as string as Dropbox api expects
            json_string = json.dumps(upload_args)
            headers = {
                "Authorization":f"Bearer {access_token}",
                "Content-Type":"application/octet-stream",
                "Dropbox-API-Arg":json_string
            }
            response = requests.post(url=upload_file_url,headers=headers,files={"upload_file":file_data})
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"An error occured: {response.text}")
    except Exception as e:
        raise Exception(e)


##################################### Shared Link Operation #####################################

def dropbox_create_shared_link_with_settings(access_token,params):
    
    '''
    Creates a shared link for a Dropbox file or folder.
    :param str access_token: (str, required) Used for authentication to the Dropbox API.
    :param dict params: (str, Required) A dictionary containing the file path.

      -  :path: (str,required) The path to the file or folder you want to share.
        
    :return: An dictionary containing information about the created shared link.
    :rtype: dict
    
    '''   
    try:
        if "path" in params:
            shared_link_url ="https://api.dropboxapi.com/2/sharing/create_shared_link_with_settings"
            headers = {
                "Authorization":f"Bearer {access_token}",
                "Content-Type":"application/json",
            }
            response = requests.post(url=shared_link_url,headers=headers,json=params)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"An Error Occured: {response.text}")
        else:
            raise Exception("Missing file path")
    except Exception as e:
        raise Exception(e)
