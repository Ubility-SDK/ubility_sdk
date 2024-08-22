from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import json
import logging

def create_service(access_token, API_SERVICE_NAME, API_VERSION):
    """
    Create a Google API service instance using the provided access token.
    :access_token: (str) The OAuth 2.0 access token for authentication.
    :API_SERVICE_NAME: (str) The name of the Google Sheets API service: "sheets".
    :API_VERSION: (str) The version of the Google Sheets API: "v4".
    Returns:
      Resource: An instance of the Google Sheets API service.
    """
    try:
        creds_data = json.loads(access_token)
        creds = Credentials.from_authorized_user_info(creds_data)
        if creds and creds.expired and creds.refresh_token:
            # in this case the token is expired and we need to get a new access token
            creds.refresh(Request())
        service = build(API_SERVICE_NAME, API_VERSION,
                        credentials=creds, static_discovery=False)
        logging.warning(API_SERVICE_NAME, API_VERSION, 'service created successfully')
        return service
    except Exception as e:
        logging.warning(f'Failed to create service instance for {e}')
        raise Exception(f'Failed to create service instance {e}')



def create_token(cred):
    try:
        result={}
        result['token']=cred['accessToken']
        result['refresh_token']=cred['refreshToken']
        result['token_uri']="https://oauth2.googleapis.com/token"
        result['client_id']=cred['clientID']
        result['client_secret']=cred['clientSecret']
        result['scopes']=["https://www.googleapis.com/auth/spreadsheets"]
        result['expiry']=cred['expirey']
        return json.dumps(result)
    except Exception as e:
        raise Exception(e)

#############################################################################################################################

# Document Actions


def googleSheet_create_spreadsheet(creds, API_SERVICE_NAME, API_VERSION, params):
    """
    Create a new Google Sheets spreadsheet.

    :access_token: (str) The OAuth 2.0 access token for authentication.
    :API_SERVICE_NAME: (str) The name of the Google Sheets API service: "sheets".
    :API_VERSION: (str) The version of the Google Sheets API: "v4".
    :params: (dict) A dictionary containing parameters:

    - :properties: (dict, required) - Dictionary containing spreadsheet properties.
    
            - :title: (str, required) - The title of the spreadsheet.
            - :locale: (str, optional) - The locale of the spreadsheet (e.g., 'es_ES').
            - :autoRecalc: (str, optional) - Automatic recalculation setting.
            
                (select one of: 'ON_CHANGE', 'MINUTE', 'HOUR')
    
    - :sheets: (list of dict, optional) - List of dictionaries representing sheets.
        
        Each dictionary should contain:
        
        - :properties: (dict) - Dictionary containing sheet properties.
            
            - :title: (str, required) - The title of the sheet.
            - :hidden: (bool, optional) - Boolean indicating whether the sheet is hidden.

    Returns:
      dict: A dictionary containing information about the created spreadsheet.

    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        if "properties" in params and "title" in params["properties"] and params["properties"]["title"]:
            service = create_service(access_token, API_SERVICE_NAME, API_VERSION)
            spreadsheet = service.spreadsheets().create(body=params).execute()
            return spreadsheet
        else:
            raise SyntaxError("Missing input data")

    except Exception as error:
        raise SyntaxError(error)


def googleSheet_delete_spreadsheet(creds, API_SERVICE_NAME, API_VERSION, params):
    """
    Delete a Google Sheets spreadsheet.

    :access_token: (str) The OAuth 2.0 access token for authentication.
    :API_SERVICE_NAME: (str) The name of the Google Drive API service: "drive".
    :API_VERSION: (str) The version of the Google Drive API: "v3".
    :params: (dict) A dictionary containing parameters:

    - :spreadsheetId: (str, required) - The ID of the spreadsheet to be deleted.

    Returns:
      dict: A dictionary containing information about the deletion result.

    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        if "spreadsheetId" in params:
            spreadsheet_id = params["spreadsheetId"]
            drive_service = create_service(access_token, API_SERVICE_NAME, API_VERSION)
            drive_service.files().delete(fileId=spreadsheet_id).execute()
            return {"Result": f"Deleted Spreadsheet ID: {spreadsheet_id}"}
        else:
            raise SyntaxError("Missing input data")

    except Exception as error:
        raise Exception(error)


