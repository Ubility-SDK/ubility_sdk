import requests
import json
import base64

status = [200, 201, 202, 204, 206, 207, 208]


def microsoft_sharepoint_refresh_access_token(creds):
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

##########################################################################################################################

############################################ Sites ########################################################

def microsoft_sharepoint_search_sites(accessToken, params):
    """
    Search for Sites matching a query.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :query: (str,required) - the query to base the search on

    Returns:
        dict: a Dictionary containing the collection of site objects

    """
    try:
        required_params=["query"]
        if all(param in params for param in required_params):
            query = params["query"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/sites?search={query}"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.get(
                url=graph_api_url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)



################################### Pages #################################################################


def microsoft_sharepoint_publish_page(accessToken, params):
    """
    Publish a SharePoint Page using Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :site_id: (str,required) - Site ID of the Site containing the Page to be published
        - :page_id: (Str,required) - Page ID of the Page to be published
    

    Returns:
        dict: Dictionary containing a confirmation message.
    """
    try:
        required_params=["site_id","page_id"]
        if all(param in params for param in required_params):
            site_id = params.get("site_id", "")
            page_id = params.get("page_id", "")
            graph_api_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/pages/{page_id}/microsoft.graph.sitePage/publish"
            headers = {"Authorization": "Bearer " + accessToken}
            response = requests.post(
                url=graph_api_url, headers=headers)
            if response.status_code == 204:
                return {"message": "The Page was Successfully Published", "Page ID": page_id}
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)


################################### Lists ##########################################

def microsoft_sharepoint_create_list(accessToken, params):
    """
    Create a new list in a site.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :site_id: (str,required) - ID of the Site where the new list will be created
        - :displayName: (str,required) - Display name of the new list
        - :description: (Str,optional) - The description of the new list
        - :template: (Str,required) - The template on which the new list is based

    Returns:
        dict: Details of the newly created list.
    """
    try:
        required_params=["site_id","displayName", "template"]
        if all(param in params for param in required_params):
            site_id = params["site_id"]
            displayName = params["displayName"]
            template = params["template"]
            description = params.get("description", "")
            graph_api_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json"
            }
            data = {
                "displayName": displayName,
                "list": {
                    "template": template,
                },
            }
            if description:
                data["description"] = description
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


def microsoft_sharepoint_get_many_list_Columns(accessToken, params):
    """
    Get the collection of columns represented as columnDefinition resources in a list.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :site_id: (str,required) - ID of the site containing the list whose columns we will get
        - :list_id: (str,required) - ID of the list whose columns we will get
        - :select: (str,optional) - The expression specified with the `$select <https://learn.microsoft.com/en-us/graph/query-parameters?tabs=http#select-parameter>`_ OData query parameter to retrieve a subset or a superset of the default properties of the columnDefinition collection.

    Returns:
        dict: a Dictionary containing the collection of columnDefinition Objects
    """
    try:
        required_params=["site_id","list_id"]
        if all(param in params for param in required_params):
            site_id = params["site_id"]
            list_id = params["list_id"]
            select = params.get("select", "")
            graph_api_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{list_id}/columns"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            query = {}
            if select:
                query["$select"] = select
            response = requests.get(
                url=graph_api_url, headers=headers, params=query)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)


########################################## List Items ##########################################


def microsoft_sharepoint_get_many_list_items(accessToken, params):
    """
    Get the collection of items in a list.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :site_id: (str,required) - ID of the site containing the list whose items we will get
        - :list_id: (str,required) - ID of the list whose items we will get
        - :filter: (str,optional) - The expression specified with the `$filter <https://learn.microsoft.com/en-us/graph/query-parameters?tabs=http#filter-parameter>`_ OData query parameter to retrieve a subset of the list items collection.

    Returns:
        dict: A dictionary containing a list of list items

    """
    try:
        required_params=["site_id","list_id"]
        if all(param in params for param in required_params):
            site_id = params["site_id"]
            list_id = params["list_id"]
            filter = params.get("filter","")
            graph_api_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{list_id}/items"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            query = {"$expand": "fields"}
            if filter:
                query["$filter"] = filter
            response = requests.get(
                url=graph_api_url, headers=headers, params=query)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)


def microsoft_sharepoint_create_list_item(accessToken, params):
    """
    Create a new listItem in a list.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :site_id: (str,required) - ID of the site containing the list where we will create a new item
        - :list_id: (str,required) - ID of the list where we will create a new item
        - :fields: (dict,required) - dictionary containing the columns and their values to set on the newly created list item. for instance:

            - :column1: first column
            - :column2: second column
            .
            .
            .
            .etc...

    Returns:
        dict: Details of the newly created list item.

    """
    try:
        required_params=["site_id","list_id", "fields"]
        if all(param in params for param in required_params):
            site_id = params["site_id"]
            list_id = params["list_id"]
            fields = params["fields"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{list_id}/items"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json"
            }
            data = {"fields": fields}
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


