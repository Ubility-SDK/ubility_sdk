# import io
# import os
# from googleapiclient.http import MediaIoBaseDownload
import json
from io import BytesIO
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseUpload
import requests
import base64
status=[200, 201, 202, 204, 206, 207, 208]
    # """
    # Create a new folder in Google Drive.

    # :param str access_token:
    #     The access token for authenticating with Google Drive. (required)

    # :param dict params:
    #     - content (str): The content to be added to the file.(required)
    #     - body (dict):
    #         - name (str): The name of the new folder. (required)
    #         - parents (list): A list of parent folder IDs where the new folder should be created. (optional)
    #     - ocrLanguage (str): The language to use for OCR (Optical Character Recognition).
    #     - useContentAsIndexableText (bool): Whether to use the content as indexable text.
    #     - properties (list): A list of custom properties with keys and values.
    #     - appProperties (list): A list of custom app properties with keys and values.

    # :return: The response from the Google Drive API after creating the folder.
    # :rtype: dict
    # """
def create_service(access_token, API_SERVICE_NAME, API_VERSION):
    try:
        creds_data = json.loads(access_token)
        creds = Credentials.from_authorized_user_info(creds_data)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        service = build(API_SERVICE_NAME, API_VERSION,
                        credentials=creds, static_discovery=False)
        return service
    except Exception as e:
        raise Exception(
            f'Failed to create service instance for {API_SERVICE_NAME}')

def create_token(cred):
    try:
        result={}
        result['token']=cred['accessToken']
        result['refresh_token']=cred['refreshToken']
        result['token_uri']="https://oauth2.googleapis.com/token"
        result['client_id']=cred['clientID']
        result['client_secret']=cred['clientSecret']
        result['scopes']=["https://www.googleapis.com/auth/drive"]
        result['expiry']=cred['expirey']
        return json.dumps(result)
    except Exception as e:
        raise Exception(e) 
    
def googledrive_create_folder(creds,params):
    """
    Create a new folder in Google Drive.

    :param str access_token:
        The access token for authenticating with Google Drive. (required)

    :param dict params:
        - body (dict):
            - name (str): The name of the folder. (required)
            - mimeType (str): The MIME type of the folder, indicating it is a Google Drive folder. (required)
            - parents (list): A list of parent folder IDs. (optional)

    :return: The response from the Google Drive API after creating the folder.
    :rtype: dict
    """
    try:
            cred=json.loads(creds)
            access_token=create_token(cred)
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            service = create_service(access_token,'drive', 'v3')
            response = service.files().create(**data).execute()
            return response
    except Exception as e:
        raise Exception(str(e))
      
def googledrive_delete_file(creds,params):
    """
    Delete a file or folder from Google Drive.

    :param str access_token:
        The access token for authenticating with Google Drive. (required)

    :param dict params:
        - fileId (str): The ID of the file or folder to be deleted. (required)
        - body (dict):
            -trashed(bool): Delete the file or folder permanently.(optional)

    :return: The response from the Google Drive API after deleting the file or folder.
    :rtype: str
    """
    try:
            cred=json.loads(creds)
            access_token=create_token(cred)
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            service = create_service(access_token,'drive', 'v3')
            if 'body'in data :
                response = service.files().update(**data).execute()
                return response
            else:
                response = service.files().delete(**data).execute()
                return "Folder deleted successfully"
    except Exception as e:
        raise Exception(str(e))
    
def googledrive_share_file(creds,params):
    """
    Share a file or folder in Google Drive with specified permissions.

    :param str access_token:
        The access token for authenticating with Google Drive. (required)

    :param dict params:
        - fileId (str): The ID of the file or folder to be shared. (required)
        - emailMessage (str): A message to include in the email notification. (optional)
        - sendNotificationEmail (bool): Whether to send a notification email or not. (optional)
        - useDomainAdminAccess (bool): Whether to use domain administrator access. (optional)
        - transferOwnership (bool): Whether to transfer ownership to new specified owners. (optional)
        - body (dict):
            - role(str): The role granted by this permission.(optional)
            - type(str): The type of the grantee.(optional)
            - emailAddress(str): The email address of the user or group to which this permission refers.(optional)
            - domain(str): The domain to which this permission refers.(optional)
            - allowFileDiscovery(bool): Whether the permission allows the file to be discovered through search.(optional)


    :return: The response from the Google Drive API after sharing the file or folder.
    :rtype: dict
    """
    try:
            cred=json.loads(creds)
            access_token=create_token(cred)
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            service = create_service(access_token,'drive', 'v3')
            response = service.permissions().create(**data).execute()
            return response 
    except Exception as e:
        raise Exception(str(e))
    