def googleSheet_get_spreadsheet(creds, API_SERVICE_NAME, API_VERSION, params):
    """
    Get information about a Google Sheets spreadsheet.

    :access_token: (str) The OAuth 2.0 access token for authentication.
    :API_SERVICE_NAME: (str) The name of the Google Sheets API service: "sheets".
    :API_VERSION: (str) The version of the Google Sheets API: "v4".
    :params: (dict) A dictionary containing parameters:

    - :spreadsheetId: (str, required) - The ID of the spreadsheet to retrieve information about.

    Returns:
      dict: A dictionary containing information about the specified spreadsheet.

    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        if "spreadsheetId" in params:
            id = params["spreadsheetId"]
            service = create_service(access_token, API_SERVICE_NAME, API_VERSION)
            response = service.spreadsheets().get(spreadsheetId=id).execute()
            return response
        else:
            raise SyntaxError("Missing input data")

    except Exception as error:
        raise Exception(error)


def googleSheet_list_spreadsheets(creds, API_SERVICE_NAME, API_VERSION):
    """
    List all Google Sheets spreadsheets in the user's Drive.

    :access_token: (str) The OAuth 2.0 access token for authentication.
    :API_SERVICE_NAME: (str) The name of the Google Sheets API service: "sheets".
    :API_VERSION: (str) The version of the Google Sheets API: "v4".

    Returns:
      dict: A dictionary containing information about the user's Google Sheets spreadsheets.
      
    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        query = "mimeType='application/vnd.google-apps.spreadsheet'"
        drive_service = create_service(access_token, API_SERVICE_NAME, API_VERSION)
        results = drive_service.files().list(q=query).execute()
        return results

    except Exception as error:
        raise Exception(error)


#############################################################################################################################

# Sheet Within Document Actions


def googleSheet_create_sheet(creds, API_SERVICE_NAME, API_VERSION, params):
    """
    Create a new sheet within a Google Sheets spreadsheet.

    :access_token: (str) The OAuth 2.0 access token for authentication.
    :API_SERVICE_NAME: (str) The name of the Google Sheets API service: "sheets".
    :API_VERSION: (str) The version of the Google Sheets API: "v4".
    :params: (dict) A dictionary containing parameters for creating the sheet.

    Returns:
      dict: A dictionary containing information about the created sheet.

    :Example:

    >>> params = 
            {
                "spreadsheetId": "your_spreadsheet_id", # (str, required)
                "requests": 
                [
                    {
                        "addSheet": 
                        {
                            "properties": 
                            {
                                "sheetId": your_sheet_id, # (int)
                                "title": "New Sheet", # (str, required)
                                "hidden": False,
                                "rightToLeft": True,
                                "index": 4,
                                "tabColor": 
                                {
                                    "red": 224,
                                    "green": 90,
                                    "blue": 57
                                }
                            }
                        }
                    }
                ]
            }

    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        if "spreadsheetId" in params and "requests" in params:
            id = params["spreadsheetId"]
            service = create_service(access_token, API_SERVICE_NAME, API_VERSION)
            data = {}
            for key, value in params.items():
                if key == "spreadsheetId":
                    continue
                if value:
                    data[key] = value
            response = service.spreadsheets().batchUpdate(spreadsheetId=id, body=data).execute()
            return response

        else:
            raise SyntaxError("Missing input data")

    except Exception as error:
        raise Exception(error)


def googleSheet_append_data_to_sheet(creds, API_SERVICE_NAME, API_VERSION, params):
    """
    Append data to a specific sheet within a Google Sheets spreadsheet.

    :access_token: (str) The OAuth 2.0 access token for authentication.
    :API_SERVICE_NAME: (str) The name of the Google Sheets API service: "sheets".
    :API_VERSION: (str) The version of the Google Sheets API: "v4".
    :params: (dict) A dictionary containing parameters for appending data to the sheet.

    Returns:
      dict: A dictionary containing information about the appended data.

    :Example:

    >>> params = 
            {
                "spreadsheetId": "your_spreadsheet_id", # (str, required)
                "sheetName": "your_sheet_name", # (str, required)
                "values": # (list of str, required)
                    [ 
                        ["A1", "B1", "C1"],
                        ["A2", "B2", "C2"]
                    ]
            }

    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        if "spreadsheetId" in params and "sheetName" in params and "values" in params:
            id = params["spreadsheetId"]
            range_to_append = params["sheetName"]
            append_values_request = {"values": params["values"]}
            service = create_service(access_token, API_SERVICE_NAME, API_VERSION)
            response = service.spreadsheets().values().append(spreadsheetId=id, range=range_to_append, body=append_values_request, valueInputOption="USER_ENTERED").execute()
            return response

        else:
            raise SyntaxError("Missing input data")
        
    except Exception as error:
        raise Exception(error)