def microsoft_sharepoint_update_list_item(accessToken, params):
    """
    Update the properties of fields on a listItem.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :site_id: (str,required) - ID of the site containing the list containing the item to be updated
        - :list_id: (str,required) - ID of the list containing the item to be updated
        - :item_id: (str,required) - ID of the list item to be updated
        - :fields: (dict,required) - dictionary containing the columns and their values to be updated on the selected list item. for instance:

            - :column1: first column
            - :column2: second column
            .
            .
            .
            .etc...

    Returns:
        dict: Details of the newly Updated list item.

    """
    try:
        required_params=["site_id","list_id", "item_id", "fields"]
        if all(param in params for param in required_params):
            site_id = params["site_id"]
            list_id = params["list_id"]
            item_id = params["item_id"]
            fields = params["fields"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{list_id}/items/{item_id}/fields"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json"
            }
            response = requests.patch(
                url=graph_api_url, headers=headers, json=fields)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)


def microsoft_sharepoint_delete_list_item(accessToken, params):
    """
    Removes an item from a list.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :site_id: (str,required) - ID of the site containing the list containing the item to be deleted
        - :list_id: (str,required) - ID of the list containing the item to be deleted
        - :item_id: (str,required) - ID of the list item to be deleted
        - :etag: (str,optional) - eTag of the version of the item to be deleted

    Returns:
        dict:  Dictionary containing a confirmation message.

    """
    try:
        required_params=["site_id","list_id", "item_id"]
        if all(param in params for param in required_params):
            site_id = params["site_id"]
            list_id = params["list_id"]
            item_id = params["item_id"]
            etag = params.get("etag", "")
            graph_api_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{list_id}/items/{item_id}"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            if etag:
                headers["if-match"] = etag
            response = requests.delete(
                url=graph_api_url, headers=headers)
            if response.status_code == 204:
                return {"message": "The List Item was Successfully Deleted", "Item ID": item_id}
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)


############################################ Files and Folders ##################################################


def microsoft_sharepoint_search_files_and_folders(accessToken, params):
    """
    Search for Dirve Items matching a query.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :site_id: (str,required) - ID of the site to search the contents of
        - :query: (str,required) - the query to base the search on

    Returns:
        dict:  an object containing an collection of DriveItems that match the search criteria. If no items were found, an empty collection is returned.

    """
    try:
        required_params=["site_id","query"]
        if all(param in params for param in required_params):
            site_id = params["site_id"]
            query = params["query"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root/search(q='{query}')"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.get(
                url=graph_api_url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)


def microsoft_sharepoint_create_folder(accessToken, params):
    """
    Create a new Folder in a site.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :site_id: (str,required) - ID of the Site where the new Folder will be created
        - :name: (str,required) - name of the new Folder
        - :parent_id: (Str,required) - ID of the parent of the new folder to be created

    Returns:
        dict: Details of the newly created Folder.
    """
    try:
        required_params=["site_id","name", "parent_id"]
        if all(param in params for param in required_params):
            site_id = params["site_id"]
            name = params["name"]
            parent_id = params["parent_id"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/{parent_id}/children"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json"
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



def microsoft_sharepoint_move_file_or_folder(accessToken, params):
    """
    Move a DriveItem to a new parent item

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :site_id: (str,required) - ID of the Site containing the DriveItem to be moved
        - :item_id: (str,required) - ID of the DriveItem to be moved
        - :parent_id: (str,required) - ID of the new parent the DriveItem will be moved to
        - :overwrite: (bool,optional) - overwrite the drive item if true and the parent contains a DriveItem with the same name

    Returns:
        dict: Details of the newly moved DriveItem.
    """
    try:
        required_params=["site_id","item_id", "parent_id"]
        if all(param in params for param in required_params):
            site_id = params["site_id"]
            item_id = params["item_id"]
            parent_id = params["parent_id"]
            overwrite = params.get("overwrite", False)
            graph_api_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/{item_id}"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json"
            }
            data = {
                "parentReference": {
                    "id": parent_id,
                },
                "@microsoft.graph.conflictBehavior": "fail"
            }
            if overwrite:
                data["@microsoft.graph.conflictBehavior"] = "replace"
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



def microsoft_sharepoint_upload_file(access_token, params):
    """
    Provide the contents of a file in a single API call. This method only supports files up to 250 MB in size.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :site_id: (str,required) - ID of the Site the file will be uploaded to
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
        required_params=["site_id","parent_folder_id", "name", "content_choice", "content_type"]
        if all(param in params for param in required_params):
            site_id = params["site_id"]
            parent_folder_id = params["parent_folder_id"]
            name = params["name"]
            content_choice = params["content_choice"]
            content_type = params["content_type"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/{parent_folder_id}:/{name}:/content"
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




############################################# END ######################################