def googledrive_copy_file(creds,params):
    """
    Copy a file on Google Drive.

    :param str access_token:
        The access token for authenticating with Google Drive. (required)

    :param dict params:
        - fileId (str): The ID of the file to be copied.
        - body (dict):
            - name (str): The name for the copied file.
            - description (str): The description for the copied file.
            - parents (list): A list containing the ID(s) of the folder(s) where the copy should be placed.

    :return: The API response after copying the file.
    :rtype: dict
    """
    try:
            cred=json.loads(creds)
            access_token=create_token(cred)
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            service = create_service(access_token,'drive', 'v3')
            response = service.files().copy(**data).execute()
            return response 
    except Exception as e:
        raise Exception(str(e))
       
def googledrive_move_file(creds,params):
    """
    Move a file or folder on Google Drive.

    :param str access_token:
        The access token for authenticating with Google Drive. (required)

    :param dict params:
        - fileId (str): The ID of the file or folder to be moved.(required)
        - addParents (str): ID of the folder where the file or folder should be moved.(required)

    :return: The API response after moving the file or folder.
    :rtype: dict
    """
    try:
            cred=json.loads(creds)
            access_token=create_token(cred)
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            service = create_service(access_token,'drive', 'v3')
            response = service.files().update(**data).execute()
            return response 
    except Exception as e:
        raise Exception(str(e))

def googledrive_create_file_text(creds,params):
    """
    Create a new file in Google Drive.

    :param str access_token:
        The access token for authenticating with Google Drive. (required)

    :param dict params:
        - content (str): The content to be added to the file.(required)
        - body (dict):
            - name (str): The name of the new folder. (required)
            - parents (list): A list of parent folder IDs where the new folder should be created. (optional)
        - ocrLanguage (str): The language to use for OCR (Optical Character Recognition).(optional)
        - useContentAsIndexableText (bool): Whether to use the content as indexable text.(optional)
        - properties (list): A list of custom properties with keys and values.(optional)
        - appProperties (list): A list of custom app properties with keys and values.(optional)

    :return: The response from the Google Drive API after creating the folder.
    :rtype: dict
    """
    try:
            cred=json.loads(creds)
            access_token=create_token(cred)
            data = {}
            for key, value in params.items():
                if key=='content':
                     continue
                if value:
                    data[key] = value
            service = create_service(access_token,'drive', 'v3')
            media = MediaIoBaseUpload(
            BytesIO(params['content'].encode('utf-8')),
            mimetype='text/plain',
            resumable=True
        )
            response = service.files().create(**data,media_body=media).execute()
            return response
    except Exception as e:
        raise Exception(str(e))    

def googledrive_upload_file(creds,params):
    """
    Upload a file to Google Drive.

    :param str access_token:
        The access token for authenticating with Google Drive. (required)

    :param dict params:
            - data (bytes): The binary data of the file to be uploaded in the form of a base64 string.(required, if 'url' is not provided)
            - url (str): The URL from which the file should be downloaded for uploading.(required, if 'url' is not provided)
            - body (dict):
                - name (str): The name of the file.(required)
                - parents (list): A list containing the ID(s) of the folder(s) where the file should be uploaded.(optional)
                - ocrLanguage (str): The OCR language for the file.(optional)
                - useContentAsIndexableText (bool): Whether to use content as indexable text.(optional)
                - properties (list): A list of custom properties with keys and values.(optional)
                - appProperties (list): A list of custom app properties with keys and values.(optional)

    :return: The API response after uploading the file.
    :rtype: dict
    """
    try:
            cred=json.loads(creds)
            access_token=create_token(cred)
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            service = create_service(access_token,'drive', 'v3')
            if 'data' in data:
                content = base64.b64decode(data['data'])
                media = MediaIoBaseUpload(BytesIO(content), mimetype='application/octet-stream', resumable=True)
                response = service.files().create(body=data['body'],media_body=media).execute()
                return response
            elif 'url' in data:
                 response = requests.get(data['url'])
                 if response.status_code in status:
                    file_content = response.content
                    media = MediaIoBaseUpload(BytesIO(file_content), mimetype='application/octet-stream', resumable=True)
                    url = service.files().create(body=data['body'],media_body=media).execute()
                    return url
    except Exception as e:
        raise Exception(str(e))
    