def googleSheet_update_rows_in_sheet(creds, API_SERVICE_NAME, API_VERSION, params):
    """
    Append data to a specific sheet within a Google Sheets spreadsheet.

    :access_token: (str) The OAuth 2.0 access token for authentication.
    :API_SERVICE_NAME: (str) The name of the Google Sheets API service: "sheets".
    :API_VERSION: (str) The version of the Google Sheets API: "v4".
    :params: (dict) A dictionary containing parameters for updating rows in the sheet.

    Returns:
      dict: A dictionary containing information about the updated data.

    :Example:

    >>> params = 
            {
                "spreadsheetId": "your_spreadsheet_id", # (str, required)
                "sheetName": "your_sheet_name", # (str, required)
                "range": "A1:C2", # (str, required)
                "values": # (list of str, required)
                    [
                        ["A1", "B1", "C1"],
                        ["A2", "B2", "C2"]
                    ]
            }

    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        if "spreadsheetId" in params and "sheetName" in params and "range" in params and "values" in params:
            id = params["spreadsheetId"]
            range_to_update = f"'{params['sheetName']}'!{params['range']}"
            update_values_request = {"values": params["values"]}
            service = create_service(access_token, API_SERVICE_NAME, API_VERSION)
            response = service.spreadsheets().values().update(spreadsheetId=id, range=range_to_update, body=update_values_request, valueInputOption="USER_ENTERED").execute()
            return response

        else:
            raise SyntaxError("Missing input data")
        
    except Exception as error:
        raise Exception(error)


def googleSheet_read_rows_in_sheet(creds, API_SERVICE_NAME, API_VERSION, params):
    """
    Read rows from a specific sheet within a Google Sheets spreadsheet.

    :access_token: (str) The OAuth 2.0 access token for authentication.
    :API_SERVICE_NAME: (str) The name of the Google Sheets API service: "sheets".
    :API_VERSION: (str) The version of the Google Sheets API: "v4".
    :params: (dict) A dictionary containing parameters for reading rows from the sheet.

    Returns:
      dict: A dictionary containing information about the updated data.

    :Example:

    >>> params = 
            {
                "spreadsheetId": "your_spreadsheet_id",  # (str, required)
                "sheetName": "your_sheet_name", # (str, required)
                "range": "A1:C2", # (str, optional)
                "majorDimension": "ROWS", # (str, optional)
            }

    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        if "spreadsheetId" in params and "sheetName" in params:
            id = params["spreadsheetId"]
            if "range" in params:
                range_to_read = f"'{params['sheetName']}'!{params['range']}"
            else:
                range_to_read = params["sheetName"]

            majorDimension = "DIMENSION_UNSPECIFIED"
            if "majorDimension" in params:
                majorDimension = params["majorDimension"]

            service = create_service(access_token, API_SERVICE_NAME, API_VERSION)
            response = service.spreadsheets().values().get(spreadsheetId=id, range=range_to_read, majorDimension=majorDimension).execute()
            return response

        else:
            raise SyntaxError("Missing input data")
        
    except Exception as error:
        raise Exception(error)


