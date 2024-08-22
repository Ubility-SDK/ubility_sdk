import requests
import json
import base64

status = [200, 201, 202, 204, 206, 207, 208]


def onedrive_refresh_access_token(creds):
    try:
        cred=json.loads(creds)
        token_endpoint="https://login.microsoftonline.com/common/oauth2/v2.0/token"
        request_body = {
            'client_id': cred['clientId'],
            'client_secret': cred['clientSecret'],
            'scope': ' '.join(['https://graph.microsoft.com/.default'] +['offline_access']),
            'refresh_token': cred['refreshToken'],
            'grant_type': 'refresh_token',
        }
        response = requests.post(token_endpoint, data=request_body)
        response_json = response.json()
        if "access_token" in response_json:
            return response_json["access_token"]
        else:
            return {"access_token": "Invalid access_token"}
    except Exception as error:
        raise Exception(error)

################################################################################################################

def onedrive_get_file(access_token, params):
    """
    Retrieve a file from OneDrive using the Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :file_id: (str,required) - ID of the file to be retrieved.

    Returns:
        dict: Details of the retrieved file.
    """
    try:
        if "file_id" in params:
            file_id = params["file_id"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}"
            headers = {
                "Authorization": "Bearer " + access_token
            }
            response = requests.get(url=graph_api_url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)



def onedrive_copy_file(access_token, params):
    """
    Asynchronously creates a copy of an driveItem (including any children), under a new parent item or with a new name. using the Graph API

    :accessToken: Access token String for authentication with Microsoft Graph API.
    :params: Dictionary containing parameters.

    - :file_id: (str,required) - ID of the file to be copied.
    - :name: (str,optional) - The new name for the copy. If this isn't provided, the same name will be used as the original.
    - :parentReference: (dict,required) - dictionary containing information about the parent destination for the copy operation
    
        - :driveId: (str,optional) - Unique identifier of the drive instance that contains the driveItem.
        - :driveType: (str,optional) - Identifies the type of drive.
        - :id: (str,optional) - Unique identifier of the driveItem in the drive or a listItem in a list.
        - :name: (str,optional) - The name of the item being referenced.
        - :path: (str,optional) - Path that can be used to navigate to the item.
        - :shareId: (str,optional) - A unique identifier for a shared resource that can be accessed via the `Shares <https://learn.microsoft.com/en-us/graph/api/shares-get?view=graph-rest-1.0>`_ API.
        - :siteId: (str,optional) - For OneDrive for Business and SharePoint, this property represents the ID of the site that contains the parent document library of the driveItem resource or the parent list of the listItem resource. The value is the same as the id property of that `site <https://learn.microsoft.com/en-us/graph/api/resources/site?view=graph-rest-1.0>`_ resource. It is an `opaque string that consists of three identifiers <https://learn.microsoft.com/en-us/graph/api/resources/site
        - :sharepointIds: (dict,optional) - Returns identifiers useful for SharePoint REST compatibility. 
        
            - :listId: (str,optional) - The unique identifier (guid) for the item's list in SharePoint.

    Returns:
        dict: Confirmation message after successful copying.
    """
    try:
        if "file_id" in params:
            file_id = params["file_id"]
            parentReference = params.get("parentReference", {})
            name = params.get("name", "")
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/copy"
            headers = {
                "Authorization": "Bearer " + access_token,
                "Content-type": "application/json"
            }
            data = {}
            if parentReference:
                data["parentReference"] = parentReference
            if name:
                data["name"] = name
            response = requests.post(
                url=graph_api_url, headers=headers, json=data)
            if response.status_code == 202:
                return {
                    "message": "File copied successfully!", 
                    "copy details link": response.headers.get("Location"),
                }
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)