def googledrive_update_file(creds,params):
    """
    Update a file on Google Drive with new content and metadata.

    :param str access_token:
        The access token for authenticating with Google Drive. (required)

    :param dict params:
        - fileId (str): The ID of the file to be updated.(required)
        - data (bytes): The binary data of the file for updating its content.(required)
        - body (dict):
            - name (str): The new name of the file.(optional)
            - properties (list): A list of custom properties with keys and values.(optional)
            - appProperties (list): A list of custom app properties with keys and values.(optional)
            - ocrLanguage (str): The new OCR language for the file.(optional)
            - useContentAsIndexableText (bool): Whether to use content as indexable text.(optional)

    :return: The API response after updating the file.
    :rtype: dict
    """
    try:
            cred=json.loads(creds)
            access_token=create_token(cred)
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            service = create_service(access_token,'drive', 'v3')
            file_metadata = service.files().get(fileId=data['fileId']).execute()
            new_file_name = data['body']['name'] if 'name' in data['body'] and data['body']['name']!='' else file_metadata['name']
            data['body']['name']= new_file_name
            media = MediaIoBaseUpload(BytesIO(data['data']), mimetype='application/octet-stream', resumable=True)
            response = service.files().update(fileId=data['fileId'],body=data['body'],media_body=media).execute()
            return response
    except Exception as e:
        raise Exception(str(e))
       
def googledrive_get_many_files(creds,params):
    """
    Get a list of files from Google Drive based on specified criteria.

    :param str access_token:
        The access token for authenticating with Google Drive. (required)

    :param dict params:
        - pageSize (int): The maximum number of files to return per page.(optional)
        - parent (str): The ID of the parent folder.(optional)
        - trashed (bool): Whether to include trashed files.(optional)
        - type (list): A list of MIME types to filter the search.(optional)
        - fields (str): The fields to include in the response.(optional)
        - query (str): A custom query string for additional filtering.(optional)
        - name (str): The name of the file or folder to search for.(optional)
        
    :return: A dictionary containing information about the files matching the criteria.
    :rtype: dict
    """
    try:
            cred=json.loads(creds)
            access_token=create_token(cred)
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            query_parts = []
            query_parts.append("mimeType != 'application/vnd.google-apps.folder'") 
            if 'query' in data:
                query_parts.append(data['query'])
            if 'name' in data:
                query_parts.append(f"name contains '{data['name']}'")
            if 'type' in data:
                type_queries = []
                for type_value in data['type']:
                    type_queries.append(f"({type_value})")
                type_query = " or ".join(type_queries)
                type_query = f"({type_query})"
                query_parts.append(type_query)
            if 'parent' in data:
                 query_parts.append((f"'{data['parent']}' in parents"))
            if 'trashed' in data:
                query_parts.append(f"trashed={data['trashed']}")
            query = " and ".join(query_parts)
            service = create_service(access_token,'drive', 'v3')
            if not query:
                files = service.files().list(**data).execute()
            else:
                data2 = {}
                for key, value in data.items():
                    if key=='name':
                        continue
                    if key=='type':
                         continue
                    if key=='query':
                         continue
                    if key=='parent':
                         continue
                    if key=='trashed':
                         continue
                    if value:
                        data2[key] = value
                files = service.files().list(**data2,q=query).execute()
            return files
    except Exception as e:
        raise Exception(str(e))

def googledrive_get_many_folders(creds,params):
    """
    Get a list of folders from Google Drive based on specified criteria.

    :param str access_token:
        The access token for authenticating with Google Drive. (required)

    :param dict params:
        - pageSize (int): The maximum number of folders to return per page.(optional)
        - parent (str): The ID of the parent folder.(optional)
        - trashed (bool): Whether to include trashed folders.(optional)
        - fields (str): The fields to include in the response.(optional)
        - query (str): A custom query string for additional filtering.(optional)
        - name (str): The name of the folder to searc   h for.(optional)

    :return: A dictionary containing information about the folders matching the criteria.
    :rtype: dict
    """
    try:
            cred=json.loads(creds)
            access_token=create_token(cred)
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            query_parts = []
            query_parts.append("mimeType ='application/vnd.google-apps.folder'") 
            if 'query' in data:
                query_parts.append(data['query'])
            if 'name' in data:
                query_parts.append(f"name contains '{data['name']}'")
            if 'parent' in data:
                 query_parts.append((f"'{data['parent']}' in parents"))
            if 'trashed' in data:
                query_parts.append(f"trashed={data['trashed']}")
            query = " and ".join(query_parts)
            service = create_service(access_token,'drive', 'v3')
            if not query:
                files = service.files().list(**data).execute()
            else:
                data2 = {}
                for key, value in data.items():
                    if key=='name':
                        continue
                    if key=='query':
                         continue
                    if key=='parent':
                         continue
                    if key=='trashed':
                         continue
                    if value:
                        data2[key] = value
                files = service.files().list(**data2,q=query).execute()
            return files
    except Exception as e:
        raise Exception(str(e))    
    