def googleSheet_delete_ColOrRow_from_sheet(creds, API_SERVICE_NAME, API_VERSION, params):
    """
    Delete columns or rows from a specific sheet within a Google Sheets spreadsheet.

    :access_token: (str) The OAuth 2.0 access token for authentication.
    :API_SERVICE_NAME: (str) The name of the Google Sheets API service: "sheets".
    :API_VERSION: (str) The version of the Google Sheets API: "v4".
    :params: (dict) A dictionary containing parameters for deleting columns or rows.

    Returns:
      dict: A dictionary containing information about the delete operation.

    :Example:

    >>> params = 
            {
                "spreadsheetId": "your_spreadsheet_id", # (str, required)
                "requests": 
                [
                    {
                        "deleteDimension": 
                        {
                            "range": 
                            {
                                "sheetId": your_sheet_id, # (int, required)
                                "dimension": "ROWS", # (str, required) "ROWS" or "COLUMNS"
                                "startIndex": 0,  # (int, required) - delete action starts after this index 
                                "endIndex": 15  # (int, required) - delete action ends at this index 
                            }
                        }
                    }
                ]
            }

    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        if "spreadsheetId" in params and "requests" in params:
            id = params["spreadsheetId"]
            service = create_service(access_token, API_SERVICE_NAME, API_VERSION)
            data = {}
            for key, value in params.items():
                if key == "spreadsheetId":
                    continue
                if value:
                    data[key] = value
            response = service.spreadsheets().batchUpdate(spreadsheetId=id, body=data).execute()
            return response

        else:
            raise SyntaxError("Missing input data")

    except Exception as error:
        raise Exception(error)


def googleSheet_remove_sheet(creds, API_SERVICE_NAME, API_VERSION, params):
    """
    Remove a sheet from a Google Sheets spreadsheet.

    :access_token: (str) The OAuth 2.0 access token for authentication.
    :API_SERVICE_NAME: (str) The name of the Google Sheets API service: "sheets".
    :API_VERSION: (str) The version of the Google Sheets API: "v4".
    :params: (dict) A dictionary containing parameters for removing a sheet.

    Returns:
      dict: A dictionary containing information about the remove sheet operation.

    :Example:

    >>> params = 
            {
                "spreadsheetId": "your_spreadsheet_id", # (str, required)
                "requests": 
                [
                    {
                        "deleteSheet": 
                        {
                            "sheetId": your_sheet_id # (int, required)
                        }
                    }
                ]
            }

    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        if "spreadsheetId" in params and "requests" in params:
            id = params["spreadsheetId"]
            service = create_service(access_token, API_SERVICE_NAME, API_VERSION)
            data = {}
            for key, value in params.items():
                if key == "spreadsheetId":
                    continue
                if value:
                    data[key] = value
            response = service.spreadsheets().batchUpdate(spreadsheetId=id, body=data).execute()
            return response

        else:
            raise SyntaxError("Missing input data")

    except Exception as error:
        raise Exception(error)


def googleSheet_clear_data_from_sheet(creds, API_SERVICE_NAME, API_VERSION, params):
    """
    Clear data from a specific range or sheet within a Google Sheets spreadsheet.

    :access_token: (str) The OAuth 2.0 access token for authentication.
    :API_SERVICE_NAME: (str) The name of the Google Sheets API service: "sheets".
    :API_VERSION: (str) The version of the Google Sheets API: "v4".
    :params: (dict) A dictionary containing parameters for clearing data.

    Returns:
      dict: A dictionary containing information about the clear data operation.

    :Example:

    >>> params = 
            {
                "spreadsheetId": "your_spreadsheet_id", # (str, required)
                "sheetName": "your_sheet_name", # (str, required)
                "range": "A1:B10"  # (str, required)
            }

    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        if "spreadsheetId" in params and "sheetName" in params:
            id = params["spreadsheetId"]
            if "range" in params:
                range_to_delete = f"'{params['sheetName']}'!{params['range']}"
            else:
                range_to_delete = params["sheetName"]

            service = create_service(access_token, API_SERVICE_NAME, API_VERSION)
            response = service.spreadsheets().values().clear(spreadsheetId=id, range=range_to_delete).execute()
            return response

        else:
            raise SyntaxError("Missing input data")
        
    except Exception as error:
        raise Exception(error)