def onedrive_delete_file(access_token, params):
    """
    Delete a DriveItem by using its ID. Deleting items using this method moves the items to the recycle bin instead of permanently deleting the item.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :file_id: (str,required) - ID of the file to be deleted.

    Returns:
        dict: Confirmation message after successful deletion.
    """
    try:
        if "file_id" in params:
            file_id = params["file_id"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}"
            headers = {
                "Authorization": "Bearer " + access_token,
            }
            response = requests.delete(url=graph_api_url, headers=headers)
            if response.status_code == 204:
                return {"message": "File deleted successfully!"}
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)



def onedrive_create_new_text_file(access_token, params):
    """
    Provide the contents of a new text file in a single API call. This method only supports files up to 250 MB in size.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :parent_folder_id: (str,required) - ID of the parent folder the file needs to be uploaded to.
        - :name: (str,required) - the new name to be assigned to the file.
        - :content: (str,required) - the string content of the new text file to be created
    
    Returns:
        dict: contains a driveItem resource for the newly created file.
    """
    try:
        if "parent_folder_id" in params and "name" in params and "content" in params:
            parent_folder_id = params["parent_folder_id"]
            name = params["name"]
            content = params["content"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{parent_folder_id}:/{name}:/content"
            headers = {
                "Authorization": "Bearer " + access_token,
                "Content-type": "text/plain"
            }
            response = requests.put(
                url=graph_api_url, headers=headers, data=content)
            if response.status_code == 201:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)



def onedrive_download_file(access_token, params):
    """
    Retrieve a file download link from OneDrive using the Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :file_id: (str,required) - ID of the file to be downloaded.

    Returns:
        dict: Details of the retrieved file.
    """
    try:
        if "file_id" in params:
            file_id = params["file_id"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/content"
            headers = {
                "Authorization": "Bearer " + access_token
            }
            response = requests.get(url=graph_api_url, headers=headers, allow_redirects=False)
            if response.status_code == 302:
                return {
                    "message": "File Download link retrieved successfully!", 
                    "Download link": response.headers.get("Location"),
                }
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)



def onedrive_rename_file(access_token, params):
    """
    Renames File with the provided name using Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :file_id: (str,required) - ID of the file to be renamed.
        - :name: (str,required) - the new name to be assigned to the file.
    
    Returns:
        dict: driveItem resource of the renamed file.
    """
    try:
        if "file_id" in params and "name" in params:
            file_id = params["file_id"]
            name = params["name"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}"
            headers = {
                "Authorization": "Bearer " + access_token,
                "Content-type": "application/json"
            }
            data = {}
            data["name"] = name
            response = requests.patch(
                url=graph_api_url, headers=headers, json=data)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)




def onedrive_search_file(access_token, params):
    """
    Search the hierarchy of items for items matching a query. using the Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :query: (str,required) - The query text used to search for items. Values may be matched across several fields including filename, metadata, and file content.

    Returns:
        dict: collection of DriveItems that match the search criteria. If no items were found, an empty collection is returned.
    """
    try:
        if "query" in params:
            query = params["query"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/drive/search(q='{query}')"
            headers = {
                "Authorization": "Bearer " + access_token,
            }
            response = requests.get(url=graph_api_url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)



def onedrive_share_file(access_token, params):
    """
    creates a sharing link for DriveItem using Microsoft Graph API.

    :accessToken: Access token String for authentication with Microsoft Graph API.
    :params: Dictionary containing parameters.

    - :file_id: (str,required) - ID of the file to be shared.
    - :type: (str,required) - The type of sharing link to create. (view, edit, embed)
    - :scope: (str,required) - The scope of link to create. (anonymous, organization, users)
    - :password: (str,optional) - The password of the sharing link that is set by the creator. Optional and OneDrive Personal only.
    - :expirationDateTime: (str,optional) - A String with format of yyyy-MM-ddTHH:mm:ssZ of DateTime indicates the expiration time of the permission.
    - :retainInheritedPermissions: (bool,optional) - Optional. 
    
        If true (default), any existing inherited permissions are retained on 
        
        the shared item when sharing this item for the first time. 
        
        If false, all existing permissions are removed when sharing 
        
        for the first time.
    
    
    Returns:
        dict: returns a single Permission resource in the response body that represents the requested sharing permission.
    """
    try:
        if "file_id" in params and "type" in params and "scope" in params:
            file_id = params["file_id"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/createLink"
            headers = {
                "Authorization": "Bearer " + access_token,
                "Content-type": "application/json"
            }
            data = {}
            ignore_keys = ["file_id"]
            data = {
                key: value
                for (key, value) in params.items()
                if value
                if key not in ignore_keys
            }
            response = requests.post(
                url=graph_api_url, headers=headers, json=data)
            if response.status_code == 201:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)



def onedrive_upload_file(access_token, params):
    """
    Provide the contents of a file in a single API call. This method only supports files up to 250 MB in size.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :parent_folder_id: (str,required) - ID of the parent folder the file needs to be uploaded to.
        - :name: (str,required) - the name to be assigned to the uploaded file as well as its extension.
        - :content_type: (str,required) - the value of the Content-type parameter to be included in the header that describes the type of the file.for more information see this `page <https://www.geeksforgeeks.org/http-headers-content-type/>`_.
        - :content_choice: (str,required) - choice for whether the user wants to upload a file by uploading it's bytestring or by providing a url. Optional Values: (byteString, url)
        - :content: (str,optional) - the base64 byte string content of the file to be uploaded. (is required when the value of content_choice is byteString)
        - :url: (str,optional) - the link containing the file to be uploaded. (is required when the value of content_choice is url)
    
    Returns:
        dict: contains a driveItem resource for the newly uploaded file.
    """
    try:
        if "parent_folder_id" in params and "name" in params and "content_choice" in params  and "content_type" in params:
            parent_folder_id = params["parent_folder_id"]
            name = params["name"]
            content_choice = params["content_choice"]
            content_type = params["content_type"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{parent_folder_id}:/{name}:/content"
            headers = {
                "Authorization": "Bearer " + access_token,
                "Content-type": content_type,
            }
            body = ""
            if content_choice == "byteString" and "content" in params:
                body = base64.b64decode(params["content"])
            elif content_choice == "url" and "url" in params:
                try:
                    url_response = requests.get(params["url"], stream=True)
                    url_response.raise_for_status()  
                    body = url_response.content
                except requests.RequestException as e:
                    raise Exception(f"Error downloading file from URL: {e}")
                except Exception as e:
                    raise Exception(f"error: {e}")
                if not body:
                    raise Exception("File content is empty.")
            else:
                raise Exception("missing input data")
            response = requests.put(
                url=graph_api_url, headers=headers, data=body)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)






def onedrive_create_folder(access_token, params):
    """
    Create a new folder or DriveItem in a Drive with a specified parent item or path.
    
    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :name: (str,required) - the name to be assigned to the new folder.
        - :parent_folder_id: (str,optional) - ID of the parent folder of the new folder. if absent, the new folder will be created in the root folder.
    
    Returns:
        dict: driveItem resource of the newly created folder.
    """
    try:
        if "name" in params:
            name = params["name"]
            if "parent_folder_id" in params:
                parent_folder_id = params["parent_folder_id"]
                graph_api_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{parent_folder_id}/children"
            else:
                graph_api_url = f"https://graph.microsoft.com/v1.0/me/drive/root/children"
            
            headers = {
                "Authorization": "Bearer " + access_token,
                "Content-type": "application/json"
            }
            data = {
                "name": name,
                "folder": { },
                "@microsoft.graph.conflictBehavior": "rename"
            }
            response = requests.post(
                url=graph_api_url, headers=headers, json=data)
            if response.status_code == 201:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)



def onedrive_delete_folder(access_token, params):
    """
    Delete a DriveItem by using its ID or path. Deleting items using this method moves the items to the recycle bin instead of permanently deleting the item.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :folder_id: (str,required) - ID of the folder to be deleted.

    Returns:
        dict: Confirmation message after successful deletion.
    """
    try:
        if "folder_id" in params:
            folder_id = params["folder_id"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{folder_id}"
            headers = {
                "Authorization": "Bearer " + access_token,
            }
            response = requests.delete(url=graph_api_url, headers=headers)
            if response.status_code == 204:
                return {"message": "Folder deleted successfully!"}
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)



def onedrive_get_items_in_folder(access_token, params):
    """
    Return a collection of DriveItems in the children relationship of a DriveItem.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :folder_id: (str,required) - ID of the folder containing the items to be retrieved.

    Returns:
        dict: the list of items in the children collection of the target item. The children collection will be composed of driveItem resources.
    """
    try:
        if "folder_id" in params:
            folder_id = params["folder_id"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{folder_id}/children"
            headers = {
                "Authorization": "Bearer " + access_token
            }
            response = requests.get(url=graph_api_url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)



def onedrive_rename_folder(access_token, params):
    """
    Renames Folder with the provided name using Microsoft Graph API.
    
    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :folder_id: (str,required) - ID of the folder to be renamed.
        - :name: (str,required) - the new name to be assigned to the folder.
    
    Returns:
        dict: driveItem resource of the renamed folder.
    """
    try:
        if "folder_id" in params and "name" in params:
            folder_id = params["folder_id"]
            name = params["name"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{folder_id}"
            headers = {
                "Authorization": "Bearer " + access_token,
                "Content-type": "application/json"
            }
            data = {}
            data["name"] = name
            response = requests.patch(
                url=graph_api_url, headers=headers, json=data)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)



def onedrive_search_folder(access_token, params):
    """
    Search the hierarchy of items for items matching a query. using the Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :query: (str,required) - The query text used to search for items. Values may be matched across several fields including filename, metadata, and file content.

    Returns:
        dict: collection of DriveItems that match the search criteria. If no items were found, an empty collection is returned.
    """
    try:
        if "query" in params:
            query = params["query"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/drive/root/search(q='{query}')"
            headers = {
                "Authorization": "Bearer " + access_token,
            }
            response = requests.get(url=graph_api_url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)



def onedrive_share_folder(access_token, params):
    """
    creates a sharing link for DriveItem using Microsoft Graph API.

    :accessToken: Access token String for authentication with Microsoft Graph API.
    :params: Dictionary containing parameters.

    - :folder_id: (str,required) - ID of the folder to be to be shared.
    - :type: (str,required) - The type of sharing link to create. (view, edit,embed)
    - :scope: (str,required) - The scope of link to create. (anonymous, organization, users)
    - :password: (str,optional) - The password of the sharing link that is set by the creator. Optional and OneDrive Personal only.
    - :expirationDateTime: (str,optional) - A String with format of yyyy-MM-ddTHH:mm:ssZ of DateTime indicates the expiration time of the permission.
    - :retainInheritedPermissions: (bool,optional) - Optional. 
    
        If true (default), any existing inherited permissions are retained on 
        
        the shared item when sharing this item for the first time. 
        
        If false, all existing permissions are removed when sharing 
        
        for the first time.
    
    
    Returns:
        dict: returns a single Permission resource in the response body that represents the requested sharing permissions.
    """
    try:
        if "folder_id" in params and "type" in params and "scope" in params:
            folder_id = params["folder_id"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{folder_id}/createLink"
            headers = {
                "Authorization": "Bearer " + access_token,
                "Content-type": "application/json"
            }
            data = {}
            ignore_keys = ["folder_id"]
            data = {
                key: value
                for (key, value) in params.items()
                if value
                if key not in ignore_keys
            }
            response = requests.post(
                url=graph_api_url, headers=headers, json=data)
            if response.status_code == 201:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)

